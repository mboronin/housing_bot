import pymysql


connection = pymysql.connect(host='localhost',
                                     database='housing',
                                     user='bot',
                                     password='1')
query = """INSERT INTO """
