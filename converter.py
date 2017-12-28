#!/usr/local/bin/python3
from sys import argv

class FileOps:
    def __init__(self, path):
        self.in_path = path
        self.out_path = path.split('.')[0] + '.html'

    def get_location(self):
        return self.in_path

    def open_files(self):
        self.in_file = open(self.in_path, 'r')
        self.out_file = open(self.out_path, 'w')
        with open(self.in_path) as f:
            self.content = f.readlines

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
        self.html_tag = html_tag

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

def begin_conversion():
    path = argv[1]
    file_ops = FileOps(path)
    file_ops.open_files()

    specials = ['#', '*', '_', '[', ']', '(', ')']
    
    stack = []
    for line in file_ops.content:
        for char in line:
            if char in specials:
                