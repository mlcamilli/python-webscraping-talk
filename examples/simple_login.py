import requests
import os
import json
from bs4 import BeautifulSoup
from . import get_redis


username = 'matt@trackmaven.com'
password = os.environ.get('MEETUP_PW')


def login():
    login_url = 'https://secure.meetup.com/login/'
    session = requests.Session()
    response = session.get(login_url)
    soup = BeautifulSoup(response.content, "html5lib")
    login_form = soup.find(id='loginForm')
    token = login_form.find('input', attrs={'name': 'token'}).attrs['value']

    form_data = {
        'email': username,
        'password': password,
        'token': token,
        'op': 'login',
        'submitButton': 'Log in'
    }
    login_response = session.post(login_url, data=form_data)
    assert login_response.url == 'http://www.meetup.com/'
    redis = get_redis()
    redis.set('meetup', json.dumps(session.cookies.get_dict()))
    return session


def visit():
    session = requests.Session()
    redis = get_redis()
    cookies = json.loads(redis.get('meetup'))
    session.cookies.update(cookies)
    response = session.get('http://www.meetup.com')
    soup = BeautifulSoup(response.content, "html5lib")
    login_link = soup.find('a',
                           attrs={'href': "https://secure.meetup.com/login/"})
    assert login_link is None
    return session
