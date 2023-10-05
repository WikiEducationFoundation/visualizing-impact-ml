import psycopg2
import os

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
