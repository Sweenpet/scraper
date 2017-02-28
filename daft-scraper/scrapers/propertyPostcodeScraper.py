from bs4 import BeautifulSoup
import urllib2
import re
import time

start = time.time()
postcodes = ['1','2','3','4','5','6','6w','7','8','9','10','11','12','13','14','15','16','17','18','20','22','24']

for pcn in postcodes:

  propertyUrls = []
  postcode = "dublin-" + pcn
  daftBaseUrl = "http://www.daft.ie/dublin/property-for-sale/" + postcode + "/?offset="

  print(postcode)
  f = open("/home/peter/Projects/DaftScraper/PropertyUrls/" + postcode + ".txt", "w")
  offset = 0
  while(True):
    daftUrl = daftBaseUrl + str(offset)
    dublinPropertiesHtml = urllib2.urlopen(daftUrl).read()

    errorPattern = '<h1>No results</h1>'

    if re.search(errorPattern, dublinPropertiesHtml, flags = 0):
      print('breaking')
      break;

    soup = BeautifulSoup(dublinPropertiesHtml, "html.parser")
    anchorTags = soup.find_all('span', {'class' : 'sr_counter'})

    for tag in anchorTags:
      tag = tag.next_sibling.next_sibling
      href = tag['href']
      f.write(href)
      f.write('\n')

    offset = offset + 10

  f.close()
end = time.time()
print(end - start)
