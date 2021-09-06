"""
File to retrieve ACCESS_TOKENS from Zerodha
"""
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from urllib.parse import urlparse, parse_qs
from kiteconnect import KiteConnect
from pyvirtualdisplay import Display
from dotenv import load_dotenv
import time
import os
# load env vars
load_dotenv()

# set webdriver location from env file
WEBDRIVER_LOCATION = os.getenv("WEBDRIVER_LOCATION")

# make a virtual display for docker
display = Display(visible=0, size=(800, 600))
display.start()

def get_token(api_key, api_key_secret, username, password, pin):
    """
    Returns an access token for a given API key, Username, Password, and pin
    """
    # use chrome, and set default options
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "normal"
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")

    # make the chrome driver using options and webdriver location
    driver = webdriver.Chrome(
        executable_path=WEBDRIVER_LOCATION,
        options=options,
        desired_capabilities=caps,
    )

    # navigate to the login page, and send user id and password
    driver.get(f"https://kite.zerodha.com/connect/login?v=3&api_key={api_key}")
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="userid"]').send_keys(username)
    driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)
    driver.find_element_by_xpath(
        '//*[@id="container"]/div/div/div/form/div[4]/button'
    ).click()

    # wait for a second to validate and then send pin
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="pin"]').send_keys(pin)
    driver.find_element_by_xpath(
        '//*[@id="container"]/div/div/div[2]/form/div[3]/button'
    ).click()

    # wait for a while, then grab the current url
    time.sleep(0.5)
    url = driver.current_url

    # generate a kite session, after grabbing the request_token from the url
    kite = KiteConnect(api_key=api_key)
    data = kite.generate_session(
        str(parse_qs(urlparse(url).query)["request_token"][0]),
        api_secret=api_key_secret,
    )

    # return the access token
    return data["access_token"]