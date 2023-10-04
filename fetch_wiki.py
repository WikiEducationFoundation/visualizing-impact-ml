import wikipediaapi

def fetch_wikipedia_data(page_title, lang='en'):
    # Initialize Wikipedia API with the desired language
    wiki_wiki = wikipediaapi.Wikipedia('test_vi', lang)
    
    # Fetch the Wikipedia page
    page = wiki_wiki.page(page_title)
    
    if not page.exists():
        print(f"The page '{page_title}' does not exist.")
        return
    
    # Collect data
    data = {
        'title': page.title,
        'summary': page.summary, 
        'sections': [],
        'links': []
    }
    
    # Fetch sections
    for section in page.sections:
        data['sections'].append({
            'title': section.title,
            'text': section.text
        })
    
    # Fetch links
    for link in page.links:
        data['links'].append(link)
    
    return data

if __name__ == "__main__":
    # Get article choice from the user
    article_choice = input("Enter the title of the Wikipedia article you want to fetch: ")
    
    # Fetch data for the chosen article
    sample_data = fetch_wikipedia_data(article_choice)
    
    # Print the collected data
    print("Collected Data:")
    print(f"Title: {sample_data['title']}")
    print(f"Summary: {sample_data['summary']}")
    print("Sections:")
    for section in sample_data['sections']:
        print(f"  - {section['title']}: {section['text']}")
    print("Links:")
    for link in sample_data['links'][:5]:  # First 5 links
        print(f"  - {link}")


def insert_into_database(data):
    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(
            host="localhost",
            database="wiki_vi_1",
            user="postgres",
            password="wikivi"
        )
        cursor = connection.cursor()

        # Insert data into the database
        insert_query = """
        INSERT INTO wikipedia_data (title, summary, sections, links)
        VALUES (%s, %s, %s, %s);
        """
        cursor.execute(insert_query, (data['title'], data['summary'], str(data['sections']), str(data['links'][:5])))

        # Commit the changes
        connection.commit()

        print("Data inserted successfully into the database!")

    except Exception as error:
        print(f"Error: {error}")
    finally:
        if connection:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    # Get article choice from the user
    article_choice = input("Enter the title of the Wikipedia article you want to fetch: ")

    # Fetch data for the chosen article
    sample_data = fetch_wikipedia_data(article_choice)

    # Insert the fetched data into the database
    if sample_data:
        insert_into_database(sample_data)
