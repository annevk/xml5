It is not really clear at this point to what extent this will all be 
finished. This is a research project to find out if it's possible to create
a superset of XML 1.0 / 1.1 and Namespaces in XML 1.0 / 1.1 that has non-fatal 
error handling. In other words, where every input stream of octets
will be turned into a (namespaced) DOM representing an XML document.

The specification is currently not up to date with the implementation. It
lacks the new entity handling and other parts of the internal subset. It
also doesn't deal with namespaces yet (element and attribute node creation
specifically).

The implementation and specification both currently lack attribute
normalization as defined by the XML 1.0/1.1 specification. There's also no
encoding sniffer defined or implemented yet that deals with
`<?xml encoding="utf-8"?>` and such.

An updated version of the specification appears to be maintained here:

https://github.com/Ygg01/xml5_draft
