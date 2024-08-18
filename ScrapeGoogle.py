from bs4 import BeautifulSoup
import requests

GOOGLE_LINK = "https://www.google.com/search?"


class GoogleScraper:
    def __init__(self, url: str):
        self.url = url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
        }
        self.response = requests.get(self.url, headers=self.headers)

    def get_response(self) -> list:
        soup = BeautifulSoup(self.response.text, "html.parser")
        results = []

        for result in soup.find_all("div", class_="g"):
            link = result.find("a")
            title = link.text
            url = link["href"]

            results.append({"title": title, "url": url})

        return results


def get_getyourguide_link(search_query: str) -> list:
    """
    Takes in the search query and gets all the get_your_guide link for the qeury
    :param search_query: search words
    :return: viator link
    """
    # Format the words
    words = search_query.split()
    mod_query = "+".join(words)

    # Make the google link
    google_link = GOOGLE_LINK + f"q={mod_query}"

    # Initialize the GoogleScraper class
    google_scraper = GoogleScraper(google_link)

    # Get all the results from the google page
    google_results = google_scraper.get_response()

    # Get all the links from viator
    links = []
    for result in google_results:
        result_url = result["url"]
        if "getyourguide.com" in result_url:
            links.append(result_url)

    # Return all the viator links
    return links
