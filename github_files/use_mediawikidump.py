from mediawiki_dump.dumps import WikipediaDump, LocalFileDump
from mediawiki_dump.reader import DumpReader, DumpReaderArticles
import json
import argparse

parser = argparse.ArgumentParser(description='parse XML files with mediawiki-dump python package into JSON')
parser.add_argument('-f', '--filenames', type=str, help='name of data file', nargs=1, required=True)
args = parser.parse_args()

# Load the dump
dump = LocalFileDump(dump_file=args.filenames[0]) 
reader = list(DumpReaderArticles().read(dump))

data = []

# Process each page in the dump
for page in reader:
    title = page.title
    text = page.content
    #links = [link.title for link in page.links()]
    
    data.append({
        'title': title,
        'text': text#,
        #'links': links
    })

# Save the data to a JSON file
with open('enwiki_articles12_xmlconversion_mwd.json', 'w') as f:
    json.dump(data, f)
