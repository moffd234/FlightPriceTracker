import datetime

from flight_search import FlightSearch


class FlightData:
    # This class is responsible for structuring the flight data.
    def __init__(self):
        self.fl = FlightSearch()

    def format_location_search(self, location) -> dict:
        """
        Calls the fl.make_city_request() to get city a city request from the tequila API then formats the data
        :param location: Location of the city being searched
        :return: A dict containing the location's type, name, and code
        """
        # Makes a location request with Tequila and returns response.json
        response = self.fl.make_location_request(location=location)

        location_type = "city"
        location_name = response["locations"][0]["name"].lower()
        code = response["locations"][0]["code"]

        return {"type": location_type, "location name": location_name, "code": code}

    def format_city_request(self, location):
        data: dict = self.fl.make_city_request(location)

        if data is None:
            print(f"No available data for location {location}")
            return None

        # Covert the departure dates to MM, DD, YYYY
        local_departure_str = data["local_departure"]
        date_obj = datetime.datetime.fromisoformat(local_departure_str[:-1])
        formatted_departure = date_obj.strftime("%m/%d/%y")

        formatted_data = {
            "price": data["price"],
            "from_city": data["flyFrom"],
            "to_city": data["cityTo"],
            "depart_date": data["local_departure"],
            "local_departure": formatted_departure
        }
        return formatted_data
