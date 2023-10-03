import psycopg2
import os

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
        with open(os.path.join(directory, filename), 'r') as file:
            content = file.read()
            # Split and process the content to extract article titles and their content
            # Then call insert_into_database for each article

if __name__ == "__main__":
    process_files('output_directory')
