# 🎂 Birthday Wisher

A Python automation script that checks a birthday list every time it runs and automatically emails a personalized "Happy Birthday" message to anyone whose birthday is today — pulling from a randomized set of letter templates so the message doesn't feel copy-pasted.

> Run it once a day (via a scheduled task), and it quietly handles birthday wishes for you — no manual emailing required.

---

## 🎮 Demo

<img width="400" height="350" alt="Screenshot 2026-09-26 053130" src="https://github.com/user-attachments/assets/b62c844d-bab5-4fb0-986d-19cdc4ddeafc" />
<img width="400" height="350" alt="Screenshot 2026-09-26 053254" src="https://github.com/user-attachments/assets/41b087aa-6ef5-46bf-9069-86ae2b0a5d6e" />

---

## ✨ Features

- 📅 **Automatic date matching** — compares today's date against a CSV list of birthdays and only triggers for exact matches.
- 🎲 **Randomized message templates** — picks one of three pre-written letter templates each time, so recipients don't get the identical message every year.
- ✉️ **Real email delivery** via Gmail's SMTP server, using `smtplib` with a secure TLS connection.
- 🔒 **Credential safety** — Gmail login and password are loaded from environment variables via `python-dotenv`, keeping secrets out of the codebase entirely.
- 🧩 **Placeholder-based personalization** — dynamically swaps in the recipient's name and sender name into the chosen template.
- 📊 **Bulk-friendly data source** — birthdays are managed in a simple CSV file, easy to update without touching any code.

---

## 🛠️ Tech Stack

| Category | Tool / Concept |
|---|---|
| Language | Python 3 |
| Data Handling | `pandas` — reading and iterating over the birthdays CSV |
| Email | `smtplib` (standard library) — SMTP + TLS email delivery |
| Secrets Management | `python-dotenv` — loading credentials from a `.env` file |
| Core Concepts | Dictionary comprehensions, date comparison, file I/O, environment variables |

---

## 📂 Project Structure

```
Birthday Wisher/
│
├── main.py                    # Entry point — checks today's date and sends the email
├── birthdays.csv               # Your birthday list: name, email, month, day
├── letter_templates/
│   ├── letter_1.txt
│   ├── letter_2.txt
│   └── letter_3.txt
├── .env                         # Your Gmail credentials (never committed — see below)
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.x installed
- `pandas` and `python-dotenv` — install via pip:

```bash
pip install pandas python-dotenv
```

### Setup

**1. Create your `.env` file** in the project root with your Gmail credentials:

```
SMTP_GMAIL_ID=your_email@gmail.com
SMTP_GMAIL_PASSWORD=your_app_password
```

> ⚠️ Use a [Gmail App Password](https://myaccount.google.com/apppasswords), not your actual Gmail password — Google blocks plain-password SMTP logins by default, and an App Password limits the blast radius if it ever leaks. Add `.env` to your `.gitignore` so it's never pushed to GitHub.

**2. Fill in `birthdays.csv`** with your contacts:

```csv
name,email,month,day
Sam,sam@example.com,3,25
Jane,jane@example.com,7,14
```

**3. Write your letter templates** in `letter_templates/`, using `[NAME]` and `[SENDER NAME]` as placeholders anywhere you want personalization.

### Run it
```bash
python main.py
```

### Automate it
This script is designed to run **once per day**. A few ways to schedule it:
- **Cron** (macOS/Linux): `0 8 * * * /usr/bin/python3 /path/to/main.py` — runs daily at 8 AM
- **Task Scheduler** (Windows): create a daily trigger pointing to the script
- **GitHub Actions**: use a [`schedule`](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule) trigger with cron syntax in a workflow file to run the script daily from GitHub's own infrastructure — no local machine needs to stay on
- **PythonAnywhere**: upload the script and set up a free [Scheduled Task](https://www.pythonanywhere.com/) to run it daily — a solid option if you want it running in the cloud without managing a server

---

## 🧩 How It Works

### 1. Loading Credentials Securely
Instead of hardcoding email credentials, they're pulled from environment variables loaded via `python-dotenv` — a standard practice for keeping secrets out of source control.

```python
load_dotenv()

my_gmail = os.getenv("SMTP_GMAIL_ID")
password_gmail = os.getenv("SMTP_GMAIL_PASSWORD")

now = dt.datetime.now()
today = (now.month, now.day)
```

### 2. Checking for a Birthday Today
The CSV is loaded with `pandas`, then converted into a dictionary keyed by `(month, day)` tuples — a neat trick that turns a date lookup into an instant O(1) dictionary check instead of looping through every row.

```python
def check_birthday():
    """Checks if today is a birthday"""
    data = pd.read_csv("birthdays.csv")
    birthday_dict = {(data_row["month"], data_row["day"]): data_row for
                     (_, data_row) in data.iterrows()}

    if today in birthday_dict:
        return birthday_dict[today]
    return None
```

### 3. Personalizing & Sending the Email
A random letter template is chosen, personalized with the recipient's name, then sent over a secure TLS connection to Gmail's SMTP server. A guard clause at the top exits gracefully — printing a message instead of crashing — on any day with no matching birthday.

```python
def send_email():
    """Sends an email to the user on their birthday"""
    birthday_dict = check_birthday()

    if birthday_dict is None:
        print("No birthdays today.")
        return

    else:
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
        print(f"Email sent to {birthday_dict['name']} at "
              f"{birthday_dict['email']}")
```

---

## 📚 What This Project Demonstrates

- Automating a genuinely repetitive personal task end-to-end (data check → personalization → real delivery)
- Working with `pandas` for CSV parsing and turning tabular data into an efficient lookup structure
- Sending real emails programmatically with `smtplib` and a secure TLS handshake
- Managing secrets safely with environment variables instead of hardcoding credentials
- Designing a script to be run on a schedule (cron/Task Scheduler) rather than only on demand

---

## 🔮 Future Improvements

- [ ] Support multiple birthdays on the same day (currently only sends to one match)
- [ ] Add logging so you can confirm the script ran and what it sent, without checking your inbox
- [ ] Replace `"Divine Demon"` with a configurable sender name (via `.env` or CSV)
- [ ] Add a dry-run mode that prints the email instead of sending it, for testing template changes safely
- [ ] Add protection against sending duplicate emails if the script is accidentally run more than once on the same day

---

## 👤 Developer

**VISHAL YADAV**
- GitHub: [@VISHAL108-Mech](https://github.com/VISHAL108-Mech)
- LinkedIn: [vishal-yadav-2a91a7428](https://www.linkedin.com/in/vishal-yadav-2a91a7428)
- Email: [vy4122000@gmail.com](mailto:vy4122000@gmail.com)
