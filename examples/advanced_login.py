from headless_browser import FirefoxScraper
from . import get_redis
import os
import json

email = 'matt@trackmaven.com'
pw = os.environ.get('AIRBNB_PW')


def login():
    scraper = FirefoxScraper()
    scraper.get('http://www.airbnb.com/')
    scraper.browser.implicitly_wait(10)
    login_button = scraper.browser.find_element_by_link_text('Log In')
    login_button.click()
    scraper.by_id('signin_email').send_keys(email)
    scraper.by_id('signin_password').send_keys(pw)
    scraper.by_id('user-login-btn').submit()
    redis = get_redis()
    redis.set('airbnb', json.dumps(scraper.browser.get_cookies()))
    return scraper


def visit():
    scraper = FirefoxScraper()
    redis = get_redis()
    cookies = json.loads(redis.get('airbnb'))
    scraper.get('http://www.airbnb.com/')
    scraper.browser.delete_all_cookies()
    for cookie in cookies:
        scraper.browser.add_cookie(cookie)
    scraper.browser.refresh()
    return scraper
