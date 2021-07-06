from dataclasses import dataclass
from bs4 import BeautifulSoup
import requests
import json


@dataclass
class Parser:
    website: str  # url to visit
    soup_tag: str  # html tag to extract links
    next_page_path: str  # next page url
    starts_with: str  # useful links starts similar
    page_limit: int = 5  # default limit page to search
    next_page_index: int = 1

    def get_link_data(self, link):
        page = requests.get(link)
        soup = BeautifulSoup(page.text, 'html.parser')
        # This is currently working on MeliProps only
        # Need refactor for argenprops
        price = soup.find('span', class_='price-tag-fraction').get_text()
        coin = soup.find('span', class_='price-tag-symbol').get_text()
        return [coin, price]

    def url_search_list(self):
        next_pages = [self.website]
        # refactor names
        page_args = self.next_page_path
        index = self.next_page_index + 1
        i = 0

        while i < self.page_limit:
            next_pages.append(self.website + page_args + str(index))
            index = index + self.next_page_index
            i += 1

        return next_pages

    def extract_links(self):
        data = {}
        data['link_list'] = []
        pages = self.url_search_list()

        for url in pages:
            print('parsing for ', url)
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'html.parser')
            # get all the links from the page in <soup_tag /> tags
            links = soup.find_all(self.soup_tag)
            outfile = open('data.json', 'w')
            dict1 = {}
            for link in links:
                current_url = link.get('href')
                try:
                    if current_url.startswith(self.starts_with):
                        link_data = self.get_link_data(current_url)
                        dict1[hash(current_url)] = {
                                'url': current_url,
                                'coin': link_data[0],
                                'price': link_data[1],
                                }
                        print("--", current_url)
                except: # noqa
                    pass
            json.dump(dict1, outfile)


@dataclass
class Parser_Zonaprops:
    website: str
    soup_tag: str  # html tag to extract links
    page_limit: int = 5  # default limit page to search
    zona: str = 'capital-federal.html'
    next_page_tag: str = '-pagina-'

    def url_search_list(self):
        pages = [self.website + '-q-' + self.zona]
        i = 2
        while i < self.page_limit:
            page = (self.website + self.next_page_tag + str(i) + '-q-' + self.zona) # noqa
            pages.append(page)
            i += 1
        return pages

    def extract_links(self):
        data = {}
        data['link_list'] = []
        pages = self.url_search_list()

        for url in pages:
            print('parsing ', url)
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'html.parser')
            # get all the links from the page in <soup_tag /> tags
            links = soup.find_all('div') # noqa
            print(links)
            print("flag")
            # for link in links:
            #    current_url = link
            #    try:
            #        print(current_url)
            #    except: # noqa
            #        pass
