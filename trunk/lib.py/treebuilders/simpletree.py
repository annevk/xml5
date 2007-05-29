import _base
from xml.sax.saxutils import escape

# DOM-core like implementation with extensions.
class Node(_base.Node):
    def __init__(self):
        self.childNodes = []

    def __iter__(self):
        for node in self.childNodes:
            yield node
            for item in node:
                yield item

    def __unicode__(self):
        return self.name

    def toxml(self):
        raise NotImplementedError

    def printTree(self, indent=0):
        tree = '\n|%s%s' % (' '* indent, unicode(self))
        for child in self.childNodes:
            tree += child.printTree(indent + 2)
        return tree

    def appendChild(self, node, index=None):
        if (isinstance(node, Text) and self.childNodes and
          isinstance(self.childNodes[-1], Text)):
            self.childNodes[-1].value += node.value
        else:
            self.childNodes.append(node)
        node.parent = self

    def insertText(self, data):
        self.appendChild(Text(data))

    def hasContent(self):
        """Return true if the node has children or text"""
        return bool(self.childNodes)

class Document(Node):
    def __init__(self):
        Node.__init__(self)

    def __unicode__(self):
        return "#document"

    def toxml(self, encoding="utf=8"):
        result = ""
        for child in self.childNodes:
            result += child.toxml()
        return result.encode(encoding)

    def hilite(self, encoding="utf-8"):
        result = "<pre>"
        for child in self.childNodes:
            result += child.hilite()
        return result.encode(encoding) + "</pre>"
    
    def printTree(self):
        tree = unicode(self)
        for child in self.childNodes:
            tree += child.printTree(2)
        return tree

class Text(Node):
    def __init__(self, value):
        Node.__init__(self)
        self.value = value

    def __unicode__(self):
        return "\"%s\"" % self.value

    def toxml(self):
        return escape(self.value)

    hilite = toxml

class Element(Node):
    def __init__(self, name):
        Node.__init__(self)
        self.name = name
        self.attributes = {}

    def __unicode__(self):
        return "<%s>" % self.name

    def toxml(self):
        result = '<' + self.name
        if self.attributes:
            for name,value in self.attributes.iteritems():
                result += ' %s="%s"' % (name, escape(value,{'"':'&quot;'}))
        if self.childNodes:
            result += '>'
            for child in self.childNodes:
                result += child.toxml()
            result += '</%s>' % self.name
        else:
            result += '/>'
        return result
    
    def hilite(self):
        result = '&lt;<code class="markup element-name">%s</code>' % self.name
        if self.attributes:
            for name, value in self.attributes.iteritems():
                result += ' <code class="markup attribute-name">%s</code>=<code class="markup attribute-value">"%s"</code>' % (name, escape(value, {'"':'&quot;'}))
        if self.childNodes:
            result += ">"
            for child in self.childNodes:
                result += child.hilite()
        else:
            return result + "/>"
        return result + '&lt;/<code class="markup element-name">%s</code>>' % self.name

    def printTree(self, indent):
        tree = '\n|%s%s' % (' '*indent, unicode(self))
        indent += 2
        if self.attributes:
            for name, value in self.attributes.iteritems():
                tree += '\n|%s%s="%s"' % (' ' * indent, name, value)
        for child in self.childNodes:
            tree += child.printTree(indent)
        return tree

class Pi(Node):
    def __init__(self, name, data):
        Node.__init__(self)
        self.name = name
        self.data = data
    
    def __unicode__(self):
        return "<?%s %s?>" % (self.name, self.data)

    def toxml(self):
        return "<?%s %s?>" % (self.name, self.data)

    def hilite(self):
        return '<code class="markup pi">&lt;?%s %s?></code>' % (escape(self.name), escape(self.data))

class Comment(Node):
    def __init__(self, data):
        Node.__init__(self)
        self.data = data

    def __unicode__(self):
        return "<!-- %s -->" % self.data
    
    def toxml(self):
        return "<!--%s-->" % self.data

    def hilite(self):
        return '<code class="markup comment">&lt;!--%s--></code>' % escape(self.data)

class TreeBuilder(_base.TreeBuilder):
    documentClass = Document
    elementClass = Element
    piClass = Pi
    commentClass = Comment

    def testSerializer(self, node):
        return node.printTree()
