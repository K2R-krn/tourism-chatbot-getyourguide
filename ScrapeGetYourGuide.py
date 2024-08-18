from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Define a global variable to determine if application is in development more or not
DEVELOPMENT_MODE = True


def get_firefox_driver(opts):
    driver = webdriver.Firefox(
        options=opts,
        executable_path="/home/appuser/.conda/bin/geckodriver",
    )
    return driver


def get_driver(opts):
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=opts
    )


OPTIONS = Options()
OPTIONS.add_argument("--disable-gpu")

FIREFOX_OPTIONS = FirefoxOptions()
FIREFOX_OPTIONS.add_argument("--disable-gpu")
FIREFOX_OPTIONS.add_argument("--headless")


class ScrapeGetYourGuide:
    def __init__(self):
        if DEVELOPMENT_MODE:
            self.driver = get_driver(OPTIONS)
        else:
            self.driver = get_firefox_driver(FIREFOX_OPTIONS)

        self.driver.implicitly_wait(5)

    def scrape_one_trip_info(self, url: str) -> str:
        # Go to the webpage
        self.driver.get(url)

        # self.driver.implicitly_wait(10)
        res = {}

        # Get highlights
        try:
            trip_highlights = self.driver.find_element(
                By.CSS_SELECTOR, 'ul[data-test-id="activity-highlights"]'
            )
            li_elements = trip_highlights.find_elements(
                By.CSS_SELECTOR, "li.activity-highlights__list-item"
            )

            highlights = []
            for element in li_elements:
                highlights.append(element.text)

            highlight_string = "\n".join(highlights)
            res["highlights"] = highlight_string
        except Exception as e:
            print("There was an exception while getting the highlights: ", e)
            res["highlights"] = "None found"

        return res["highlights"]

    def get_response(self, url: str) -> list:
        # Got to the webpage
        self.driver.get(url)
        print("Going to url: ", url)

        # self.driver.implicitly_wait(10)

        # Find all the trips
        try:
            trips = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, ".vertical-activity-card")
                )
            )
        except Exception as e:
            print("The following exception occured: ", e)
            return [{"message": "Could not find any trips", "status": 400}]

        status = 0

        if len(trips) != 0:
            status = 200
            res = []
            for trip in trips:
                single_trip = {}
                # Get the title of the trip
                try:
                    title = trip.find_element(
                        By.CSS_SELECTOR, 'p[data-test-id="activity-card-title"]'
                    )
                    single_trip["title"] = title.text
                except Exception as e:
                    print("The following exception occured: ", e)
                    single_trip["title"] = ""

                # Get the rating of the trip
                try:
                    rating = trip.find_element(
                        By.CSS_SELECTOR, "span.rating-overall__rating-number"
                    )
                    single_trip["rating"] = rating.text
                except Exception as e:
                    print("The following exception occured: ", e)
                    single_trip["rating"] = "Not found"

                # Get the review of the trip
                try:
                    reviews = trip.find_element(
                        By.CSS_SELECTOR, "div.rating-overall__reviews span"
                    )
                    single_trip["num_reviews"] = reviews.text
                except Exception as e:
                    print("The following exception occured: ", e)
                    single_trip["num_reviews"] = "Not found"

                # Get the price of the trip
                try:
                    pricing_container = trip.find_element(
                        By.CSS_SELECTOR, "div.baseline-pricing__container"
                    )
                    pricing_value = pricing_container.find_element(
                        By.CSS_SELECTOR, "div.baseline-pricing__value"
                    )
                    pricing_category = pricing_container.find_element(
                        By.CSS_SELECTOR, "p.baseline-pricing__category"
                    )

                    single_trip["pricing_value"] = pricing_value.text
                    single_trip["pricing_category"] = pricing_category.text
                except Exception as e:
                    print("The following exception occured: ", e)
                    single_trip["pricing_value"] = "Not found"
                    single_trip["pricing_category"] = "Not found"

                # Get the href of the trip
                try:
                    trip_href = trip.find_element(
                        By.CSS_SELECTOR, "a.vertical-activity-card__container"
                    )
                    href_value = trip_href.get_attribute("href")
                    single_trip["link"] = href_value
                except Exception as e:
                    print("The following exception occured: ", e)
                    single_trip["link"] = "Not found"

                # Add in success message
                single_trip["message"] = "Success!"
                single_trip["status"] = status

                # Append to result
                res.append(single_trip)
        else:
            status = 400
            print("No trips were found")
            return [{"status": status, "message": "Could not find any trips"}]

        # if status == 200:
        #     for trip in tqdm(res):
        #         if trip["link"] != "Not found":
        #             try:
        #                 self.driver.implicitly_wait(2)
        #                 highlights = self.scrape_one_trip_info(trip["link"])
        #                 trip["highlights"] = highlights
        #             except Exception as e:
        #                 print("An exception occurred executing this function: ", e)
        #                 trip["highlights"] = "Not found"

        return res


def get_getyourguide_trips(links: list) -> list:
    """
    Take as an input a list of urls of getyourguide pages and returns all
    the available trips
    :param links: urls of getyourguide pages
    :return: list og trips
    """
    res = []
    scraper = ScrapeGetYourGuide()
    for url in links:
        trips = scraper.get_response(url)
        res.extend(trips)

    return res
