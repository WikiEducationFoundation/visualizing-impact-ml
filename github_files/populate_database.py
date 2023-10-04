import psycopg2
import os
import json

def insert_into_database(article_title, article_content):
    try:
        connection = psycopg2.connect(
            database="wikivi"
        )
        cursor = connection.cursor()

        insert_query = """
        INSERT INTO wikipedia_articles (title, content)
        VALUES (%s, %s);
        """
        cursor.execute(insert_query, (article_title, article_content))

        connection.commit()

    except Exception as error:
        print(f"Error: {error}")
    finally:
        if connection:
            cursor.close()
            connection.close()

def process_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename), 'r') as file:
                data = json.load(file)
                for entry in data:
                    title = entry.get('title')
                    content = entry.get('text')
                    # Call insert_into_database for each article
                    insert_into_database(title, content)

if __name__ == "__main__":
    process_files('output_directory')
