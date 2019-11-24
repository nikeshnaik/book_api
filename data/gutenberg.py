import mysql.connector
import traceback
import sqlparse
import json

# config = {'user':'rootx','password':'rootx1234','host':'localhost','port':3306,'raise_on_warnings':True,'charset':'utf8'}

class CreateAndDumpSQL():
    def __init__(self,config):
        self.cursor = None
        self.conn = mysql.connector.connect(**config)

    def create_database(self):
        try:
            cursor = self.conn.cursor()
            with open('data/gutendex.sql','r',encoding="utf-8") as sql:
                sql_commands = sql.read()
            print("Fetched DB Create Sql File and Executing..")
            test_sql = "SHOW DATABASES LIKE 'gutenberg';"
            cursor.execute(test_sql)

            if not cursor.fetchall():

                for each in sqlparse.split(sql_commands):
                    if each:
                        print(each)
                        cursor.execute(each)

                print("DataBase Created and SQL Dumped")

            else:
                print("Database Already Created")


            self.conn.commit()
            cursor.close()

        except Exception as error:
            print(traceback.format_exc(error))

# if __name__ == '__main__':
    #
    # config = json.load(open('../config.json'))
    # create = CreateAndDumpSQL(config)
    # create.create_database()
