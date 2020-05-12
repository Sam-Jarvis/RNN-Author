## PROBLEMS TO SOLVE
1) (SOLVED) What should be done with the parsed data? How is it stored / handled? 
2) (SOLVED) How do I properly parse the whole file? Maybe parse each line? 
3) Double spacing
4) (SOLVED DIRTILY) Beginning / end tags with no data, just tags
5) Short tags that have fewer / no attributes error out

## GENERAL NOTES
Each paragraph is a <div class="fmtx1"> or <div class="fmtx"> tag

<div class="calibre6"> <br class="calibre6"/></div>
<div class="calibre6"> <br class="calibre6"/></div>

## ORDER OF OPERATION
1) extract_chapters: finds all items marked 'chapter' in a book and appends them to a list which it returns
2) export_chapters: creates an html file in /html-chapters for each item in html_parts
3) extract_raw_content: place each paragraph of a chapter in a list and return it
4) clean_raw_content: parse raw html and return a list of clean text paragraphs
5) format_word: takes a string and replaces unknown characters found in it
6) save_words: create or open file (list of words) and append new words to it