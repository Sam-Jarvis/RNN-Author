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