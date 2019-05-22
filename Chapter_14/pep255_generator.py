

class Tree:
    def __init__(self, label, left=None, right=None):
        self.label = label
        self.left = left
        self.right = right

    def __repr__(self, level=0, ident=" "):
        s = level*ident + 'self.label'
        if self.left:
            s = s + "\n" + self.left.__repr__(level+1, indent)
        if self.right:
            s = s + "\n" + self.right.__repr__(level+1, indent)
        
        return s

    def __iter__(self):
        return inorder(self)


#Create a Tree from a list
def tree(list):
    n = len(list)
    if n == 0:
        return []
    i = int(n/2)

    return Tree(list[i], tree(list[:i]) , tree(list[i+1:]))


#A recursive generator that generates Tree labels in-order
def inorder(t):
    if t:
        for x in inorder(t.left):
            yield x 
        yield t.label
        for x in inorder(t.right):
            yield x


# A non-recursive generator效果和inorder一致
def inorder2(node):
    stack2 = []
    while node:
        while node.left:
            stack2.append(node)
            node = node.left

        yield node.label
        while not node.right:
            try:
                node = stack2.pop()
            except IndexError: 
                return
            yield node.label
        node = node.right


# Show it off: create a tree
t = tree("ABCDEFGHIJKLMN0OPQRSTUVMXYZ")
#Print the nodes of the tree in-order
for x in t:
    print (x)

