from dataclasses import dataclass
from bs4 import BeautifulSoup
import requests
import json


@dataclass
class Parser:
    website: str  # url to visit
    soup_tag: str  # html tag to extract links
    next_page: str  # next page url 
    starts_with: str  # useful links starts similar
    page_limit: int = 5  # default limit page to search

    def extract_links(self):
        page_number = 0
        data = {}
        data['link_list'] = []
        while page_number < self.page_limit:
            if page_number == 0:
                # first page should not have the next_page on the url
                url = self.website
            else:
                url = self.website + self.next_page + str(page_number)
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'html.parser')
            # get all the links from the page in <soup_tag /> tags
            links = soup.find_all(self.soup_tag)
            for link in links:
                url = link.get('href')
                if url.startswith(self.starts_with):
                    data['link_list'].append({
                        'id': hash(url),  # noqa The id will allow us know if we have already seen this link 
                        'url': url,
                    })
            page_number += 1

        with open('page.txt', 'w') as outfile:
            json.dump(data, outfile)

        return True
