import re

pat = re.compile(r"(\S+)|(<[^>]*>)")
text = "<foo> This is a <b> foo file </b> you know. </foo>"

# Version 2 - Push-mode, recursive generators
def run():
    parser = parse_items()
    next(parser)
    try:
        for m in pat.finditer(text):
            token = m.group(0)
            print('Feeding', repr(token))
            parser.send(token)
        parser.send(None) # to signal EOF
    except StopIteration as e:
        tree = e.value
        print(tree)

def parse_elem(opening_tag):
    name = opening_tag[1:-1]
    closing_tag = "</%s>" % name
    items = yield from parse_items(closing_tag)
    return (name, items)

def parse_items(closing_tag=None):
    elems = []
    while 1:
        token = yield 
        if not token:
            break # EOF
        if is_opening_tag(token):
            '''
            作者原来用的是elems.append(yield from parse_elem(token))
            可能是写该问的时候yield from还没完成，只是提出来了，
            会报错，因此这里进行了拆分。

            这里用了递归调用yield from,实际运行中，外部client每次send都只会运行一个yield
            ，所以当前可能suspend在递归调用中很深层次的yield。
            '''
            e = yield from parse_elem(token)
            elems.append(e)
        elif token == closing_tag:
            break
        else:
            elems.append(token)
    return elems

def is_opening_tag(token):
    return token.startswith("<") and not token.startswith("</")

run()
