import mysql.connector
import traceback
import json
# import Exception

class SearchFiltersInSQL():

    def __init__(self, config):
        self.cursor = None
        self.conn = mysql.connector.connect(**config)

    def searchBookID(self, book_ids=[]):
        sql_query =  "select gutenberg_id as book_id FROM books_book where gutenberg_id={};"
        all_book_ids = []
        error = False
        try:
            book_ids = tuple(book_ids)
            cursor = self.conn.cursor(dictionary=True)
            print("In searchBookID--------------------->",book_ids)
            for each in tuple(book_ids):
                print("*"*50)
                print(sql_query.format(each))
                print("*"*50)

                cursor.execute(sql_query.format(each))

                all_book_ids.extend(cursor.fetchall())

        except Exception as error:
            print(traceback.format_exc(error))
            cursor.close()
            error = True

        finally:
            cursor.close()

        return {'error':error,'data':all_book_ids}

    def searchBookTitle(self, book_titles=[]):
        sql_query = "select gutenberg_id as book_id FROM books_book where title like '%{}%' ;"
        all_book_titles = []
        error = False
        try:

            cursor = self.conn.cursor(dictionary=True)

            for each in book_titles:
                # print(sql_query.format(each))
                cursor.execute(sql_query.format(each))

                all_book_titles.extend(cursor.fetchall())

        except Exception as error:
            print(traceback.format_exc(error))
            cursor.close()
            error = True

        finally:
            cursor.close()

        return {'error':error,'data':all_book_titles}

    def searchBookLanguage(self, book_languages=[]):
        sql_query = "SELECT all_lang.book_id FROM books_language AS book_lang JOIN books_book_languages AS all_lang ON book_lang.id = all_lang.language_id where book_lang.code like '%{}%';"

        books_with_language = []

        error = False
        try:

            cursor = self.conn.cursor(dictionary=True)

            for each in book_languages:
                # print(sql_query.format(each))
                cursor.execute(sql_query.format(each))

                books_with_language.extend(cursor.fetchall())

        except Exception as error:
            print(traceback.format_exc(error))
            cursor.close()
            error = True

        finally:
            cursor.close()

        return {'error':error,'data':books_with_language}


    def searchMIMETypes(self, mime_filters = []):
        sql_query = "select book_id from books_format where mime_type like '%{}%';"

        bookid_with_mime = []
        error = False
        try:

            cursor = self.conn.cursor(dictionary=True)

            for each in mime_filters:
                # print(sql_query.format(each))
                cursor.execute(sql_query.format(each))

                bookid_with_mime.extend(cursor.fetchall())

        except Exception as error:
            print(traceback.format_exc(error))
            cursor.close()
            error = True

        finally:
            cursor.close()

        return {'error':error,'data':bookid_with_mime}

    def searchBookAuthor(self, authors_filter=[]):
        sql_query = "select b_author.book_id from books_book_authors as b_author join books_author as all_author on b_author.author_id = all_author.id where all_author.name like '%{}%';"

        book_author = []
        error = False
        try:

            cursor = self.conn.cursor(dictionary=True)

            for each in authors_filter:
                # print(sql_query.format(each))
                cursor.execute(sql_query.format(each))

                book_author.extend(cursor.fetchall())

        except Exception as error:
            print(traceback.format_exc(error))
            cursor.close()
            error = True

        finally:
            cursor.close()

        return {'error':error,'data':book_author}

    def searchBookTopics(self, book_topics=[]):
        sql_subject_query = "select bbs.book_id from books_subject join books_book_subjects as bbs on books_subject.id= bbs.subject_id where books_subject.name like '%{}%';"

        sql_bookshelves_query = "select bbb.book_id from books_bookshelf as bbs join books_book_bookshelves as bbb on bbb.bookshelf_id=bbs.id where bbs.name like '%{}%';"

        book_with_topics = []
        error = False
        try:

            cursor = self.conn.cursor(dictionary=True)

            for each in book_topics:
                # print(sql_query.format(each))
                cursor.execute(sql_subject_query.format(each))
                book_with_topics.extend(cursor.fetchall())

                cursor.execute(sql_bookshelves_query.format(each))
                book_with_topics.extend(cursor.fetchall())

        except Exception as error:
            print(traceback.format_exc(error))
            cursor.close()
            error = True

        finally:
            cursor.close()

        return {'error':error,'data':book_with_topics}

# if __name__ == '__main__':

    # config = json.load(open('./config.json'))
    # config['database'] = 'gutenberg'

    # try:
        # search  = SearchFiltersInSQL(config)

        # book_id_data = search.searchBookID([2,3,4])
        # # print(book_id_data)
        # print("*"*50)
        #
        # book_title_data = search.searchBookTitle(['The United States','The MayFlower Compact'])
        # # print(book_title_data)
        # print("*"*50)
        #
        # book_languages = search.searchBookLanguage(['en','da'])
        # # print(book_languages)
        # print("*"*50)
        #
        # book_mimes = search.searchMIMETypes(['text/plain','epub'])
        # # print(book_mimes)
        # print("*"*50)
        #
        # book_authors = search.searchBookAuthor(['Thomas','Lincoln'])
        # # print(book_authors)
        # print("*"*50)
        #
        # book_topics = search.searchBookTopics(['United States Law','Civil W'])
        # # print(book_topics)
        # print("*"*50)
        #
        # # import pdb;pdb.set_trace()
        # final = book_id_data['data'] + book_title_data['data'] + book_languages['data'] + book_mimes['data'] + book_authors['data'] + book_topics['data']


    #
    # except Exception as error:
    #     print(traceback.format_exc(error))
