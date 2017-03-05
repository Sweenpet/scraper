import os
from domain import HouseUrl, PropertyTypeEnum

class PropertyUrlLoader():

    def __init__(self, path, repo):
        self.path = path
        self.repo = repo

    def action(self):
        files = os.listdir(self.path)

        for file_name in files:
            postcode = file_name.split('.')[0]
            url_file = open(self.path + file_name, "r")

            print("---------------")
            print(postcode)
            print("---------------")

            for line in url_file:
                print("inserting: " + line)
                split = line.split('/')
                county = split[1]
                property_type = self.__get_property_type(split[2])
                house_url = HouseUrl(None, county, postcode, property_type.value, line)
                self.repo.insert_into_house_urls(house_url)

    def __get_property_type(self, search_string):
        split = search_string.split('-')
        property_text = split[0]

        if property_text.lower() == "apartments":
            return PropertyTypeEnum.APARTMENT
        elif property_text.lower() == "houses":
            return PropertyTypeEnum.HOUSE
        elif property_text.lower() == "duplexes":
            return PropertyTypeEnum.DUPLEX
        elif property_text.lower == "sites":
            return PropertyTypeEnum.SITE
        elif property_text.lower == "bungalows":
            return PropertyTypeEnum.BUNGALOW
        else:
            return PropertyTypeEnum.UNKNOWN
