import extract
import glob
from os import listdir
import concurrent.futures
import time

book = extract.extract_book("WoTcs.epub")

# chapters = extract.extract_chapters(book)
# extract.export_chapters(chapters)
#print(glob.glob("/home/adam/*.txt"))
all_chapters = glob.glob("html-chapters/*.html")

t1 = time.perf_counter()
for html_file in all_chapters:
    # for each chapter, extract raw content
    raw_content = extract.extract_raw_content(html_file)
    parsed = extract.clean_raw_content(raw_content)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(extract.save_words, parsed)
t2 = time.perf_counter() 

print(f"Elapsed time: {t2 - t1} seconds")
