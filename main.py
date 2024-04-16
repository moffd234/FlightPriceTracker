import os
import smtplib
import flight_data
from data_manager import DataManager
from dotenv import find_dotenv, load_dotenv
from notification_manager import NotificationManager

dotenv_path = find_dotenv()  # Finds the .env file path
load_dotenv(dotenv_path)  # loads the .env file from the path found above

EMAIL_KEY = os.getenv("EMAIL_KEY")
GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
GMAIL_SMTP = os.getenv("GMAIL_SMTP")

nm = NotificationManager()
fl_data = flight_data.FlightData()
dm = DataManager()


def find_codes():
    sheet_fields = dm.read_fields("prices")

    index = 2  # Keeps track of the row to edit
    for row in sheet_fields:
        city = row["city"]
        location_info = fl_data.format_location_search(location=city)
        params = {
            "prices": {
                "iataCode": location_info["code"]
            }
        }
        dm.edit_fields(row=index, params=params)
        index += 1


def check_prices():
    price_fields = dm.read_fields("prices")  # Gets all the fields in the "prices" Google Sheet
    email_list = dm.read_fields(page="users")  # Gets all the fields in the "users" Google Sheet
    p_row = 2  # Keeps track of the row starting at two since that is the first row with a city
    for row in price_fields:
        city = row["iataCode"]  # Gets the IATA code for the city in the row
        price = row["lowestPrice"]  # Gets the target price from the row

        data = fl_data.format_city_request(city)  # Finds best price available for the next 6 months
        if data:
            print(f"BEST PRICE FOR {city}= {data['price']}")
            if data['price'] < price:
                u_row = 2  # keeps track of the row in the user sheet
                for user in email_list:
                    # nm.send_message(data) # Sends text alert of the low price
                    email = user["email"]
                    name = f"{user['firstName']} {user['lastName']}"
                    city = row['city']
                    send_emails(name=name, email=email, data=data, city=city)
                    u_row += 1

        p_row += 1


def get_input():
    if input("Would you like to create an account? yes/no ") == "yes":
        f_name = input("\nWhat is your first name ")
        l_name = input("\nWhat is your last name ")
        email = input("\nWhat is your email address ")
        confirm_address = input("\nPlease re-enter your email address ")
        while email != confirm_address:
            print("Those emails do not match ")
            email = input("\nWhat is your email address ")
            confirm_address = input("\nPlease re-enter your email address ")
        params = {
            "user": {
                "email": email,
                "firstName": f_name,
                "lastName": l_name,
            }}
        dm.add_fields(params=params)


def send_emails(name, email, city, data):
    email_contents = \
        f"Good Morning {name},\n We have found an amazing price from PHL to {city} on " \
        f"{data['local_departure']} for only ${data['price']}"
    with smtplib.SMTP(GMAIL_SMTP, port=587) as connection:
        connection.starttls()  # Starts secure transfer
        connection.login(user=GMAIL_ADDRESS, password=EMAIL_KEY)  # Logins to mail provider
        connection.sendmail(from_addr=GMAIL_ADDRESS, to_addrs=email,
                            msg=f"Subject: LOW PRICE ON A FLIGHT TO {city}"
                                f"\n\n{email_contents}")
        connection.getreply()


check_prices()
