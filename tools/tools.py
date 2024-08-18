from ScrapeGoogle import get_getyourguide_link
from ScrapeGetYourGuide import get_getyourguide_trips
import json


def get_destination_tourism_info(destination: str):
    """
    Gets all the information about all the available tourist activities
    in that particular destination.
    :param destination:
    :return:
    """
    query = "getyourguide" + " " + destination
    destination_link = get_getyourguide_link(query)
    trips = get_getyourguide_trips(destination_link)

    output = json.dumps(trips, indent=5)

    return output
