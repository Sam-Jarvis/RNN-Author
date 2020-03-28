import ebooklib
from ebooklib import epub

book = epub.read_epub('WoT1.epub')

for item in book.get_items():
    if item.get_type() == ebooklib.ITEM_DOCUMENT:
        print('==================================')
        print('NAME : ', item.get_name())
        print('----------------------------------')
        # print(item.get_body_content())
        # print('==================================')