from bs4 import BeautifulSoup
import urllib2
import re
import time

class DaftPropertyUrlScraper:

    def __init__(self, county, filename, is_rental):
        self.filename = filename
        self.file_handle = open(filename, "w")

        self.daft_base_url = daftBaseUrl = "" \
                                           ""
        self.error_pattern = '<h1>No results</h1>'
        self.offset = 0

    def action(self):

        start = time.time()

        while(True):
            daftUrl = self.daft_base_url + str(self.offset)
            dublinPropertiesHtml = urllib2.urlopen(daftUrl).read()

            if re.search(self.error_pattern, dublinPropertiesHtml, flags = 0):
                print('breaking')
                break;

            soup = BeautifulSoup(dublinPropertiesHtml)
            anchorTags = soup.find_all('span', {'class' : 'sr_counter'})

            for tag in anchorTags:
                tag = tag.next_sibling.next_sibling
                href = tag['href']
                self.file_handle.write(href)
                self.file_handle.write('\n')


            self.offset = self.offset + 10
            print(self.offset)

        self.file_handle.close()

        end = time.time()

        print(end - start)



scraper = DaftPropertyUrlScraper('dublin', 'property_urls.txt')
scraper.action()