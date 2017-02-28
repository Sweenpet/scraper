from bs4 import BeautifulSoup
import urllib2
import re
import os
import sqlite3

class HousePatterns:
    latitude = "\"latitude\":\"(\d+.\d+)\""
    longitude = "\"longitude\":\"([-]\d+.\d+)\""
    floor_area = "<strong>Overall Floor Area:</strong>\s+(\d+.?\d+)\sSq.\sMetres"
    price = "(\d+,(\d+,?)*)"
    beds = "(\d+) Beds?"
    baths = "(\d+) Baths?"
    house = "(Duplex|Apartment|Semi-Detached|Terraced|Bungalow|Detached|Townhouse|End of Terrace House|Acre Site|House)"
    energy = "Energy Performance Indicator:\s+(d+.\d+)\s+kWh/m2/yr"
    energy_rating = "ber_(\w+).png"
    ber_number = "BER No (\d+)"
    description = "Property Description:(.+)Features"

class HouseDetails():

    def __init__(self, postcode):
        self.price = 'null'
        self.house_type = 'null'
        self.beds = 'null'
        self.baths = 'null'
        self.lon = 'null'
        self.lat = 'null'
        self.floor_area = 'null'
        self.location = 'null'
        self.energy_performance = 'null'
        self.energy_rating = 'null'
        self.ber_number = 'null'
        self.postcode = postcode
        self.description = 'null'

class DaftPropertyScraper:

    def __init__(self, input, output):
        self.input = input
        self.output = output
        self.base_url = "http://www.daft.ie"
        self.html_directory = output + 'html_pages/'

        if not os.path.isdir(self.html_directory):
                    os.mkdir(self.html_directory)


    def action(self):

        urlFiles = os.listdir(self.input)

        print(len(urlFiles))

        for fileName in urlFiles:

            postcode = fileName.split('.')[0]
            urlFile = open(self.input + fileName, "r")

            print(fileName)
            propertyFile = open(self.output + fileName, "w")
            propertyFile.write('Type, Price (euro), Beds, Baths, floor area(m^2), location, postcode, lon, lat, energy-performance(kWh/m2/yr), enery-rating, ber number, text, file')
            propertyFile.write('\n')

            count = 0
            for line in urlFile:
              count = count + 1

            print('Total no of properties: ' + str(count))

            #go back to beginning
            urlFile.seek(0)
            houseCount = 0
            for line in urlFile:
               print(houseCount)
               print(line)

               houseDetails = HouseDetails(postcode)

               url = self.base_url + line
               req = urllib2.Request(url)

               try:
                  propertyHtml = urllib2.urlopen(req).read()

                  html_filepath = self.html_directory + str(houseCount) + '.html'
                  html_file = open(html_filepath, "w")
                  html_file.write(propertyHtml)
                  html_file.close()

                  longitudeMatch = re.search(HousePatterns.longitude, propertyHtml, flags = 0)
                  if longitudeMatch:
                     houseDetails.lon = longitudeMatch.group(1)

                  latitudeMatch = re.search(HousePatterns.latitude, propertyHtml, flags = 0)
                  if latitudeMatch:
                     houseDetails.lat = latitudeMatch.group(1)

                  areaMatch = re.search(HousePatterns.floor_area, propertyHtml, flags = 0)
                  if areaMatch:
                     houseDetails.floorArea = areaMatch.group(1)

                  energyMatch = re.search(HousePatterns.energy, propertyHtml, flags = 0)
                  if energyMatch:
                     houseDetails.energyPerformance = energyMatch.group(1)

                  energyRatingMatch = re.search(HousePatterns.energy_rating, propertyHtml, flags = 0)
                  if energyRatingMatch:
                     houseDetails.energyRating = "BER " + energyRatingMatch.group(1)

                  berNumberMatch = re.search(HousePatterns.ber_number, propertyHtml, flags=0)
                  if berNumberMatch:
                     houseDetails.berNumber = berNumberMatch.group(1)

                  description_match = re.search(HousePatterns.description, propertyHtml, flags=0)
                  if description_match:
                     houseDetails.description = description_match
                     houseDetails.description = houseDetails.description.replace('<br>','').replace('<p>','')

                  locality = line.split('/')
                  houseDetails.location = locality[3]

                  soup = BeautifulSoup(propertyHtml, "html.parser")

                  houseSummaryElement = soup.find('div', { 'id':'smi-summary-items'})

                  if (houseSummaryElement == None):
                     print ('could not find house summary')
                     continue

                  childNodes = houseSummaryElement.findChildren()

                  innerText = childNodes[0].text
                  priceMatch = re.search(HousePatterns.price, innerText, flags = 0)
                  if priceMatch:
                     houseDetails.price = priceMatch.group(1)

                  subsets = houseDetails.price.split(',')
                  textPrice = ""

                  for t in subsets:
                     textPrice = textPrice + t

                  houseDetails.price = textPrice

                  text = houseSummaryElement.text

                  houseMatch = re.search(HousePatterns.house, text, flags = 0)
                  if (houseMatch):
                     houseDetails.houseType = houseMatch.group(1)

                  bedsMatch = re.search(HousePatterns.beds, text, flags = 0)
                  if (bedsMatch):
                     houseDetails.beds = bedsMatch.group(1)

                  bathsMatch = re.search(HousePatterns.baths, text, flags = 0)
                  if (bathsMatch):
                     houseDetails.baths = bathsMatch.group(1)

                  details = houseDetails.house_type + ', ' + houseDetails.price + ', ' \
                         + houseDetails.beds + ', ' + houseDetails.baths + ', ' \
                         + houseDetails.floor_area + ', ' + houseDetails.location \
                         + ', ' + houseDetails.postcode + ',' + houseDetails.lon \
                         + ', ' + houseDetails.lat + ', ' + houseDetails.energy_performance \
                         + ', ' + houseDetails.energy_rating + ',' + houseDetails.ber_number \
                         + ','  + houseDetails.description + ',' + html_filepath
                  propertyFile.write(details)
                  propertyFile.write('\n')

                  houseCount += 1
               except:
                    print('error')

            urlFile.close()
            propertyFile.close()


scraper = DaftPropertyScraper('/home/peter/Projects/DaftScraper/PropertyUrls/', '/home/peter/Projects/DaftScraper/RentalProperties/')
scraper.action()
