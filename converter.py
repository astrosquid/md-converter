#!/usr/local/bin/python3
from sys import argv
import sys

class Stack:
    """Quick stack implementation using a Python list."""
    stack = []

    def __init__(self):
        pass

    def push(self, element):
        """Push an element to the top of the stack."""
        print("Pushing into the stack: " + element.__class__.__name__)
        self.stack.append(element)

    def pop(self):
        """Pop an element off the top of the stack."""
        elem = self.stack[-1]
        del self.stack[-1]
        print("Popping off the stack: " + elem.__class__.__name__)
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

    def get_content(self):
        return self.content

class Tag():
    def __init__(self, html_tag):
        self.html_tag = html_tag
        self.content = ""

    def get_tag(self):
        return self.html_tag
    
    def wrap_tag(self):
        """Create HTML representation of self."""
        return '<{} class="why-article">{}</{}>'.format(self.html_tag, self.content, self.html_tag)

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
        self.level = 0
        limit = 6
        while self.level < limit:
            if line[self.level] == '#':
                self.add_level()
            else:
                break

    def add_level(self):
        self.level += 1

    def get_level(self):
        return self.level

    def wrap_tag(self):
        self.html_tag = self.html_tag + str(self.level)
        return super().wrap_tag()

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

class Parens():
    def __init__(self):
        self.content = ""

    def add_content(self, content):
        self.content += content

    def no_parens(self):
        return self.content[1:len(self.content)-1]

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
        return Link("")

    print(char + " is not special, aborting.")
    sys.exit(1)

def is_ending_tag(char, tag):
    print('Passed to ending checker: ' + char + tag)
    ending_tags = {
        'p' : '\n',
        'h' : '\n',
        'b' : '*',
        'i' : '_',
        'a' : ']'
    }

    if tag in ending_tags.keys():
        if ending_tags[tag] == char:
            return True

    return False

def analyze_line(line):
    """Create HTML string literal of the line passed in."""
    markdown = {
        '#' : '\n',
        '*' : '*',
        '_' : '_',
        '[' : ']',
        '(' : ')'
    }

    specials = ['*', '_', '[', ']', '(', ')']
    output = Stack() # stack

    if line[0] == '#':
        # Make a header...
        header = Header(line)
        output.push(header)
        # Eliminate group of # at beginning of line.
    elif line[0] == '\n':
        # TODO: make a line break (new class, no content) and return
        pass
    else:
        # ...or make a new paragraph.
        output.push(Tag('p'))

    block = ""

    for char in line:
        if char in specials:
            # is this the ending to the elem on the top of the stack?
            if is_ending_tag(char, output.peek().get_tag()):
                # wrap up this element, append to last element's content
                # output.peek().add_content(char)
                elem = output.pop()
                output.peek().add_content(elem.wrap_tag())
            else:
                output.push(decide_tag(char))
        elif char == '\n':
            block += output.pop().wrap_tag()
        else:
            output.peek().add_content(char)

    return block

def list_to_str(l):
    x = ""
    for y in l:
        x += y
    
    return x

def convert():
    path = argv[1]
    out_path = path.split('.')[0] + '.html'
    
    output = []

    with open(path) as f:
        for line in f:
            output.append(analyze_line(line))

    out_file = open(out_path, 'w')
    for line in output: 
        out_file.write(line)
    out_file.write('\n')
    out_file.close()

convert()
