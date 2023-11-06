"""
 Parses the entries in a bibtex file and creates one 
 markdown (.md) file per entry
"""

import os
from datetime import datetime
import bibtexparser

def quote_string(s):
    return '"' + s + '"'

def normalize_date (input_date_string):
    # normalize the date string. Supply Mising fields
    try:
        dt = datetime.strptime(input_date_string, "%Y-%m-%d")
    except:
        try:
            dt = datetime.strptime(input_date_string,"%Y-%m")
            dt.replace(day=1)
        except:
            try:
                dt = datetime.strptime(input_date_string,"%Y")
                dt.replace (month=1, day=1)
            except:
                print ("Invalid Date field")
                return ("1900-01-01")
    return (dt.strftime("%Y-%m-%d"))

def extract_bibtex_entries (bibtex_file_name, output_dir):

    # Check if the output_dir exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Load the BibTeX file
    with open(bibtex_file_name) as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)

    # Loop through each entry in the BibTeX file
    for entry in bib_database.entries:
        # Get the BibTeX key for the entry
        key = entry['ID']

        # Create a new Markdown file for the entry
        filename = os.path.join(output_dir, f'{key}.md')
        with open(filename, 'w') as f:
            # Write the front matter for the Markdown file
            f.write('+++\n')

            title = entry['title'].replace('\n', ' ')
            f.write(f"title = \"{title}\"\n")
            date = normalize_date(entry['date'])
            f.write(f"date = {date}\n")

            f.write('[extra]\n')
            authors = entry['author'].replace('\n', ' ').split(" and ")
            authors = ",".join(list(map(quote_string, authors)))
            f.write(f"authors = [{authors}]\n")

            match entry['ENTRYTYPE'].lower():
                case "article":
                    publication = entry['journaltitle'] 
                    if 'volume' in entry:
                        publication = publication + "," + entry['volume']
                    if 'number' in entry:
                        publication = publication + "(" + entry['number'] + ")"
                    if 'pages' in entry:
                        publication = publication + ", pp." + entry['pages'] + "."
                    type = "journals"
                case "inproceedings":
                    publication = entry['booktitle'] + ", pp." + entry['pages']
                    type = "conferences"
                case "patent":
                    publication = "US Patent: " + entry['number']
                    type = "patents"
                case _:
                    print ("Unknown bibentry type:", entry['ENTRYTYPE'])
                    type = "unknown"
            publication = publication.replace('\n', ' ')
            f.write(f"publication = \"{publication}\"\n")
            f.write(f"type = \"{type}\"\n")
            f.write('+++\n\n')

            # Write the content of the publication to the Markdown file
            if "abstract" in entry:
                f.write(f'{entry["abstract"]}\n')

if __name__ == "__main__":
    extract_bibtex_entries ("_bib/papers.bib", "content/papers2")

