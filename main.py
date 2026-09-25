"""Implement a birthday wisher automation that sends an email to the user on
 their birthday."""
import datetime as dt
import pandas as pd
import smtplib
import random
import os
from dotenv import load_dotenv

load_dotenv()

my_gmail = os.getenv("SMTP_GMAIL_ID")
password_gmail = os.getenv("SMTP_GMAIL_PASSWORD")

now = dt.datetime.now()
today = (now.month, now.day)


def check_birthday():
    """Checks if today is a birthday"""
    data = pd.read_csv("birthdays.csv")
    birthday_dict = {(data_row["month"], data_row["day"]): data_row for
                     (_, data_row) in data.iterrows()}

    if today in birthday_dict:
        return birthday_dict[today]
    return None


def send_email():
    """Sends an email to the user on their birthday"""
    birthday_dict = check_birthday()
    letter_path = f"letter_templates/letter_{random.randint(1, 3)}.txt"
    with open(letter_path, "r") as file:
        content = file.read()
        content = content.replace("[NAME]", birthday_dict["name"])
        content = content.replace("[SENDER NAME]", "Divine Demon")

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_gmail, password=password_gmail)
        connection.sendmail(from_addr=my_gmail,
                            to_addrs=birthday_dict["email"],
                            msg=f"subject:Happy Birthday!\n\n{content}")


send_email()
