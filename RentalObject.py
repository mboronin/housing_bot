import time
from datetime import datetime

from bs4 import BeautifulSoup
from future.types.newint import long

import config


class RentalObject:
    """An item availalbe for rent

    Attributes:
        id:
        address:
        image:
        category:
        rent:
        rooms:
        size:
        startdate:
        enddate:
        moveindate:
        numberofapplicants:
        landlord:
        latitude:
        longitude:
        balcony:
        elevator:
        region:
        district:
    """

    def __init__(self, result):
        self.id = int(result.find("span", "rentalObjectId hidden").string)
        self.link = config.BOSTAD_LINK + str(result.find("a", href=True)['href'])
        self.address = str(result.find("span", "address notranslate").string)
        self.rooms = int(result.find("span", "rooms hidden").string)
        self.rent = float(result.find("span", "rent hidden").string.replace(",", "."))
        self.msize = float(result.find("span", "size hidden").string.replace(",", "."))
        ms = ((long(result.find("span", "startdate hidden").string)) / 10000000.0) - config.TIME_CONST
        self.startdate = datetime.fromtimestamp(ms)
        ms = (long(result.find("span", "enddate hidden").string) / 10000000.0) - config.TIME_CONST
        self.enddate = datetime.fromtimestamp(ms)
        ms = (long(result.find("span", "moveindate hidden").string) / 10000000.0) - config.TIME_CONST
        self.moveindate = datetime.fromtimestamp(ms)
        self.number_of_applicants = int(result.find("span", "applications hidden").string)
        self.landlord = str(result.find("span", "landlord hidden").string)
        self.housetype = str(result.find("span", "boendetyp hidden").string)
        self.contracttype = str(result.find("span", "kontraktstyp hidden").string)
        latitude = result.find("span", "latitude hidden").string
        if latitude is not None:
            self.latitude = float(latitude.replace(",", "."))
        else:
            self.latitude = None
        longitude = result.find("span", "longitude hidden").string
        if longitude is not None:
            self.longitude = float(longitude.replace(",", "."))
        else:
             self.longitude = None
        self.imagelink = config.BOSTAD_LINK + result.find("span", "imagePrimaryId hidden").string
        self.balcony = bool(result.find("span", "balcony hidden").string)
        self.elevator = bool(result.find("span", "elevator hidden").string)
        self.region = str(result.find("span", "region hidden").string)
        self.district = str(result.find("span", "district hidden").string)

    def __str__(self):
        attrs = vars(self)
        return attrs

    def get_insert_list(self):
        data = (
            self.id,
            self.link,
            self.address,
            self.rooms,
            self.rent,
            self.msize,
            self.startdate,
            self.enddate,
            self.moveindate,
            self.number_of_applicants,
            self.landlord,
            self.housetype,
            self.contracttype,
            self.latitude,
            self.longitude,
            self.imagelink,
            self.balcony,
            self.elevator,
            self.region,
            self.district
        )
        return data


'''


itemBank = []
for row in rows:
    itemBank.append((
        tempRow2['Item_Name'],
        tempRow1['Item_Price'],
        tempRow3['Item_In_Stock'],
        tempRow4['Item_Max'],
        getTimeExtra
        )) #append data
'''

'''
'''

'''
        def __str__(self):
            return """
            product_id      = {product_id}
            product_name    = {product_name}
            id_value        = {id_value}
            category_id     = {category_id}
            brand_id        = {brand_id}
            match_text      = {match_text}
            matches         = {matches}
        """.format(
                product_id=self.product_id,
                product_name=self.product_name,
                id_value=self.id_value,
                category_id=self.category_id,
                brand_id=self.brand_id,
                match_text=self.match_text,
                matches=self.matches,
            )
'''
