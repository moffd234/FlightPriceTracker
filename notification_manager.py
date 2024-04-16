import os
from dotenv import load_dotenv, find_dotenv
from twilio.rest import Client

dotenv_path = find_dotenv()  # Finds the .env file path
load_dotenv(dotenv_path)  # loads the .env file from the path found above


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.phone_number = os.getenv("PHONE_NUMBER")
        twilio_auth = os.getenv("AUTH_TOKEN")
        twilio_sid = os.getenv("ACCOUNT_SID")
        self.twilio_client = Client(twilio_sid, twilio_auth)

    def send_message(self, data: dict):
        message = self.twilio_client.messages.create(
            from_=self.phone_number,
            body=f"Low price alert! Only ${data['price']} to fly from {data['from_city']} to {data['to_city']}"
                 f" on {data['local_departure']}",
            to='+13029324622'
        )
        print(message.status)
