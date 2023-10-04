import psycopg2
import os

def insert_into_database(id, article_title, article_content):
    try:
        connection = psycopg2.connect(
            database="wikivi"
        )
        cursor = connection.cursor()

        insert_query = """
        INSERT INTO wikipedia_articles (id, title, content)
        VALUES (%s, %s);
        """
        cursor.execute(insert_query, (id, article_title, article_content))
        
        connection.commit()
        
    except Exception as error:
        print(f"Error: {error}")
    finally:
        if connection:
            cursor.close()
            connection.close()
'''
def process_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename), 'r') as file:
		data = json.load(file)
		i = 0
		for entry in data:
		    title = entry.get('title')
		    content = entry.get('text')
		    id = i
		    insert_into_database(id, title, content)
		    i += 1

if __name__ == "__main__":
    process_files('output_directory')
'''
