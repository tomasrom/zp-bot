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
            outfile = open('data.txt', 'w')
            for link in links:
                current_url = link.get('href')
                try:
                    if current_url.startswith(self.starts_with):
                        data['link_list'].append({
                            'id': hash(current_url),  # noqa The id will allow us know if we have already seen this link 
                            'url': current_url,
                        })
                        print("--", current_url)
                        json.dump(data, outfile)
                except: # noqa
                    pass

