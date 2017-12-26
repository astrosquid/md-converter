#!/usr/local/bin/python3

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

    def wrap_tag(self, tag, content):
        return '<{}>{}</{}>' % {tag, content, tag}

class Header:
    def __init__(self, level):
        self.level = level
        self.html_tag = 'h'

class Paragraph:
    def __init__(self):
        self.html_tag = 'p'

class Italics:
    def __init__(self):
        self.html_tag = 'i'

class Bold:
    def __init__(self):
        self.html_tag = 'b'

class Link:
    def __init__(self):
        self.html_tag = 'b'