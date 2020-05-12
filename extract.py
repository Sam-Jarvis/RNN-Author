import ebooklib
import pickle
import string
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
        try:
            self.start_tag += f"{tag} {attrs[0][0]} {attrs[0][1]}"
        except(IndexError):
            self.start_tag += f"{tag}"

    def handle_endtag(self, tag):
        self.end_tag += tag

    def handle_data(self, data):
        self.data += data


def extract_book(path):
    return epub.read_epub(path)
    # book = epub.read_epub('WoT1.epub')


def extract_chapters(book):
    """finds all items marked 'chapter' in a book and appends them to a list which it returns"""
    documents = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            if item.is_chapter():
                documents.append(item)
    return documents


def export_chapters(html_parts):
    """creates an html file in /html-chapters for each item in html_parts"""
    counter = 0
    for part in html_parts:
        with open(f'html-chapters/html-chapter{counter}.html', 'w') as current_chap:
            current_chap.write(part.get_content().decode())
        counter += 1


def extract_raw_content(chapter):
    """place each paragraph of a chapter in a list and return it"""
    raw = []
    with open(chapter, "r") as chap:
        raw = chap.readlines()
    return raw


def clean_raw_content(raw_content):
    """parse raw html and return a list of clean text paragraphs"""
    parser = MyHTMLParser()
    parsed = []
    for line in raw_content:
        parser.feed(line)
        clean = parser.data
        clean = format_text(clean)
        if clean != "":
            parsed.append(clean)
        parser.reset_data()
    return parsed


def format_text(text):
    """takes a string and replaces unknown characters found in it"""
    text = text.replace("”", "\"")
    text = text.replace("“", "\"")
    text = text.replace("’", "\'")
    text = text.replace("\n", "")
    text = text.replace("  ", "")
    text = text.replace("—", "-")
    return text


def save_words(paragraph):
    """create or open file (list of words) and append new words to it"""
    with open("word-list\\words.txt", "a") as w:
        for word in paragraph.split(" "):
            w.write(f"{format_text(word)}\n")


def debug_list_print_items(print_list):
    for item in print_list:
        print(item)


def debug_list_print_stats(print_list):
    print(f"length: {len(print_list)}")
    print(print_list)


# if __name__ == "__main__":
    # print("start: ", parser.start_tag, "\nend: ", parser.end_tag, "\ndata: ", parser.data)
    # todo: if /html-chapters is empty, run export_chapters, otherwise don't
    # chapters = extract_chapters(book)

    # paragraph = extract_raw_content("html-chapters\\html-chapter5.html")
    # parsed = clean_raw_content(paragraph)
    #debug_list_print_stats(parsed)
    # for i in range(0,3):
    #     save_words(parsed[i])

