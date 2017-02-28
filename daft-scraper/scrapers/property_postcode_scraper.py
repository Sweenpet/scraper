from bs4 import BeautifulSoup
import urllib2
import re
import time
import os

class DaftPostcodeScraper:

    def __init__(self, output_directory):

        self.output_directory = output_directory
        self.postcodes = ['1','2','3','4','5','6','6w','7','8','9','10','11','12','13','14','15','16','17','18','20','22','24']
        self.error_pattern = '<h1>No results</h1>'

        if not os.path.isdir(output_directory):
            os.mkdir(output_directory)

    def action(self):
        start = time.time()

        for pcn in self.postcodes:

          postcode = "dublin-" + pcn
          daftBaseUrl = "http://www.daft.ie/dublin/property-for-sale/" + postcode + "/?offset="

          print(postcode)

          f = open(self.output_directory + postcode + ".txt", "w")

          offset = 0

          while True:
            daft_url = daftBaseUrl + str(offset)
            dublin_properties_html = urllib2.urlopen(daft_url).read()

            if re.search(self.error_pattern, dublin_properties_html, flags = 0):
              print('breaking')
              break

            soup = BeautifulSoup(dublin_properties_html, "html.parser")
            anchorTags = soup.find_all('span', {'class' : 'sr_counter'})

            for tag in anchorTags:
              tag = tag.next_sibling.next_sibling
              href = tag['href']
              f.write(href)
              f.write('\n')

            offset += 10

          f.close()
        end = time.time()
        print(end - start)



scraper = DaftPostcodeScraper("/home/peter/Projects/DaftScraper/PropertyUrls/")
scraper.action()