import os
import requests
import datetime
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()  # Finds the .env file path
load_dotenv(dotenv_path)  # loads the .env file from the path found above

API_KEY = os.getenv("TEQUILA_KEY")
TEQUILA_URL = "https://api.tequila.kiwi.com/"


class FlightSearch:
    """
    FlightSearch class is responsible for interacting with the Flight Search API provided by Tequila Kiwi.

    Attributes:
        location_type (str): The type of location to search for (e.g., "city").
        header (dict): A dictionary containing the headers to be used in the API request.
            It includes the "apikey" header with the API key for authentication.

    Methods:
        make_city_request(): Makes a location query request to the Flight Search API.
            Returns:
                dict: A dictionary containing the response data in JSON format from the API.

    Usage:
        # Instantiate the FlightSearch class with the desired location
        flight_search = FlightSearch(location="Paris")

        # Make a location query request to the Flight Search API
        location_info = flight_search.make_city_request()
        print(location_info)
    """

    def __init__(self):
        """
        Initializes the FlightSearch class with the given location.

        """
        self.location_type = "city"

        self.header = {
            "apikey": API_KEY,
        }

    def make_location_request(self, location):
        """
        Makes a location query request to the Flight Search API.

        Returns:
            dict: A dictionary containing the response data in JSON format from the API.
        """

        location_url = f"{TEQUILA_URL}locations/query"
        params = {
            "term": location,
            "locale": "en-US",
            "location_types": self.location_type
        }
        response = requests.get(url=location_url, params=params, headers=self.header)
        response.raise_for_status()
        return response.json()

    def make_city_request(self, location):
        now = datetime.date.today()
        today_date_string = now.strftime('%d/%m/%Y')
        six_months_later = now + datetime.timedelta(days=6*30)
        six_months_later_string = six_months_later.strftime("%d/%m/%Y")

        params = {
            "fly_from": "PHL",
            "fly_to": location,
            "date_from": today_date_string,  # Starting departure date (dd/mm/yyyy)
            "date_to": six_months_later_string, # Ending departure date (dd/mm/yyyy)
            "ret_from_diff_city": "false",
            "ret_to_diff_city": "false",
            "adults": 1,
            "curr": "USD",
            "locale": "en",  # Sets language in response
            "vehicle_type": "aircraft",
            "limit integer": 5,
            "sort": "price"
            # "price_to": <INSERT PRICE> THIS SETS THE MAX PRICE TO LOOK FOR
        }

        city_url = f"{TEQUILA_URL}v2/search"
        response = requests.get(url=city_url, params=params, headers=self.header)
        response.raise_for_status()
        data = response.json()

        # Check if there are flights available in the response
        if "data" in data and len(data["data"]) > 0:
            # Extract the first two flights from the response
            first_flight = data["data"][0]
            return first_flight

        else:
            return None
