import datetime
import mwxml
import argparse
from populate_database import insert_into_database

now = datetime.datetime.now()

# Parser for manually entering a local XML article file
parser = argparse.ArgumentParser(description='parse XML files with mwxml python package to format the XML data into python objects')
parser.add_argument('-f', '--filenames', type=str, help='name of XML data file', nargs=1, required=True)
args = parser.parse_args()

# Process XML article into a mwxml iterator
dump = mwxml.Dump.from_file(open(args.filenames[0]))

# Iterate through each article in the dump
for page in dump.pages:
    wikiid = page.id
    title = page.title
    revision_of_interest = next(page)
    text = revision_of_interest.text
    # Populate the database
    insert_into_database(wikiid, title, text)

now2 = datetime.datetime.now()
elapsed = now2 - now
print(elapsed.total_seconds())