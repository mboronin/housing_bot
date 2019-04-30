from datetime import datetime

from future.types.newint import long

from src import config


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

    @classmethod
    def from_db(self, row):
        self.id = row[0],
        self.link = row[1],
        self.address = row[2],
        self.rooms = row[3],
        self.rent = row[5],
        self.msize = row[6],
        self.startdate = row[7],
        self.enddate = row[8],
        self.moveindate = row[9],
        self.number_of_applicants = row[10],
        self.landlord = row[11],
        self.housetype = row[12],
        self.contracttype = row[13],
        self.latitude = row[14],
        self.longitude = row[15],
        self.imagelink = row[16],
        self.balcony = row[17],
        self.elevator = row[18],
        self.region = row[19],
        self.district = row[20]
        return self

    def __str__(self):
        return """
        link = {link}
        address = {address}
        rooms = {rooms}
        imagelink = {imagelink}
        """.format(link=self.link, address=self.address, rooms=self.rooms, imagelink=self.imagelink)
