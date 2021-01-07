
from lxml.etree import Element, ElementTree
from lxml import etree

from ..parsers.parser import ParserResult

class Rss():

    def __init__(self, title, link, descrip):
        """
        Construct an RSS object

        Parameters
        ----------
        title: str
            The name of the channel that you're creating
        link: str
            Link to HTML site hosting this RSS
        descrip: str
            Description of this RSS feed 
        """
        self.title   = title
        self.link    = link
        self.descrip = descrip

        self.extra_tags = {}


    def add_top_tag(self, tag, value):
        """
        """
        self.extra_tag[tag] = value

    def gen_item(self, entry):
        """
        """
        parent = Element('item')

        # define the required keys
        item_title = Element('title')
        item_title.text = entry.title
        item_link = Element('link')
        item_link.text = entry.link
        item_guid = Element('guid')
        item_guid.text = entry.link
        item_descrip = Element('description')
        item_descrip.text = entry.descrip

        # Assemble child attributes
        children = [item_title, item_link, item_descrip, item_guid]

        # Add the extra tags as child elements
        for tag,value in entry.extras.items():
            item_tag = Element(tag)
            item_tag.text = value
            children.append( item_tag )

        # Add The extra
        for child in children:
            parent.append(child)

        return parent


    def feed_xml(self, entries):
        """
        """
        # Construct the top element
        channel = Element('channel')
        
        # Add the children
        # define the required keys
        channel_title = Element('title')
        channel_title.text = self.title
        channel_link = Element('link')
        channel_link.text = self.link
        channel_descrip = Element('description')
        channel_descrip.text = self.descrip

        channel.append( channel_title )
        channel.append( channel_link )
        channel.append( channel_descrip )

        # Add extra tags
        for tag, val in self.extra_tags.items():
            channel_tag = Element(tag)
            channel_tag.text = val
            channel.append( channel_tag )

        # add all the entries
        for entry in entries:
            channel.append(self.gen_item(entry))

        # Surround everything in an rss tag
        root = Element('rss', version='2.0')
        root.append(channel)

        return root


    def feed_str(self, entries, pretty_print=True):
        """
        """
        # Get the XML output
        xml_out = self.feed_xml(entries)

        # Generate feed string
        return etree.tostring(xml_out, 
                              doctype='<?xml version="1.0"?>',
                              pretty_print=pretty_print)


    def write(self, entries, filename, pretty_print=True):
        """
        Writes parsed site data to a given file
        """
        with open(filename, 'wb') as fl:
            fl.write( self.feed_str(entries=entries, 
                                    pretty_print=pretty_print) )
