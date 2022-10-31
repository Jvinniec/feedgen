
from lxml.etree import Element, ElementTree
from lxml import etree
import lxml
from typing import Any, List, Dict

from ..parsers.parser import ParserResult

class RssFeed():
    """ Class for constructing an RSS feed from a list of ParseResult objects """

    def __init__(self, title:str, link:str, descrip:str) -> None:
        """
        Construct an RSS object

        Parameters
        ----------
        title : `str`
            The name of the channel that you're creating
        link : `str`
            Link to HTML site hosting this RSS
        descrip : `str`
            Description of this RSS feed 
        """
        self.title   = title
        self.link    = link
        self.descrip = descrip

        self.extra_tags = {}


    def add_top_tag(self, tag:str, value:Any) -> None:
        """
        Set the value of a specific top-level tag.

        Parameters
        ----------
        tag : `str`
            Tag in `self.extra_tags` to be set
        value : `Any`
            Value to be set. Can be any value.
        """
        self.extra_tag[tag] = value


    def gen_item(self, entry:ParserResult) -> lxml.etree.Element:
        """
        Create an XML tree of values associated with a single parsed result

        Parameters
        ----------
        entry : `ParserResult`
            Parsed results from a webpage to be converted

        Returns
        -------
        XML tree containing results extracted from `entry`
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


    def feed_xml(self, entries:List[ParserResult]) -> lxml.etree.Element:
        """
        Returns a list of parsed website results as an XML formatted list

        Parameters
        ----------
        entries : `List[ParserResult]`
            List of parsed results to be converted to XML
        
        Returns
        -------
        XML formatted results from `entries`
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


    def feed_str(self, entries:List[ParserResult], pretty_print:bool=True) -> str:
        """
        Convert parsed results into a string suitable for outputing to a file

        Parameters
        ----------
        entries : `List[ParserResult]`
            List of entries parsed from the web
        pretty_print : `bool` (default=True)
            Creates formatted XML output

        Returns
        -------
        XML output formatted as a string
        """
        # Get the XML output
        xml_out = self.feed_xml(entries)

        # Generate feed string
        return etree.tostring(xml_out, 
                              doctype='<?xml version="1.0"?>',
                              pretty_print=pretty_print)


    def write(self, entries:List[ParserResult], filename:str, pretty_print:bool=True) -> None:
        """
        Writes parsed site data to a given file

        Parameters
        ----------
        entries : `List[ParserResult]`
            List of entries parsed from the web
        filename : `str`
            Name of the file to write results to
        pretty_print : `bool` (default=True)
            Creates formatted XML output
        """
        with open(filename, 'wb') as fl:
            fl.write( self.feed_str(entries=entries, 
                                    pretty_print=pretty_print) )
