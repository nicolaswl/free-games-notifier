import praw
import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()
reddit = praw.Reddit(client_id=os.environ.get("CLIENT_ID"),
                     client_secret=os.environ.get("CLIENT_SECRET"),
                     user_agent=os.environ.get("USER_AGENT"))

sales = ""
for post in reddit.subreddit("gamedeals").top("day"):
        if "Free" in post.title:
            sales += post.title + "\n" + post.url + "\n\n"

if sales != "":
    recipients = []
    for line in open('./recipients'):
        recipients.append(line.strip())

    msg = EmailMessage()
    msg['Subject'] = "New Free Games"
    msg['From'] = os.environ.get("EMAIL")
    msg['To'] = ", ".join(recipients)
    msg.set_content(sales)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(os.environ.get("EMAIL"), os.environ.get("EMAIL_PASS"))
        smtp.send_message(msg)