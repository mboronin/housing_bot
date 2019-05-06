from src import config
from src.dao import base
from src import Appartment


def get_user(userid):
    connection = base.get_connection()
    mycursor = connection.cursor()
    mycursor.execute("SELECT login,password FROM housing.users where userid={userid};".format(userid=userid))
    return mycursor.fetchone()


def get_all_objects():
    connection = base.get_connection()
    mycursor = connection.cursor()
    mycursor.execute("SELECT * FROM housing.rentals where enddate > now() limit 5;")
    results = mycursor.fetchall()
    apts = []
    for result in results:
        apts.append(Appartment.Appartment(result))
    return apts


def get_with_filters(rooms, min_rent, max_rent, district):
    if rooms == 0 and district == "" and min_rent == 0 and max_rent == 0:
        query = "SELECT * FROM housing.rentals where enddate > now();"
    if rooms == 0 and district == "":
        query = "SELECT * FROM housing.rentals where enddate > now() and rent > {min_rent} and rent < {max_rent};".format(
            max_rent=max_rent, min_rent=min_rent)
    elif rooms == 0:
        query = "SELECT * FROM housing.rentals where enddate > now() and rent > {min_rent} and rent < {max_rent} and district={district};".format(
            max_rent=max_rent, min_rent=min_rent, district=district)
    elif district == "":
        query = "SELECT * FROM housing.rentals where enddate > now() and rent > {min_rent} and rent < {max_rent} and rooms={rooms};".format(
            max_rent=max_rent, min_rent=min_rent, rooms=rooms)
    connection = base.get_connection()
    mycursor = connection.cursor()
    mycursor.execute(query)
    results = mycursor.fetchall()
    apts = []
    for result in results:
        apts.append(Appartment.Appartment(result))
    return apts


def get_object(id):
    query = """SELECT * from housing.rentals where id={id};""".format(id=id)
    conn = base.get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    result = list(cursor.fetchone())
    print(result)
    apt = Appartment.Appartment(result)
    return apt
