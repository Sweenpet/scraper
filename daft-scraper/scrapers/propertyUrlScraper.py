from bs4 import BeautifulSoup
import urllib2
import re
import time

start = time.time()

offset = 0;
county = "dublin";
daftBaseUrl = "http://www.daft.ie/" + county + "/property-for-sale/?offset="
propertyUrls = [];
flag = True

f = open("propertyUrls.txt", "w")

while(True):
  daftUrl = daftBaseUrl + str(offset)
  dublinPropertiesHtml = urllib2.urlopen(daftUrl).read()
 
  errorPattern = '<h1>No results</h1>'
   
  if re.search(errorPattern, dublinPropertiesHtml, flags = 0):
   print('breaking')
   break;
    
  soup = BeautifulSoup(dublinPropertiesHtml)
  anchorTags = soup.find_all('span', {'class' : 'sr_counter'})

  for tag in anchorTags:
    tag = tag.next_sibling.next_sibling
    href = tag['href']
    f.write(href)
    f.write('\n')
 

  offset = offset + 10
  print(offset)
f.close()

end = time.time()
print(end - start)
