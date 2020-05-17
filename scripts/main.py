from Extract.extract import Extractor
from Extract import progressbar as pb
import os
import concurrent.futures
import time

HTML_CHAPTERS = "docs\\html-chapters"
VALID_HEADINGS = ["chapter", "epilogue", "prologue", "glossary"]

os.chdir("docs")
extractor = Extractor("WoTcs.epub")
os.chdir("..")

epub_chapters = extractor.extract_chapters(extractor.book)
extractor.export_chapters(epub_chapters, HTML_CHAPTERS)
sorted_chapters = extractor.sort_chapters(f"{HTML_CHAPTERS}\\*.html")
pure = extractor.extract_text_chapter(sorted_chapters, VALID_HEADINGS)

total_chapters = len(pure)
print(f"Total chapters: {total_chapters}")

t1 = time.perf_counter()
for i in pb.progressbar(range(total_chapters), "Processing: ", 40):
    for paragraph in pure[i]:
        extractor.save_words(paragraph)
t2 = time.perf_counter() 

print(f"Elapsed time: {t2 - t1} seconds")
print(f"Total words: {extractor.get_total_words()}")
