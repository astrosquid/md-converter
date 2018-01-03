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
        # print("Pushing into the stack: " + element.__class__.__name__)
        self.stack.append(element)

    def pop(self):
        """Pop an element off the top of the stack."""
        elem = self.stack[-1]
        del self.stack[-1]
        #print("Popping off the stack: " + elem.__class__.__name__)
        return elem

    def peek(self):
        """See the most recent item on the stack."""
        return self.stack[-1]

    def empty(self):
        if not self.stack:
            return True
        return False

class Tag():
    """General HTML tag class. Works for simple tags like bold (b) and italics (i)."""
    def __init__(self, html_tag):
        self.html_tag = html_tag
        self.content = ""

    def get_tag(self):
        """Return the HTML string tag as a literal."""
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
    def __init__(self):
        super().__init__('a')
        self.link = ''
        self.content_finished = False

    def set_href(self, link):
        self.link = link

    def finished_content(self):
        self.content_finished = True

    def add_content(self, content):
        if self.content_finished():
            self.link += content
        else:
            self.content += content

    def wrap_tag(self):
        return '<{} href=\'{}\'>{}</{}>' % {self.html_tag, self.link, self.content, self.html_tag}

    def elim_notation(self):
        # TODO
        # modify this to look for:
        # the first and last parens before the first open bracket
        # the first open bracket and last close bracket after the parens
        pass

class Parens():
    """Should delete, no longer needed."""
    def __init__(self):
        self.content = ""

    def add_content(self, content):
        self.content += content

    def no_parens(self):
        return self.content[1:len(self.content)-1]

class Preformatted(Tag):
    def __init__(self):
        super().__init__('pre')

    # everything else within-bounds of this tag will be accepted as content

class Escape():
    """Used to denote the existence of an escaped character."""
    def __init__(self):
        pass

class Analyzer:
    def __init__(self):
        self.output = Stack()

    def decide_tag(self, char):
        if char == '*':
            return Tag('b')
        elif char == '_':
            return Tag('i')
        elif char == '[':
            return Link()

        sys.exit(1)

    def is_ending_tag(self, char, tag):
        # print('Passed to ending checker: ' + char + tag)
        ending_tags = {
            'b' : '*',
            'i' : '_',
            'a' : ')',
            'pre' : '```',
            'tt' : '`'
        }

        if tag in ending_tags.keys():
            if ending_tags[tag] == char:
                return True

        return False

    def analyze_line(self, line):
        """Create HTML string literal of the line passed in."""
        #specials = ['*', '_', '[', ']', '(', ')', '`']
        beginnings = ['*', '_', '[', '`']

        if line[0] == '#':
            # Make a header...
            header = Header(line)
            self.output.push(header)
            # TODO: Eliminate group of # at beginning of line.
            for char in line:
                if char == '#':
                    line = line[1:]
                else:
                    break
        elif line[0] == '\n':
            # TODO: make a line break (new class, no content) and return
            pass
        else:
            # ...or make a new paragraph.
            self.output.push(Tag('p'))

        block = ""

        for char in line:
            if not self.output.empty() and self.output.peek().__class__.__name__ == 'Escape':
                self.output.pop()
                self.output.peek().add_content(char)
                continue

            if char in beginnings:
                # New element to stack.
                self.output.push(self.decide_tag(char))
            elif not self.output.empty() and self.is_ending_tag(char, self.output.peek().get_tag()):
                # wrap up this element, append to last element's content
                elem = self.output.pop()
                self.output.peek().add_content(elem.wrap_tag())
            elif char == '\\':
                self.output.push(Escape())
            elif char == '\n':
                # End this line.
                block += self.output.pop().wrap_tag()
            else:
                self.output.peek().add_content(char)

        return block

    def convert(self):
        # TODO: add a newline to the end of the md file.
        path = argv[1]
        out_path = path.split('.')[0] + '.html'

        output = []

        with open(path) as f:
            for line in f:
                output.append(self.analyze_line(line))

        out_file = open(out_path, 'w')
        for line in output:
            out_file.write(line)
            out_file.write('\n')
            out_file.write('\n')
        out_file.close()

if __name__ == '__main__':
    analyzer = Analyzer()
    analyzer.convert()
