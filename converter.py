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

class Tag:
    def __init__(self, html_tag):
        self.html_tag = html_tag

    def wrap_tag(self):
        return '<{} class="why-article">{}</{}>' % {self.html_tag, self.content, self.html_tag}

    def add_content(self, content):
        self.content = content

    def get_content(self):
        return self.content

    def elim_notation(self):
        self.content = self.content[1:len(self.content)-1]

class Header(Tag):
    def __init__(self):
        super().__init__('h')
        self.level = 0

    def add_level(self):
        self.level += 1
        self.html_tag = 'h' + str(self.level)

    def get_level(self):
        return self.level

class Link(Tag):
    def __init__(self, link):
        super().__init__('a')
        self.link = link

    def wrap_tag(self):
        return '<{} href=\'{}\'>{}</{}>' % {self.html_tag, self.content, self.html_tag}

class Formatted(Tag):
    def __init__(self):
        super().__init__('prefor')

    # everything else within-bounds of this tag will be accepted as content

class Escape():
    def __init__(self, esc_char):
        self.char = esc_char

def make_header(line):
    header = Header()
    limit = 6
    count = 0
    while count < limit:
        if line[count] == '#':
            header.add_level()
            count += 1
        else:
            break
    
    header.add_content(line[(count+1):])

    return header

# make a stack for every element we're converting
def analyze_line(line):
    specials = ['#', '*', '_', '[', ']', '(', ')']
    # [Bold, Italics, Link, Preformatted]
    used = [False, False, False, False]
    output = [] # stack

    # if this line is just a newline... 
    if line[0] == '\n':
        output += line
        return output
    # if this line is a header...
    elif line[0] == '#':
        header = make_header(line)
    else:
        # make a new paragraph
        output.append(Tag('p'))

    for char in line:
        if char in specials:
            if char == used[len(used - 1)]:
                # create object 
                x = 1

def convert():
    path = argv[1]
    file_ops = FileOps(path)
    file_ops.open_files()
    
    output = []
    for line in file_ops.content:
        output.append(analyze_line(line))

    # write output to file
    # return and exit