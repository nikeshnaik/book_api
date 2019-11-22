

SELECT
      BOOK_MAIN.book_id,
			BOOK_MAIN.title,
			BOOK_MAIN.download_count,
			BOOK_MAIN.mime_type,
			BOOK_MAIN.urls,
			BOOK_MAIN.languages,
			BOOK_MAIN.topics as subjects,
			BOOK_MAIN.author_name_birth_year,
            BOOK_shelves.topics as bookshelf
FROM

           (
           SELECT 			BOOK_MAIN.book_id,
							BOOK_MAIN.title,
							BOOK_MAIN.download_count,
							BOOK_MAIN.mime_type,
							BOOK_MAIN.urls,
							BOOK_MAIN.languages,
							BOOK_MAIN.topics,
							BOOK_authors.author_name_birth_year

			FROM

					(SELECT	BOOK_MAIN.book_id,
							BOOK_MAIN.title,
							BOOK_MAIN.download_count,
							BOOK_MAIN.mime_type,
							BOOK_MAIN.urls,
							BOOK_MAIN.languages,
							BOOK_subject.topics
					FROM
							(SELECT BOOK_MAIN.book_id,
									BOOK_MAIN.title,
									BOOK_MAIN.download_count,
									BOOK_MAIN.mime_type,
                  BOOK_MAIN.urls,
									BOOK_languages.code as languages

							FROM
									(SELECT BOOK_MAIN.book_id,
										   BOOK_MAIN.title,
										   BOOK_MAIN.download_count,
										   IFNULL(BOOK_mime.mime_types, 'None') as mime_type,
                                           IFNULL(BOOK_mime.urls,'None') as urls

										FROM
											(SELECT gutenberg_id as book_id, title,download_count FROM books_book where gutenberg_id in {}) as BOOK_MAIN

										LEFT JOIN
											(SELECT book_id,group_concat(mime_type) as mime_types,group_concat(url) as urls FROM books_format  group by book_id) as BOOK_mime

										ON BOOK_MAIN.book_id = BOOK_mime.book_id

									) AS BOOK_MAIN


									LEFT JOIN
											(SELECT all_lang.book_id, book_lang.code
											 FROM books_language AS book_lang
											 JOIN books_book_languages AS all_lang
											 ON book_lang.id = all_lang.language_id

											 ) as BOOK_languages

									ON BOOK_MAIN.book_id=BOOK_languages.book_id
							)

							AS BOOK_MAIN

							LEFT JOIN

									(SELECT bbs.book_id,group_concat(books_subject.name) as topics
									 FROM books_subject
									 JOIN books_book_subjects as bbs
									 ON books_subject.id= bbs.subject_id
									 GROUP BY bbs.book_id
									 )  AS BOOK_subject

							ON BOOK_MAIN.book_id=BOOK_subject.book_id
					)
					AS BOOK_MAIN

					LEFT JOIN

					(
						SELECT b_author.book_id,
						GROUP_CONCAT(DISTINCT CONCAT(all_author.name ,'|',all_author.birth_year,'|',all_author.death_year))
						AS author_name_birth_year
						FROM books_book_authors as b_author
						JOIN books_author AS all_author
						ON b_author.author_id = all_author.id
						GROUP BY b_author.book_id
                    )
					 AS BOOK_authors on BOOK_MAIN.book_id=BOOK_authors.book_id

		) AS BOOK_MAIN

        LEFT JOIN

        (SELECT bbb.book_id, group_concat(bbs.name) as topics
         FROM books_bookshelf as bbs
         JOIN books_book_bookshelves as bbb
         ON bbb.bookshelf_id=bbs.id group by bbb.book_id)
         AS BOOK_shelves ON BOOK_MAIN.book_id=BOOK_shelves.book_id
         ORDER BY BOOK_MAIN.download_count DESC limit {} offset {};
