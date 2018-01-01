#!/usr/local/bin/python3
from sys import argv

class Stack:
    """Quick stack implementation using a Python list."""
    stack = []

    def __init__(self):
        pass

    def push(self, element):
        """Push an element to the top of the stack."""
        self.stack.append(element)

    def pop(self):
        """Pop an element off the top of the stack."""
        elem = self.stack[-1]
        del self.stack[-1]
        return elem

    def peek(self):
        """See the most recent item on the stack."""
        return self.stack[-1]

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
        self.content = ""

    def wrap_tag(self):
        """Create HTML representation of self."""
        return '<{} class="why-article">{}</{}>' % {self.html_tag, self.content, self.html_tag}

    def add_content(self, content):
        """Add string literal content to self."""
        self.content += content

    def get_content(self):
        """Return string literal content."""
        return self.content

    def elim_notation(self):
        """Permanently eliminate markdown notation; careful when using for Link class."""
        self.content = self.content[1:len(self.content)-1]

    def no_notation(self):
        """Create and return string literal content without markdown notation."""
        return self.content[1:len(self.content)-1]

class Header(Tag):
    def __init__(self, line):
        super().__init__('h')
        # TODO: can probably cut out 'count' here
        self.level = 0
        limit = 6
        while self.level < limit:
            if line[self.level] == '#':
                self.add_level()
            else:
                break

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
        # TODO: fix this
        return '<{} href=\'{}\'>{}</{}>' % {self.html_tag, self.content, self.html_tag}

    def elim_notation(self):
        # TODO
        # modify this to look for:
        # the first and last parens before the first open bracket
        # the first open bracket and last close bracket after the parens
        pass

class Formatted(Tag):
    def __init__(self):
        super().__init__('prefor')

    # everything else within-bounds of this tag will be accepted as content

class Escape():
    def __init__(self, esc_char):
        self.char = esc_char

def decide_tag(char):
    if char == '*':
        return Tag('b')
    elif char == '_':
        return Tag('i')
    elif char == '[':
        return Link()

def analyze_line(line):
    """Create HTML string literal of the line passed in."""
    markdown = {
        '#' : '\n',
        '*' : '*',
        '_' : '_',
        '[' : ']',
        '(' : ')'
    }
    specials = ['#', '*', '_', '[', ']', '(', ')']
    output = [] # stack

    # If this line is just a newline... 
    if line[0] == '\n':
        # ...add it to output and return...
        output += line
        return output
    elif line[0] == '#':
        # ...or, make a header...
        header = Header(line)
        output.append(header)
    else:
        # ...or make a new paragraph.
        output.append(Tag('p'))

    for char in line:
        if char in specials:
            # is this a new element?
            if char == output.last:
                # wrap up this element, append to last element's content
                pass
            else:
                tag = decide_tag(char)
        else:
            output.append(char)

def convert():
    path = argv[1]
    file_ops = FileOps(path)
    file_ops.open_files()
    
    output = []
    for line in file_ops.content:
        output.append(analyze_line(line))

    # write output to file
    # return and exit