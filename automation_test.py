"""
Author: Joe Casper
Email: josephcasperjr@gmail.com
"""

import json
import os
import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def main():
    """
    Tests logging in to the Dexcom website
    """
    constants = json.load(open(os.path.join(os.path.dirname(__file__), "constants.json")))

    # Init webdriver and go to homepage
    browser = webdriver.Firefox()
    browser.get(constants['DEXCOM_URL'])
    assert browser.title == 'Dexcom Clarity'

    # On homepage
    btn_home_users = _get_element(browser, By.LINK_TEXT, 'Dexcom Clarity for Home Users')
    btn_home_users.click()

    # On login page
    input_username = _get_element(browser, By.ID, 'username')
    input_password = _get_element(browser, By.ID, 'password')
    btn_login = _get_element(browser, By.NAME, 'op')

    WebDriverWait(browser, 10).until(EC.element_to_be_clickable(input_username))

    input_username.send_keys(constants['USERNAME'])
    input_password.send_keys(constants['PASSWORD'])
    btn_login.click()


def _get_element(browser, by, selector):
    """
    Find an element and assert that that element was found. Used instead of browser.find_element() as that throws a
    NoSuchElementException if no element is found, and I'd rather it fail the test through an assertion so that
    it can be caught by pytest and be reported correctly

    :param browser: WebDriver browser object
    :param by: Method to find the selector
    :param selector: The string being used to find the element
    :return: an HTML element
    """
    element = browser.find_elements(by, selector)
    assert len(element) > 0, f'Element {selector} not found by {by}'
    return element[0]


main()
