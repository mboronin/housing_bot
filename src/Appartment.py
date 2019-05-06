class Appartment:

    def __init__(self, row):
        self.id = row[0],
        self.link = row[1],
        self.address = row[2],
        self.rooms = row[3],
        self.rent = row[4],
        self.msize = row[5],
        self.startdate = row[6],
        self.enddate = row[7],
        self.moveindate = row[8],
        self.number_of_applicants = row[9],
        self.landlord = row[10],
        self.housetype = row[11],
        self.contracttype = row[12],
        self.latitude = row[13],
        self.longitude = row[14],
        self.imagelink = row[15],
        self.balcony = row[16],
        self.elevator = row[17],
        self.region = row[18],
        self.district = row[19]

    def __str__(self):
        return """{address}\n{rooms} rooms\nRent is {rent} sek/month.\nSize is {msize}\nView the details here {link}""".format(link=self.link[0], address=self.address[0], rent=self.rent[0], rooms=self.rooms[0],
                           msize=self.msize[0])
