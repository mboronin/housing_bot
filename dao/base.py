import pymysql

conn = None


def get_connection():
    global conn
    if conn and conn.open:
        return conn

    conn = pymysql.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        user=config.DB_USER,
        password=config.DB_PASS,
        charset=config.DB_CHARSET,
    )
    return conn


def close_connection():
    if conn and conn.open:
        conn.close()


def write_commit():
    get_connection().commit()


def create_write_structure():
    conn = get_connection()
    config.logger.debug('Creating schema and table: `{database}`.`{table}`'.format(
        database=config.DB_SCHEMA, table=config.DB_TABLE))

    try:
        query = 'CREATE DATABASE IF NOT EXISTS {database}'.format(
            database=config.DB_SCHEMA)
        res = conn.cursor().execute(query)
    except MySQLError as e:
        config.logger.debug("Schema already exists.")

    try:
        query = """
            CREATE TABLE IF NOT EXISTS `{database}`.`{table}` (
                `product_id` int(11) NOT NULL,
                `matchstring` varchar(150) COLLATE utf8_unicode_ci,
                `category_id` int(11) NOT NULL,
                `brand_id` int(11) NOT NULL,
                PRIMARY KEY (`product_id`,`matchstring`)
            )
                ENGINE=InnoDB
                DEFAULT
                CHARSET=utf8
                COLLATE=utf8_unicode_ci;
        """.format(database=config.DB_SCHEMA,
                   table=config.DB_TABLE)
        res = conn.cursor().execute(query)
    except MySQLError as e:
        config.logger.debug("Table already exists.")

    config.logger.debug('Done.')


def create_all_indexes():
    fields = ['product_id', 'matchstring', 'category_id', 'brand_id']
    for field in fields:
        create_index(field)


def create_index(field):
    conn = get_connection()
    query = """
        CREATE INDEX `{table}_{field}_idx`
        ON `{database}`.`{table}`
        ({field});
    """.format(database=config.DB_SCHEMA,
               table=config.DB_TABLE,
               field=field)
    res = conn.cursor().execute(query)


def backup_tables():
    conn = get_connection()
    query = """
        DROP TABLE IF EXISTS `{database}`.`{backup_table}`;
    """.format(
        database=config.DB_SCHEMA,
        backup_table=config.DB_BACKUP_TABLE,
    )
    res = conn.cursor().execute(query)
    query = """
        RENAME TABLE `{database}`.`{original_table}`
        TO `{database}`.`{backup_table}`;
    """.format(
        database=config.DB_SCHEMA,
        original_table=config.DB_TABLE,
        backup_table=config.DB_BACKUP_TABLE,
    )
    res = conn.cursor().execute(query)
