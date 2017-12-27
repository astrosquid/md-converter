#!/usr/local/bin/python3
from sys import argv

class FileOps:
    def __init__(self, path):
        self.path = path

    def get_location(self):
        return self.path

    def open_file(self):
        self.in_file = open(self.path, 'r')
        self.out_file = open(self.path, 'w')

    def write(self, content):
        self.out_file.write(content)

    def close_files(self):
        self.in_file.close()
        self.out_file.close()

class TagFormatter:
    def __init__(self):
        return

class Tag:
    def __init__(self, html_tag, content):
        self.content = content

    def wrap_tag(self):
        return '<{}>{}</{}>' % {self.html_tag, self.content, self.html_tag}

class Header(Tag):
    def __init__(self, level):
        super().__init__()
        self.level = level

class Link(Tag):
    def __init__(self, link):
        super().__init__()
        self.link = link
        self.html_tag = 'a'

    def wrap_tag(self):
        return '<{} href=\'{}\'>{}</{}>' % {self.html_tag, self.content, self.html_tag}

def convert():
    path = argv[1]
    fo = FileOps(path)
    