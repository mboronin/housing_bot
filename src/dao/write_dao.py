from src import config
from src.dao import base


def save_object(insert_list):
    query = """
        INSERT IGNORE INTO `{database}`.`{table}`
        (id, link, address, rooms, rent, msize, startdate, enddate, moveindate, number_of_applicants, landlord, housetype, contracttype, latitude, longtitude, imagelink, balcony, elevator, region, district)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """.format(database=config.DB_SCHEMA, table=config.DB_TABLE)
    conn = base.get_connection()
    cursor = conn.cursor()
    cursor.execute(query, insert_list)


def save_user(user_details):
    query = """
            INSERT IGNORE INTO `{database}`.`{table}`
            (login, password, name, userid)
            VALUES (%s, %s, %s, %s);
        """.format(database=config.DB_SCHEMA, table=config.USER_TABLE)
    conn = base.get_connection()
    cursor = conn.cursor()
    cursor.execute(query, user_details)
    conn.commit()