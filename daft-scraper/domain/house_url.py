from domain.property_type_enum import PropertyTypeEnum

class HouseUrl:

    def __init__(self, id, county, postcode, type, url):
        self.id = id
        self.county = county
        self.postcode = postcode
        self.property_type = self.__convert_to_house_type_enum(type)
        self.url = url


    def __convert_to_house_type_enum(self, value):
        if type(value) is int:
            return PropertyTypeEnum(value)

        return type
