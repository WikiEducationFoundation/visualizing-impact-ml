import psycopg2
import psycopg2.extras
import os

def insert_into_bulk_database(cursor, data):
    try:
        insert_query = """
        INSERT INTO wikipedia_data (id, title, content)
        VALUES %s;
        """
        psycopg2.extras.execute_values(
            cursor, insert_query, data, page_size=100
        )
    except Exception as error:
        print(f"Error: {error}")

def insert_into_database(wikiid, article_title, article_content):
    try:
        connection = psycopg2.connect(
            database="wikivi"
        )
        cursor = connection.cursor()

        insert_query = """
        INSERT INTO wikipedia_data (id, title, content)
        VALUES (%s, %s, %s);
        """
        cursor.execute(insert_query, (wikiid, article_title, article_content))
        
        connection.commit()
        
    except Exception as error:
        print(f"Error: {error}")
    finally:
        if connection:
            cursor.close()
            connection.close()
