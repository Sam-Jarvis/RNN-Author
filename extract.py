import ebooklib
import pickle
from ebooklib import epub
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    start_tag = ""
    end_tag = ""
    data = ""

    def reset_data(self):
        self.start_tag = ""
        self.end_tag = ""
        self.data = ""

    def handle_starttag(self, tag, attrs):
        self.start_tag += f"{tag} {attrs[0][0]} {attrs[0][1]}"

    def handle_endtag(self, tag):
        self.end_tag += tag

    def handle_data(self, data):
        self.data += data


book = epub.read_epub('WoT1.epub')

def export_chapters(html_parts):
    """creates an html file in /html-chapters for each item in html_parts"""
    counter = 0
    for part in html_parts:
        with open(f'html-chapters/html-chapter{counter}.html', 'w') as current_chap:
            current_chap.write(part.get_content().decode())
        counter += 1


def extract_chapters(book):
    """finds all items marked 'chapter' in a book and appends them to a list which it returns"""
    documents = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            if item.is_chapter():
                documents.append(item)
    return documents


def extract_content(chapter):
    """place each paragraph of a chapter in a list and return it"""
    lines = []
    with open(chapter, "r") as chap:
        lines = chap.readlines()
    return lines


def extract_words(paragraph):
    """create or open file (list of words) and append new words to it"""
    with open("word-list\\words.txt", "a") as w:
        paragraph_len = len(paragraph)
        for word in paragraph.split(" "):
            if "/n" in word:
                w.write(f"{word}")
            else:
                w.write(f"{word}\n")


def debug_list_print_items(print_list):
    for item in print_list:
        print(item)


def debug_list_print_stats(print_list):
    print(f"length: {len(print_list)}")
    print(print_list)


if __name__ == "__main__":
    # print("start: ", parser.start_tag, "\nend: ", parser.end_tag, "\ndata: ", parser.data)
    # todo: if /html-chapters is empty, run export_chapters, otherwise don't
    chapters = extract_chapters(book)
    print(f"{len(chapters)} chapters")

    parser = MyHTMLParser()
    paragraph = extract_content("html-chapters\\html-chapter5.html")

    parser.feed(paragraph[15])
    extract_words(parser.data)
    parser.reset_data()

    parser.feed(paragraph[16])
    extract_words(parser.data)
    parser.reset_data()

# PROBLEMS TO SOLVE
# 1) What should be done with the parsed data? How is it stored / handled?
# 2) How do I properly parse the whole file? Maybe parse each line?

# GENERAL NOTES
# Each paragraph is a <div class="fmtx1"> or <div class="fmtx"> tag