import datetime as dt
import pandas as pd
import smtplib, random, os, dotenv

dotenv.load_dotenv()

my_gmail = os.getenv("SMTP_GMAIL_ID")
password_gmail = os.getenv("SMTP_GMAIL_PASSWORD")

now = dt.datetime.now()
today = (now.month, now.day)

data = pd.read_csv("birthdays.csv")

birthday_dict = {(data_row["month"], data_row["day"]): data_row for
                 (index, data_row) in data.iterrows()}

if today in birthday_dict:
    letter_path = f"letter_templates/letter_{random.randint(1, 3)}.txt"
    with open(letter_path, "r") as file:
        content = file.read()
        content = content.replace("[NAME]", birthday_dict[today]["name"])
        content = content.replace("[SENDER NAME]", "Divine Demon")

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_gmail, password=password_gmail)
        connection.sendmail(from_addr=my_gmail,
                            to_addrs=birthday_dict[today]["email"],
                            msg=f"subject:Happy Birthday!\n\n{content}")
