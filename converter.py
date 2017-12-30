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

    def add_content(self, content):
        self.content = content

class Header(Tag):
    def __init__(self):
        super().__init__()
        self.level = 0

    def add_level(self):
        self.level += 1

    def get_level(self):
        return self.level

class Link(Tag):
    def __init__(self, link):
        super().__init__()
        self.link = link
        self.html_tag = 'a'

    def wrap_tag(self):
        return '<{} href=\'{}\'>{}</{}>' % {self.html_tag, self.content, self.html_tag}

def make_header(line):
    header = Header()
    limit = 6
    count = 0
    while count < limit:
        if line[count] == '#':
            header.add_level()
            count += 1
        else 
            break
    
    header.add_content(line[(count+1):])

    return header

# make a stack for every element we're converting
def analyze_line(line):
    specials = ['#', '*', '_', '[', ']', '(', ')']
    used = [] # stack
    output = [] # stack

    # if this line is just a newline... 

    # if this line is a header...
    if line[0] == '\n':
        output += line
        return output
    elif line[0] == '#':
        header = make_header(line)
    
    for char in line:
        if char in specials:
            if char == used[len(used - 1)]:
                # create object 
                x = 1

def convert():
    path = argv[1]
    file_ops = FileOps(path)
    file_ops.open_files()
    
    stack = []
    for line in file_ops.content:
        analyze_line(line)