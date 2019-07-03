# http://www.cosc.canterbury.ac.nz/greg.ewing/python/yield-from/yield_from.html
# Greg Ewing—who penned PEP 380 and implemented yield
# from in CPython—published a few examples of examples of yield from that did
# not depend on asyncio


# Version 1 - Pull-mode, recursive functions
import re

pat = re.compile(r"(\S+)|(<[^>]*>)")

def scanner(text):
    for m in pat.finditer(text):
        token = m.group(0)
        print('Feeding:', repr(token))
        yield token
    yield None # to signal EOF

text =  "<foo> This is a <b> foo file </b> you know. </foo>"
token_stream = scanner(text)

def parse_items(closing_tag=None):
    elems = []
    while 1:
        token = next(token_stream)
        if not token:
            break #EOF
        if is_opening_tag(token):
            elems.append(parse_elem(token))
        elif token == closing_tag:
            break
        else:
            elems.append(token)
    return elems

def is_opening_tag(token):
    return token.startswith("<") and not token.startswith("</")

def parse_elem(opening_tag):
    name = opening_tag[1:-1]
    closing_tag = "</%s>" % name
    items = parse_items(closing_tag)
    return (name, items)

tree = parse_items()
print(tree)
