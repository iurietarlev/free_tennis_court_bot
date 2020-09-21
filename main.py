from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options

from easydict import EasyDict
import argparse
import yaml
import requests
import random
import calendar


free_days = {"Monday": False, "Tuesday": False, "Wednesday": False,
             "Thursday": False, "Friday": False, "Saturday": False, "Sunday": False}


def telegram_bot_sendtext(bot_message, bot_token, bot_chatID):
    send_text = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={bot_chatID}&parse_mode=Markdown&text={bot_message}'
    response = requests.get(send_text)
    return response.json()


def get_arguments():
    """
    Parse input arguments
    """
    parser = argparse.ArgumentParser(
        description="Code for Checking Tennis Court Cancellations")
    parser.add_argument('--cfg', type=str, default=None,
                        help='compulsory config file',)
    return parser.parse_args()


def yaml_load(file_path):
    with open(file_path, 'r') as f:
        return yaml.load(f)
    f.close()


def cfg_from_file(file_path):
    return EasyDict(yaml_load(file_path))


def check_next_day(driver, index):
    try:
        if index != 0:
            next_day = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.LINK_TEXT, "Next Day")))
            next_day.click()

        # TODO: replace time.sleep with conditional waits from WebDriverWait (not working atm)
        time.sleep(2)  # temp solution
        date = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "h2.pull-left"))
        ).text

        element = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located(
                (By.XPATH, "//span[.='Free']"))
        )
        return True, date

    except:
        return False, date


def login(driver, username, password):
    sign_in = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(
            (By.LINK_TEXT, "Sign in")))
    sign_in.click()

    email = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (By.ID, "EmailAddress")))
    email.send_keys(username)

    pswd = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (By.ID, "Password")))
    pswd.send_keys(password)

    driver.find_element_by_id("signin-btn").click()


def main():
    args = get_arguments()
    cfg = cfg_from_file(args.cfg)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")

    # for headless pass in the chrome_options
    driver = webdriver.Chrome(  # options=chrome_options,
        executable_path=cfg.CHROME_DRIVER_PATH)
    driver.get(cfg.URL)

    login(driver, cfg.USERNAME, cfg.PASSWORD)
    while True:  # busy waiting
        # go through the next 7 days of booking sheets
        for i in range(7):
            available, date = check_next_day(driver, i)
            day = date.split(" ")[0]

            # send message of availability
            if available and not free_days[day]:
                free_days[day] = True
                telegram_bot_sendtext(f"Free court on {date}",
                                      cfg.TELEGRAM_BOT_TOKEN, cfg.TELEGRAM_BOT_CHAT_ID)

            # send message of apparent inavailability
            if not available and free_days[day]:
                free_days[day] = False
                telegram_bot_sendtext(f"Free court on {date} has just been taken.",
                                      cfg.TELEGRAM_BOT_TOKEN, cfg.TELEGRAM_BOT_CHAT_ID)

        # scroll back through the pages
        for i in range(6):
            driver.back()
            time.sleep(random.randrange(1, 3))
        time.sleep(random.randrange(1, 10))

    driver.quit()


if __name__ == '__main__':
    main()
