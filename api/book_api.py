from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from book_search import SearchFiltersInSQL,SearchSortBooks
from data import CreateAndDumpSQL
import json
import traceback

app = FlaskAPI(__name__)


@app.route("/books/v1/", methods=['GET', 'POST'])
def book_api():
    print("v1 api request in ")

    config = json.load(open('./config.json'))
    config['database'] = 'gutenberg'

    search = SearchFiltersInSQL(config)
    sortdata = SearchSortBooks(config)

    print(request.data)
    final_data = {}
    start =0
    end=55000
    if request.method =='POST':

        filters = request.data.get('filters',None)
        print('Filter -->',type(filters))
        # import pdb;pdb.set_trace()
        start = filters.get('start',0)
        end = filters.get('end',100)

        all_book_ids = []
        for key, value in filters.items():
            data = []
            if key == 'book_id':
                data = search.searchBookID(value)
                all_book_ids.extend([each['book_id'] for each in data['data']])

            elif key == 'title':
                data = search.searchBookTitle(value)
                all_book_ids.extend([each['book_id'] for each in data['data']])

            elif key == 'language':
                data = search.searchBookLanguage(value)
                all_book_ids.extend([each['book_id'] for each in data['data']])

            elif key == 'mime_types':
                data  = search.searchMIMETypes(value)
                all_book_ids.extend([each['book_id'] for each in data['data']])

            elif key == 'authors':
                data = search.searchBookAuthor(value)
                all_book_ids.extend([each['book_id'] for each in data['data']])

            elif key =='topics':
                data = search.searchBookTopics(value)
                all_book_ids.extend([each['book_id'] for each in data['data']])


        all_book_ids = tuple(list(set(all_book_ids)))

        print(all_book_ids,start,end)
        sql_data = sortdata.grabBookDetailsSQL(all_book_ids,start,end)

        for row in sql_data:
            row['mime_type'] = row['mime_type'].split(';') if row['mime_type'] != None else row['mime_type']

            row['urls'] = row['urls'].split(',') if row['urls'] != None else row['urls']

            row['subjects'] = row['subjects'].split('--') if row['subjects'] != None else  row['subjects']

            # temp = row['author_name_birth_year']

            # if row['author_name_birth_year']:
            #     if birth_year and death_year:
            #         temp = f'Author Name: {author} ({birth_year} - {death_year})'
            #     elif birth_year and death_year==None:
            #         temp = f'Author Name: {author} ({birth_year}- Present)'
            #     else:
            #         temp = f'Author Name: {author}'

            # row['author_name_birth_year'] = temp

            row['bookshelf'] = row['bookshelf'].split('--') if row['bookshelf'] != None else row['bookshelf']

        final_data['data'] = sql_data
        return json.dumps(final_data,indent=4)



if __name__ == "__main__":
    config = json.load(open('./config.json'))
    print("here")
    try:
        # dumpdata = CreateAndDumpSQL(config)
        # dumpdata.create_database()
        print("DataBase Created")

        app.run(debug =False)

    except Exception as error:
        print("Error at Deployment",traceback.format_exc(error))
