import sys
import sqlite3
import uuid
from domain import HouseUrl

class DaftRepo:

    def __init__(self):
        self.conn = sqlite3.connect('../daft.db')
        self.cursor = self.conn.cursor()
        self.__configure()

    def __configure(self):
        self.__create_house_details()
        self.__create_house_urls()
        self.conn.commit()

    def __create_house_details(self):
        create_table_sql = "create table if not exists house_details (" \
                               " id text primary key," \
                               " url text not null," \
                               " beds integer," \
                               " baths integer," \
                               " description text," \
                               " latitude real," \
                               " longitude real," \
                               " floor_area real," \
                               " house_type integer," \
                               " enery_performance real," \
                               " energy_rating real," \
                               " ber_number real," \
                               " postcode text," \
                               " price real," \
                               " timestamp date);" \

        self.cursor.execute(create_table_sql)

    def __create_house_urls(self):
        create_house_urls = "create table if not exists house_url (" \
                            "id text primary key," \
                            "county text not null,"  \
                            "postcode text not null," \
                            "property_type int not null," \
                            "url text not null);"

        self.cursor.execute(create_house_urls)

    def __does_house_details_exist(self):
        table_exists_sql = "select count(*) from sqlite_master where " \
                            "type='table' AND name='house_details';"

        result = self.cursor.execute(table_exists_sql)
        return result.arraysize > 0

    def __does_house_url_exist(self):
        table_exists_sql = "select count(*) from sqlite_master where " \
                           "type='table' AND name='house_url';"

        result = self.cursor.execute(table_exists_sql)
        return result.arraysize > 0

    def insert_into_house_urls(self, house_url):
        insert_sql = ("insert into house_url values (" +
                      "'" + str(uuid.uuid1()) + "'" + "," +
                      "'" + house_url.county + "'" + "," +
                      "'" + house_url.postcode + "'" + "," +
                      str(house_url.property_type) + "," +
                      "'" + house_url.url + "'" +
                      ");")

        try:
            self.conn.execute(insert_sql)
            self.conn.commit()
        except:
            error = sys.exc_info()[0]
            print(error)


    def insert_into_house_details(self, house_details):
        insert_sql = ("insert into house_details values (" +
                     self.__format_input(uuid.uuid1()) + ", " +
                     self.__format_input(house_details.url_id)  + ", " +
                     str(house_details.beds) + ", " +
                     str(house_details.baths) + ", " +
                     self.__format_input(house_details.description) + ", " +
                     str(house_details.lat) + ", " +
                     str(house_details.lon) + ", " +
                     str(house_details.floor_area) + ", " +
                     str(house_details.house_type) + ", " +
                     str(house_details.energy_performance) + ", " +
                     self.__format_input(house_details.energy_rating) + ", " +
                     str(house_details.ber_number) + "'" + ", " +
                     self.__format_input(house_details.price) +
                     ");")

        try:
            self.conn.execute(insert_sql)
            self.conn.commit()
        except:
            sys.exc_info()[0]

    def select_all_house_details(self):
        return self.conn.execute("select * from house_details")

    def select_all_house_urls(self):
        result = self.conn.execute("select * from house_url")

        house_urls = []
        for row in result.fetchall():
            house_url = HouseUrl(row[0], row[1], row[2], row[3], row[4])
            house_urls.append(house_url)

        return house_urls

    def get_house_url_count(self):
        return self.conn.execute("select count(*) from house_url")

    def __format_input(self, input):
        return "'" + str(input) + "'"