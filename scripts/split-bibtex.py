"""
This script performs the following functions:

1. splits the content of a BibTeX file into
   multiple files, one per entry (in its own directory).
2. it creates the "index.md" file in for each entry.
   At this point the date is not copied from the bibtex
   entry. This can be done in the future.
"""

import os
import re
C_index_md_content="+++\ndate=2000-01-01\n[extra]\ntype={}\n+++\n"


def split_bibtex_file(input_file_path, output_directory_path):
    if not os.path.exists(output_directory_path):
        os.makedirs(output_directory_path)

    with open(input_file_path, 'r', encoding="UTF-8") as input_file:
        bibtex_entries = re.split(r'(?<=\n\n)', input_file.read())

    for entry in bibtex_entries:
        match = re.search(r'@(\w+){\s*([\w_\-]+),', entry)
        if match:
            entry_type = match.group(1)
            entry_key = match.group(2)
            entry_directory_path = os.path.join(output_directory_path, f'{entry_key}')
            if not os.path.exists(entry_directory_path):
                os.makedirs(entry_directory_path)
            output_file_path = os.path.join(entry_directory_path, f'{entry_key}.bib')
            with open(output_file_path, 'w') as output_file:
                output_file.write(entry)
        
        if entry_type == "Patent":
            publication_type = "patents"
        elif entry_type == "Article":
            publication_type = "journals"
        else:
            publication_type = "conferences"
        publication_type = '"' + publication_type + '"'
        with open(os.path.join(entry_directory_path,"index.md"),"w") as f:
            f.write(C_index_md_content.format(publication_type))

if __name__ == '__main__':
    split_bibtex_file("_bib/papers.bib", "content/papers")
    split_bibtex_file("_bib/patents.bib", "content/patents")

