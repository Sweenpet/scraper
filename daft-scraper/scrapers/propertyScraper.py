from bs4 import BeautifulSoup
import urllib2
import re
import time
import os

# Container class for hous details
class HouseDetails(object):
  pass


start = time.time()

daftBaseUrl = "http://www.daft.ie"

urlFiles = os.listdir("/home/peter/Projects/DaftScraper/PropertyUrls")

latitudePattern = "\"latitude\":\"(\d+.\d+)\""
longitudePattern = "\"longitude\":\"([-]\d+.\d+)\""
floorAreaPattern = "<strong>Overall Floor Area:</strong>\s+(\d+.?\d+)\sSq.\sMetres"
pricePattern = "(\d+,(\d+,?)*)"
bedsPattern = "(\d+) Beds?"
bathsPattern = "(\d+) Baths?"
housePattern = "(Duplex|Apartment|Semi-Detached|Terraced|Bungalow|Detached|Townhouse|End of Terrace House|Acre Site|House)"
energyPattern = "Energy Performance Indicator:\s+(d+.\d+)\s+kWh/m2/yr"
energyRatingPattern = "ber_(\w+).png"
berNumberPattern = "BER No (\d+)"

for fileName in urlFiles:

    postcode = fileName.split('.')[0]
    urlFile = open("/home/peter/Projects/DaftScraper/PropertyUrls/" + fileName, "r")

    print(fileName)
    propertyFile = open("/home/peter/Projects/DaftScraper/RentalProperties/"+fileName, "w")
    propertyFile.write('Type, Price (euro), Beds, Baths, floor area(m^2), location, postcode, lon, lat, energy-performance(kWh/m2/yr), enery-rating, ber number')
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
       houseDetails = HouseDetails()

       #add these as default parameters in class
       houseDetails.price = 'null'
       houseDetails.houseType = 'null'
       houseDetails.beds = 'null'
       houseDetails.baths = 'null'
       houseDetails.lon = 'null'
       houseDetails.lat = 'null'
       houseDetails.floorArea = 'null'
       houseDetails.location = 'null'
       houseDetails.postcode = postcode
       houseDetails.energyPerformance = 'null'
       houseDetails.energyRating = 'null'
       houseDetails.berNumber = 'null'


       url = daftBaseUrl + line
       req = urllib2.Request(url)

       try:
          propertyHtml = urllib2.urlopen(req).read()

          longitudeMatch = re.search(longitudePattern, propertyHtml, flags = 0)
          if longitudeMatch:
             houseDetails.lon = longitudeMatch.group(1)

          latitudeMatch = re.search(latitudePattern, propertyHtml, flags = 0)
          if latitudeMatch:
             houseDetails.lat = latitudeMatch.group(1)

          areaMatch = re.search(floorAreaPattern, propertyHtml, flags = 0)
          if areaMatch:
             houseDetails.floorArea = areaMatch.group(1)

          energyMatch = re.search(energyPattern, propertyHtml, flags = 0)
          if energyMatch:
             houseDetails.energyPerformance = energyMatch.group(1)

          energyRatingMatch = re.search(energyRatingPattern, propertyHtml, flags = 0)
          if energyRatingMatch:
             houseDetails.energyRating = "BER " + energyRatingMatch.group(1)

          berNumberMatch = re.search(berNumberPattern, propertyHtml, flags=0)
          if berNumberMatch:
             houseDetails.berNumber = berNumberMatch.group(1)

          locality = line.split('/')
          houseDetails.location = locality[3]

          soup = BeautifulSoup(propertyHtml, "html.parser")

          houseSummaryElement = soup.find('div', { 'id':'smi-summary-items'})

          if (houseSummaryElement == None):
             continue

          childNodes = houseSummaryElement.findChildren()

          innerText = childNodes[0].text
          priceMatch = re.search(pricePattern, innerText, flags = 0)
          if priceMatch:
             price = priceMatch.group(1)

          subsets = price.split(',')
          textPrice = ""

          for t in subsets:
             textPrice = textPrice + t

          houseDetails.price = textPrice

          text  = houseSummaryElement.text

          houseMatch = re.search(housePattern, text, flags = 0)
          if (houseMatch):
             houseDetails.houseType = houseMatch.group(1)

          bedsMatch = re.search(bedsPattern, text, flags = 0)
          if (bedsMatch):
             houseDetails.beds = bedsMatch.group(1)

          bathsMatch = re.search(bathsPattern, text, flags = 0)
          if (bathsMatch):
             houseDetails.baths = bathsMatch.group(1)

          details = houseDetails.houseType + ', ' + houseDetails.price + ', ' \
                 + houseDetails.beds + ', ' + houseDetails.baths + ', ' \
                 + houseDetails.floorArea + ', ' + houseDetails.location \
                 + ', ' + houseDetails.postcode + ',' + houseDetails.lon \
                 + ', ' + houseDetails.lat + ', ' + houseDetails.energyPerformance \
                 + ', ' + houseDetails.energyRating + ',' + houseDetails.berNumber

          propertyFile.write(details)
          propertyFile.write('\n')

          houseCount = houseCount + 1
       except:
            print('error')

    urlFile.close()
    propertyFile.close()
