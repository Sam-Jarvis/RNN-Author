import extract
from os import listdir

book = extract.extract_book("WoTcs.epub")

# chapters = extract.extract_chapters(book)
# extract.export_chapters(chapters)

all_chapters = listdir("html-chapters/")

