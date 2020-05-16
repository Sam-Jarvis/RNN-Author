from extract import Extractor
import glob
import os
import concurrent.futures
import progress.bar
import time

#FOR TESTING. REMOVE
from ebooklib import epub

os.chdir("docs")
extractor = Extractor("WoTcs.epub")
os.chdir("..")

epub_chapters = extractor.extract_chapters(extractor.book)
extractor.export_chapters(epub_chapters, "docs\\html-chapters")

sorted_chapters = extractor.sort_chapters("docs\\html-chapters\\*.html")
total_chapters = len(sorted_chapters)

print(f"Total chapters: {total_chapters}")
# bar = progress.bar.IncrementalBar("Processing", max=total_chapters)

pure_chapters = []
chapter_headings = ["chapter", "epilogue", "prologue", "glossary"]
# t1 = time.perf_counter()
for html_file in sorted_chapters:
    # for each chapter, extract raw content
    raw_content = extractor.extract_raw_content(html_file)
    parsed = extractor.clean_raw_content(raw_content)
    if len(parsed) > 0:
        if parsed[0].lower().replace(" ", "") in chapter_headings:
            pure_chapters.append(html_file)

extractor.debug_list_print_stats(pure_chapters)
    # for paragraph in parsed:
    #     extractor.save_words(paragraph)
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     executor.map(extract.save_words, parsed)
    # bar.next()
# bar.finish()
# t2 = time.perf_counter() 

# print(f"Elapsed time: {t2 - t1} seconds")
# print(f"Total words: {extractor.get_total_words()}")
