import requests
from bs4 import BeautifulSoup
from config import START_IMG

HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0',
           'accept': '*/*'}


async def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


async def pars(URL):
    html = await get_html(URL)
    if html.status_code == 200:
        soup = BeautifulSoup(html.text, 'html.parser')
        name = soup.find('div', class_="b-post__title").text[1:]
        full = soup.find('table', class_="b-post__info")
        info = full.findAll('tr')
        full_info = info[0].findAll('td')
        scope = full_info[1].findAll('span')
        img_ = soup.find('div', class_='b-sidecover')
        img = img_.find('a').get('href')
        for i in info:
            if i.text[0:12] == ' Дата выхода':
                data = i.text[14:]
            if i.text[0:7] == ' Страна':
                country = i.text[9:]
            if i.text[0:5] == ' Жанр':
                genre = i.text[7:]
        try:
            films_data = [img, name, scope[0].text + ' ' + scope[2].text, country, data, genre, URL]
        except:
            films_data = [img, name, scope[0].text, country, data, genre, URL]
        return films_data
    else:
        films_data = [START_IMG, 'name', 'scope', 'country', 'data', 'genre', 'URL']
        return films_data

