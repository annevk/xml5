class Node(object):
    def __init__(self, name):
        """Node representing an item in the tree.
        parent - The parent of the current node (or None for the document node)
        childNodes - a list of child nodes of the current node. This must 
        """
        self.parent = None
        self.childNodes = []

    def __unicode__(self):
        raise NotImplementedError

    def appendChild(self, node):
        """Insert node as a child of the current node
        """
        raise NotImplementedError

    def insertText(self, data, insertBefore=None):
        """Insert data as text in the current node, positioned before the 
        start of node insertBefore or to the end of the node's text.
        """
        raise NotImplementedError

class TreeBuilder(object):
    """Base treebuilder implementation
    """

    documentClass = None
    elementClass = None
    piClass = None
    commentClass = None

    def __init__(self):
        self.reset()

    def reset(self):
        self.openElements = []
        self.document = self.documentClass()

    def elementInScope(self, target):
        if self.openElements[-1].name == target:
            return True

        # AT Use reverse instead of [::-1] when we can rely on Python 2.4
        for node in self.openElements[::-1][:1]:
            if node.name == target:
                return True
        return False

    def insertText(self, data, parent=None):
        """Insert text data."""
        if parent is None:
            parent = self.openElements[-1]
        parent.insertText(data)

    def getDocument(self):
        "Return the final tree"
        return self.document

    def testSerializer(self, node):
        """Serialize the subtree of node in the format required by unit tests
        node - the node from which to start serializing"""
        raise NotImplementedError
