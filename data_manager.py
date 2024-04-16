import os
import requests
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()  # Finds the .env file path
load_dotenv(dotenv_path)  # loads the .env file from the path found above

SHEETY_KEY = os.getenv("SHEETY_KEY")
SHEET_NAME = os.getenv("SHEET_NAME")
SHEETY_URL = f"https://api.sheety.co/{SHEET_NAME}/flightDeals/"


class DataManager:
    """
    DataManager class is responsible for interacting with the Google Sheet using the Sheety API.

    Attributes:
        sheety_header (dict): A dictionary containing the headers to be used for API requests.
            It includes the Authorization header with the Sheety API key and Content-Type header as "application/json."

    Methods:
        read_fields(): Fetches and retrieves all rows from the Google Sheet using the Sheety API.
            Returns:
                list: A list of dictionaries containing the rows' data fetched from the Google Sheet.

        edit_fields(row, field, value): Edits a specific field in a row of the Google Sheet using the Sheety API.
            Args:
                row (int): The row number (object ID) of the row to be edited.
                field (str): The name of the field (column) in the Google Sheet to be updated.
                value (str): The new value to be set for the specified field.

    Usage:
        # Instantiate the DataManager class
        data_manager = DataManager()

        # Fetch and retrieve all rows from the Google Sheet
        all_rows = data_manager.read_fields()
        print(all_rows)

        # Edit a specific field in a row of the Google Sheet
        data_manager.edit_fields(row=2, field="City", value="New City")
    """

    def __init__(self):
        self.sheety_header = {
            "Authorization": f"Bearer {SHEETY_KEY}",
            "Content-Type": "application/json"
        }

    def read_fields(self, page) -> list:
        """
        Fetches and retrieves all rows from the Google Sheet using the Sheety API.

        Returns:
            list: A list of dictionaries containing the rows' data fetched from the Google Sheet.
        """
        response = requests.get(url=f'{SHEETY_URL}{page}', headers=self.sheety_header)
        response.raise_for_status()
        return response.json()[page]

    def edit_fields(self, row, params: dict):
        """
        Edits a specific field in a row of the Google Sheet using the Sheety API.

        Args:
            row (int): The row number (object ID) of the row to be edited.
            params (dict): A dictionary containing the fields to edited along with the new values
        """
        page = next(iter(params))
        url = f"https://api.sheety.co/{SHEET_NAME}/flightDeals/{page}/{row}"
        sheety_response = requests.put(url=url, json=params, headers=self.sheety_header)
        print(sheety_response.text)
        sheety_response.raise_for_status()


    def add_fields(self, params):
        page = next(iter(params))
        url = f"https://api.sheety.co/{SHEET_NAME}/flightDeals/users"
        sheety_response = requests.post(url=url, json=params, headers=self.sheety_header)
        print(sheety_response.text)
        sheety_response.raise_for_status()

