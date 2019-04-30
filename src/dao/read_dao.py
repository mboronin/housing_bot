from src import config
from src.dao import base
from src import Appartment


def save_object(insert_list):
    query = """
        INSERT IGNORE INTO `{database}`.`{table}`
        (id, link, address, rooms, rent, msize, startdate, enddate, moveindate, number_of_applicants, landlord, housetype, contracttype, latitude, longtitude, imagelink, balcony, elevator, region, district)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """.format(database=config.DB_SCHEMA, table=config.DB_TABLE)
    conn = base.get_connection()
    cursor = conn.cursor()
    cursor.execute(query, insert_list)


def get_all_objects():
    connection = base.get_connection()
    mycursor = connection.cursor()
    mycursor.execute("SELECT * FROM housing.rentals where enddate > now();")
    results = mycursor.fetchall()
    apts = []
    for result in results:
        apts.append(Appartment.Appartment(result))
    return apts


def get_with_filters(rooms, min_rent, max_rent, district):
    if rooms is None and district is None and min_rent is None and max_rent is None:
        query = "SELECT * FROM housing.rentals where enddate > now();"
    if rooms is None and district is None:
        query= "SELECT * FROM housing.rentals where enddate > now() and rent > {min_rent} and rent < {max_rent};".format(
            max_rent=max_rent, min_rent=min_rent)
    elif rooms is None:
        query = "SELECT * FROM housing.rentals where enddate > now() and rent > {min_rent} and rent < {max_rent} and district={district};".format(
            max_rent=max_rent, min_rent=min_rent, district=district)
    elif district is None:
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
    return str(apt)
