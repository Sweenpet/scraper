from bs4 import BeautifulSoup
from domain import HousePatterns, HouseDetails
import urllib2
import re

class DaftPropertyScraper:

    def __init__(self, repo):
        """
        :type repo:DaftRepo
        """
        self.base_url = "http://www.daft.ie"
        self.repo = repo

    def action(self):

        url_count = self.repo.get_house_url_count().fetchone()
        house_urls = self.repo.select_all_house_urls()

        print("---------------------------------------")
        print("Scraping " + str(url_count[0]) + " pages" )
        print("---------------------------------------")

        for house_url in house_urls:
            postcode = house_url.postcode
            house_details = HouseDetails()
            url = self.base_url + house_url.url
            req = urllib2.Request(url)

            try:
                propertyHtml = urllib2.urlopen(req).read()

                longitudeMatch = re.search(HousePatterns.longitude, propertyHtml, flags = 0)
                if longitudeMatch:
                    house_details.lon = longitudeMatch.group(1)

                latitudeMatch = re.search(HousePatterns.latitude, propertyHtml, flags = 0)
                if latitudeMatch:
                    house_details.lat = latitudeMatch.group(1)

                areaMatch = re.search(HousePatterns.floor_area, propertyHtml, flags = 0)
                if areaMatch:
                    house_details.floor_area = areaMatch.group(1)

                energyMatch = re.search(HousePatterns.energy, propertyHtml, flags = 0)
                if energyMatch:
                    house_details.energy_performance = energyMatch.group(1)

                energyRatingMatch = re.search(HousePatterns.energy_rating, propertyHtml, flags = 0)
                if energyRatingMatch:
                    house_details.energy_rating = "BER " + energyRatingMatch.group(1)

                berNumberMatch = re.search(HousePatterns.ber_number, propertyHtml, flags=0)
                if berNumberMatch:
                    house_details.ber_number = berNumberMatch.group(1)

                description_match = re.search(HousePatterns.description, propertyHtml, flags=0)
                if description_match:
                    house_details.description = description_match
                    house_details.description = house_details.description.replace('<br>','').replace('<p>','')

                locality = house_url.url.split('/')
                house_details.location = locality[3]

                soup = BeautifulSoup(propertyHtml, "html.parser")

                houseSummaryElement = soup.find('div', { 'id':'smi-summary-items'})

                if (houseSummaryElement == None):
                    print ('could not find house summary')
                    continue

                childNodes = houseSummaryElement.findChildren()

                innerText = childNodes[0].text
                priceMatch = re.search(HousePatterns.price, innerText, flags = 0)
                if priceMatch:
                    house_details.price = priceMatch.group(1)

                subsets = house_details.price.split(',')
                textPrice = ""

                for t in subsets:
                    textPrice = textPrice + t

                house_details.price = textPrice

                text = houseSummaryElement.text

                houseMatch = re.search(HousePatterns.house, text, flags = 0)
                if (houseMatch):
                    house_details.house_type = houseMatch.group(1)

                bedsMatch = re.search(HousePatterns.beds, text, flags = 0)
                if (bedsMatch):
                    house_details.beds = bedsMatch.group(1)

                bathsMatch = re.search(HousePatterns.baths, text, flags = 0)
                if (bathsMatch):
                    house_details.baths = bathsMatch.group(1)

                house_details.url_id = house_url.id

                self.repo.insert_into_house_details(house_details)
            except:
             print('error')

        def __get_house_type(self, house_name)
