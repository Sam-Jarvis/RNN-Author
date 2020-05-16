import ebooklib
import pickle
import string
import re
from glob import glob
from ebooklib import epub
from html.parser import HTMLParser
import threading

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


class Extractor:
    book = epub.EpubBook()
    lock = threading.Lock()
    total_words = 0

    def __init__(self, path_to_book, total_words=0):
        self.book = epub.read_epub(path_to_book)
        self.total_words += total_words

    # def extract_book(path):
    #     return epub.read_epub(path)
    #     # book = epub.read_epub('WoT1.epub')


    def extract_chapters(self, book: epub.EpubBook) -> list:
        """finds all items marked 'chapter' in a book and appends them to a list which it returns"""
        documents = []
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                if item.is_chapter():
                    documents.append(item)
        return documents


    def export_chapters(self, html_parts: list, path: str):
        """creates an html file in /html-chapters for each item in html_parts"""
        counter = 0
        for part in html_parts:
            with open(f'{path}/{counter}.html', 'w') as current_chap:
                current_chap.write(part.get_content().decode())
            counter += 1


    def sort_chapters(self, path: str):
        """creates and returns a sorted list of all items in directory specified by path"""
        all_chapters = glob(path)
        all_chapters.sort(key=lambda f: int(re.sub('\\D', '', f)))
        return all_chapters


    def extract_raw_content(self, chapter) -> list:
        """place each paragraph of a chapter in a list and return it"""
        raw = []
        with open(chapter, "r") as chap:
            raw = chap.readlines()
        return raw


    def extract_tags(self, chapter) -> list:
        """return a list of all unique tags in a chapter""" 
        parser = MyHTMLParser()
        tags = []
        for line in chapter:
            parser.feed(line)
            tag = parser.start_tag
            if tag not in tags:
                tags.append(tag)
            parser.reset_data()
        return tags


    def clean_raw_content(self, raw_content: list) -> list:
        """parse raw html and return a list of clean text paragraphs"""
        parser = MyHTMLParser()
        parsed = []
        for line in raw_content:
            parser.feed(line)
            clean = parser.data
            clean = self.format_text(clean)
            if clean != "":
                parsed.append(clean)
            parser.reset_data()
        return parsed


    def format_text(self, text: str) -> str:
        """takes a string and replaces unknown characters found in it"""
        text = text.replace("”", "\"")
        text = text.replace("“", "\"")
        text = text.replace("’", "\'")
        text = text.replace("\n", "")
        text = text.replace("  ", "")
        text = text.replace("—", "-")
        return text


    def save_words(self, paragraph: str, is_multithreaded=False):
        """create or open file (list of words) and append new words to it"""
        with open(f"docs\\word-list\\words.txt", "a") as w:
            if is_multithreaded:
                with self.lock:
                    for word in paragraph.split(" "):
                        w.write(f"{self.format_text(word)};")
                        self.total_words += 1
            else:
                for word in paragraph.split(" "):
                        w.write(f"{self.format_text(word)};")
                        self.total_words += 1


    def get_total_words(self):
        return self.total_words


    def debug_list_print_items(self, print_list: list):
        for item in print_list:
            print(item)


    def debug_list_print_stats(self, print_list: list):
        print(f"length: {len(print_list)}")
        for item in print_list:
            print(item, '\n')


# if __name__ == "__main__":
    # print("start: ", parser.start_tag, "\nend: ", parser.end_tag, "\ndata: ", parser.data)
    # todo: if /html-chapters is empty, run export_chapters, otherwise don't
    # chapters = extract_chapters(book)

    # paragraph = extract_raw_content("html-chapters\\html-chapter5.html")
    # parsed = clean_raw_content(paragraph)
    #debug_list_print_stats(parsed)
    # for i in range(0,3):
    #     save_words(parsed[i])

