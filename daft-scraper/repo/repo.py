import sqlite3

class DaftRepo:

    def __init__(self):
        self.conn = sqlite3.connect('daft.db')

    def configure(self):
        create_table_sql = " create table house_details (" \
                           " id integer primary key," \
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
                           " postcode text" \
                           " price real" \
                           " timestamp date);" \

        self.conn.execute(create_table_sql)

    def insert(self, house_details):
        insert_sql = ("INSERT INTO stocks VALUES (" +
                     str(house_details.url) + "," +
                     str(house_details.beds) + "," +
                     str(house_details.baths) + "," +
                     str(house_details.description) + "," +
                     str(house_details.lat) + "," +
                     str(house_details.lon) + "," +
                     str(house_details.floor_area) + "," +
                     str(house_details.house_type) + "," +
                     str(house_details.energy_performance) + "," +
                     str(house_details.energy_rating) + "," +
                     str(house_details.ber) + "," +
                     str(house_details.postcode) + "," +
                     str(house_details.price))

        self.conn.execute(insert_sql)


    def select_all(self):
        return self.conn("select * from house_details")
