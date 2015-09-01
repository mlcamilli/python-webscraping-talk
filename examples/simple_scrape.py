import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse


def scrape():
    page = requests.get('http://www.930.com/concerts')
    soup = BeautifulSoup(page.content, 'html5lib')
    concerts = soup.find_all('div', attrs={'class': 'list-view-item'})
    data = []
    for concert in concerts:
        item = {}
        try:
            item['artist'] = concert.h1.text.split(':')[0].replace(
                '(NEW DATE)', '').strip()
            date_str = concert.find('h2', attrs={'class': 'dates'}).text
            time_str = concert.find(
                'h2', attrs={'class': 'times'}).text.replace(
                'Doors:', '').strip()
            item['time'] = parse('{} {}'.format(date_str, time_str))
            item['link'] = concert.h3.a.attrs['href']
            item['sold_out'] = concert.h3.a.text != 'Tickets'
            data.append(item)
        except:
            continue
    return data
