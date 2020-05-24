import ebooklib
from ebooklib import epub
from Extract.htmlparser import MyHTMLParser
import re
from glob import glob
import threading

class Extractor:
    book = epub.EpubBook()
    lock = threading.Lock()
    total_items = 0

    def __init__(self, path_to_book, total_items=0):
        self.book = epub.read_epub(path_to_book)
        self.total_items += total_items


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


    def get_all_chapters_from_directory(self, path: str):
        """HELPER: returns a list of all html files in the path specified"""
        all_chapters = glob(path)
        return all_chapters


    def sort_chapters(self, path: str):
        """creates and returns a sorted list of all items in directory specified by path"""
        all_chapters = self.get_all_chapters_from_directory(path)
        all_chapters.sort(key=lambda f: int(re.sub('\\D', '', f)))
        return all_chapters


    def extract_raw_content(self, chapter) -> list:
        """place each paragraph of a chapter in a list and return it"""
        raw = []
        with open(chapter, "r") as chap:
            raw = chap.readlines()
        return raw


    def extract_tags(self, chapter) -> list:
        """REDUNDANT: return a list of all unique tags in a chapter""" 
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


    def extract_text_chapter(self, chapters: list, valid_chapters: list) -> list:
        """returns a list of only the text chapters and not ToC, title etc"""
        pure_chapters = []
        for html_file in chapters:
            # for each chapter, extract raw content
            raw_content = self.extract_raw_content(html_file)
            parsed = self.clean_raw_content(raw_content)
            if len(parsed) > 0:
                if re.sub("\\d", "", (parsed[0].lower().replace(" ", ""))) in valid_chapters: 
                    pure_chapters.append(parsed)
        return pure_chapters


    def save_content(self, paragraph: str, splitter, filename):
        """create or open file (list of words) and append new words to it"""
        with open(f"docs\\word-list\\{filename}.txt", "a") as w:
            for word in paragraph.split(splitter):
                w.write(f"{self.format_text(word)};")
                self.total_items += 1


    def get_total_items(self):
        """returns the object in question's total word count (words it has saved)"""
        return self.total_items


    def debug_list_print_items(self, print_list: list):
        for item in print_list:
            print(item)


    def debug_list_print_stats(self, print_list: list):
        print(f"length: {len(print_list)}")
        for item in print_list:
            print(item, '\n')

