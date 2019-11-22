import mysql.connector
import traceback
import json

class SearchSortBooks():

    def __init__(self, config):
        self.cursor = None
        self.conn = mysql.connector.connect(**config)

    def grabBookDetailsSQL(self,book_ids,offset,limit):
        cursor = self.conn.cursor(dictionary=True)
        error = False
        book_details = {}

        try:
            sql_query = open('./book_search/sql_query.sql').read()
            print("Book_ids in grabBookDetailsSQL--->",book_ids)
            print("generated sql --->",sql_query.format(book_ids,limit,offset))
            cursor.execute(sql_query.format(book_ids,limit,offset))
            book_details = cursor.fetchall()
            print("Fetched book_details -->",book_details)

        except Exception as error:
            print(traceback.format_exc(error))
            error = True

        finally:
            cursor.close()
            self.conn.close()

        return book_details


# if __name__ == '__main__':

    # filtered_data = json.load(open('test.json'),encoding='UTF-8')
    # config = json.load(open('config.json'))
    # config['database'] = 'gutenberg'
    # res = SearchSortBooks(config)
    # data = res.grabBookDetailsSQL(data,25,50)
    # print(data)
    # print(len(data))
