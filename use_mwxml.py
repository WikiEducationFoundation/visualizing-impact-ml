import datetime
import mwxml
import mwparserfromhell
import argparse

import psycopg2
from populate_database import insert_into_bulk_database

now = datetime.datetime.now()

BULK_SIZE = 1000

# Parser for manually entering a local XML article file
parser = argparse.ArgumentParser(description='parse XML files with mwxml python package to format the XML data into python objects')
parser.add_argument('-f', '--filenames', type=str, help='name of XML data file', nargs=1, required=True)
args = parser.parse_args()

# Process XML article into a mwxml iterator
dump = mwxml.Dump.from_file(open(args.filenames[0]))

connection = psycopg2.connect(database="wikivi")
cursor = connection.cursor()

bulk_data = []

# Iterate through each article in the dump
for page in dump.pages:
    wikiid = page.id
    title = page.title
    revision_of_interest = next(page)
    content = revision_of_interest.text
    parsed_content = mwparserfromhell.parse(content).strip_code()

    bulk_data.append((wikiid, title, content, parsed_content))
    if len(bulk_data) >= BULK_SIZE: 
        insert_into_bulk_database(cursor, bulk_data)
        bulk_data = []

# If there's any remaining data, insert it
if bulk_data:
    insert_into_bulk_database(cursor, bulk_data)

cursor.close()
connection.commit()
connection.close()

now2 = datetime.datetime.now()
elapsed = now2 - now
print(elapsed.total_seconds())