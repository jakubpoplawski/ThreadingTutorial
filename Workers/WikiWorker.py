import requests
from bs4 import BeautifulSoup


class WikiWorker():
    def __init__(self):
        self.url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

    @staticmethod
    def extract_companies(page_html):
        soup = BeautifulSoup(page_html, 'lxml')
        table = soup.find(id='constituents')
        table_rows = table.find_all('tr')
        for table_row in table_rows[1:]:
            symbol = table_row.find('td').text.strip('\n')
            yield symbol

    def get_companies(self):
        response = requests.get(self.url)
        if response.status_code != 200:
            print('Page unavailable.')
            return []
        else:
            yield from self.extract_companies(response.text)



