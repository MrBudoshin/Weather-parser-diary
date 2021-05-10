import requests
from bs4 import BeautifulSoup


class Wezer:

    def __init__(self, begin_date, month):
        self.db_date = {}
        self.begin_date = int(begin_date)
        self.month = month

    def get_day_weather(self, param):
        response = requests.get(
            f'https://darksky.net/details/55.7616,37.6095/2020-{self.month}-{param}/si12/en')
        html_doc = BeautifulSoup(response.text, features='html.parser')
        list_day = html_doc.find_all('div', {'class': "date"})
        list_weather = html_doc.find_all('p', {'id': "summary"})
        list_temp = html_doc.find_all('span', {'class': "temp"})
        return {'date': list_day[0].text, 'state': list_weather[0].text, 'temperature': list_temp[0].text}

    def get_weather(self, end_date):
        for days in range(self.begin_date, int(end_date) + 1):
            day_weather = self.get_day_weather(param=days)
            self.db_date[days] = day_weather
        return self.db_date


if __name__ == '__main__':

    wz = Wezer(begin_date=20, month=12)
    a = wz.get_weather(22)
    print(a)