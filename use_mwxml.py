import mwxml
import argparse
from populate_database import insert_into_database

parser = argparse.ArgumentParser(description='parse XML files with mwxml python package to format the XML data into python objects')
parser.add_argument('-f', '--filenames', type=str, help='name of XML data file', nargs=1, required=True)
args = parser.parse_args()

dump = mwxml.Dump.from_file(open(args.filenames[0]))
i = 0
for page in dump.pages:
    revision_of_interest = next(page)
    title = revision_of_interest.title
    text = revision_of_interest.text
    wikiid = revision_of_interest.id
    id = i
    i += 1
    insert_into_database(id, title, text)
