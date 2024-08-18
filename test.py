# from ScrapeGoogle import get_getyourguide_link
# from ScrapeGetYourGuide import get_getyourguide_trips
# import json
#
#
# getyourguide_links = get_getyourguide_link("getyourguide Barcelona")
# getyourguide_trips = get_getyourguide_trips(getyourguide_links)
#
# output = json.dumps(getyourguide_trips, indent=5)
#
# print(output)

# Steps:
# 1. The user can enter absolutely anything they want, so
#    step 1 is to figure out if it is a travel question or not.

# 2. If not a travel question, pretty straight forward,
#    if it is a travel question, figure out where the user wants to travel

# 3. Get all

import configparser
from helpers.helpers import (
    find_question_type,
    answer_non_travel_question,
    get_destination,
)
import os
from agents.destination_info import get_destination_data

config = configparser.ConfigParser()
config.read("config.ini")

OPENAI_API_KEY = config.get("API", "OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

question = "I want to go to Ireland. Can you show me some of the things I can do there?"

# Given the question find out if it is a travel and tourism related question or something else:
is_travel_question = find_question_type(question)
# is_travel_question is True if it is a travel question, false otherwise

if not is_travel_question:
    answer = answer_non_travel_question(question)
    print(answer)
else:
    travel_question_answer = get_destination(question)
    if "false__no_destination" in travel_question_answer:
        ans = answer_non_travel_question(question)
        print(ans)
    else:
        destination = travel_question_answer
        destination_data = get_destination_data(
            destination=destination, question=question
        )
        print(destination_data)
