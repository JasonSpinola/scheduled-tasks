import smtplib
import datetime as dt
import pandas as pd
from random import choice
import os

# import os and use it to get the Github repository secrets
MY_EMAIL_HOST = os.environ.get("MY_EMAIL_HOST")
MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")

# Get today's date information
time = dt.datetime.now()
day = time.day
month = time.month
year = time.year
date = f"{int(day)}/{int(month)}"

# Template Paths
templates = ["letter_templates/letter_1.txt",
             "letter_templates/letter_2.txt",
             "letter_templates/letter_3.txt"]

# Get birthday CSV data
birthday_data = pd.read_csv("birthdays.csv")
birthday_dict = birthday_data.to_dict()
num_of_checks = len(birthday_dict["Name"])

# Choose a random template
template_choice = choice(templates)
with open(template_choice, "r") as template:
    template_str = template.read()

for person in range(num_of_checks):
    # Checking each person to see if their birthday is today
    persons_birthday = f"{birthday_dict["Day"][person]}/{birthday_dict["Month"][person]}"

    # Condition to action if date matches
    if persons_birthday == date:

        name = birthday_dict["Name"][person]
        new_email = template_str.replace("[NAME]", name)
        too_address = birthday_dict["Email"][person]

        with smtplib.SMTP_SSL(host=MY_EMAIL_HOST, timeout=30, port=465) as connection:
            # connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=too_address,
                msg=f"Subject: Happy Birthday!\n\n{new_email}")
