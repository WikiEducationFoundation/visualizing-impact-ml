import psycopg2
import mwparserfromhell
import datetime

now = datetime.datetime.now()

# Connect to the wikivi database
conn = psycopg2.connect(
    dbname='wikivi',
)

cursor = conn.cursor()

# Retrieve the content column
cursor.execute("SELECT id, content FROM wikipedia_data;")
rows = cursor.fetchall()

for row in rows:
    wiki_id, content = row
    # Parse the content using mwparserfromhell
    parsed_content = mwparserfromhell.parse(content).strip_code()
    
    # Update the table with the parsed content
    cursor.execute("UPDATE wikipedia_data SET parsed_content = %s WHERE id = %s;", (parsed_content, wiki_id))

# Commit the changes and close the connection
conn.commit()
cursor.close()
conn.close()

now2 = datetime.datetime.now()
elapsed = now2 - now
print(elapsed.total_seconds())
