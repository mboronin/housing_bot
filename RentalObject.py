from datetime import datetime

from bs4 import BeautifulSoup


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
        longtitude:
        balcony:
        elevator:
        region:
        district:
    """

    def __init__(self, result):
        self.id = int(result.find("span", "rentalObjectId hidden").string)
        self.link = str(result.find("a", href=True)['href'])
        self.rooms = int(result.find("span", "rooms hidden").string)
        self.rent = result.find("span", "rent hidden").string
        #self.size = float(result.find("span", "size hidden").string.replace(",", "."))
        self.startdate = (int(result.find("span", "startdate hidden").string)/1000.0)
        self.enddate = (int(result.find("span", "enddate hidden").string)/1000.0)
        self.moveindat = result.find("span", "moveindate hidden").string
        self.number_of_applicants = int(result.find("span", "applications hidden").string)
        self.landlord = result.find("span", "landlord hidden").string
        self.type = result.find("span", "boendetyp hidden").string
        self.contracttype = result.find("span", "kontraktstyp hidden").string
        self.latitude = result.find("span", "latitude hidden").string
        self.longtitude = result.find("span", "longitude hidden").string
        self.imagelink = "https://bostad.uppsala.se" + result.find("span", "imagePrimaryId hidden").string
        self.balcony = bool(result.find("span", "balcony hidden").string)
        self.elevator = bool(result.find("span", "elevator hidden").string)
        self.region = result.find("span", "region hidden").string
        self.district = result.find("span", "district hidden").string

    def __str__(self):
        attrs = vars(self)
        print(attrs)
