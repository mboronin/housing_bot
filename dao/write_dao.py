import pymysql

def save_product_id_match(inset_list):
    query = """
        INSERT IGNORE INTO `{database}`.`{table}`
        (product_id, matchstring, category_id, brand_id)
        VALUES (%s, %s, %s, %s);
    """.format(database=config.DB_SCHEMA, table=config.DB_TABLE)

    conn = base.get_connection()
    cursor = conn.cursor()
    cursor.executemany(query, inset_list)
