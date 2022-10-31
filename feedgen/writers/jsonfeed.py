# File: feedgen/writers/jsonfeed.py
# Author: J. Cardenzana (c) 2022
# =============================================================================
# This file defines the implementation of the `JsonFeed` class. This file is
# responsible for writing the results of parsing a page to a JSON formatted 
# file. 
#
# Each RSS Feed is required to have the following parameters at the top level:
#    - version (string): JSON feed version (e.g. 'https://jsonfeed.org/version/1.1')
#    - title (string): A title for the feed
#    - home_page_url (string): A link that defines the feed's location (hosting url)
#    - description (string): Description of the RSS feed
#    - items (JSON list): Any number of item objects defining a link in the feed
# The channel includes a list of items that have the following parameters:
#    - id (string): Unless set by the parser author, defaults to the link
#    - title (string): Title of the feed entry
#    - url (string): Link to the article entry
#    - content_text (string): Short description of the article
#    - src_name (string): Name of base site (e.g. 'Yahoo News')
#    - src_url (string): Base URL for the source (e.g. 'https://news.search.yahoo.com/search?')
# =============================================================================

import json
import datetime
from typing import Any, List, Dict

from ..parsers.parser import ParserResult

class JsonFeed():
    """ Class for constructing a JSON feed from a list of ParseResult objects """

    def __init__(self, title:str, link:str, descrip:str) -> None:
        """
        Construct a JSON Feed object

        Parameters
        ----------
        title : `str`
            The name of the channel that you're creating
        link : `str`
            Link to HTML site hosting this feed
        descrip : `str`
            Description of this feed 
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
            Value to be set. Can be any value, as long as it's JSON serializable.
        """
        self.extra_tag[tag] = value


    def gen_item(self, entry:ParserResult) -> Dict[str,Any]:
        """
        Create a dictionary of values associated with a single parsed result

        Parameters
        ----------
        entry : `ParserResult`
            Parsed results from a webpage to be converted into
            a dictionary object of key:value pairs

        Returns
        -------
        Dictionary of objects extracted from `entry`
        """
        # define the required keys
        parent = {
            "id": entry.link,
            "title": entry.title,
            "url": entry.link,
            "content_text": entry.descrip,
        }

        # Add the extra tags as child elements
        for tag,value in entry.extras.items():
            # Format datetime objects
            if isinstance(value, datetime.datetime):
                value = value.isoformat()

            parent[tag] = value

        return parent


    def feed_json(self, entries:List[ParserResult]) -> Dict[str, Any]:
        """
        Generate a dictionary containing the parsed results in `entries`.

        Parameters
        ----------
        entries : `List[ParserResult]`
            List of parsed results
        
        Returns
        -------
        Dictionary of items ready to be written to a JSON file
        """
        # Construct the top element
        channel = {
            "version": "https://jsonfeed.org/version/1.1",
            "title": self.title,
            "home_page_url": self.link,
            "description": self.descrip,
            "items": []
        }

        # Add extra tags
        for tag, val in self.extra_tags.items():
            channel[tag] = val

        # add all the entries
        for entry in entries:
            channel["items"].append(self.gen_item(entry))

        return channel


    def write(self, entries:List[ParserResult], filename:str, pretty_print:bool=True) -> None:
        """
        Writes parsed site data to a given file.

        Parameters
        ----------
        entries : `List[ParserResult]`
            List of parsed results
        filename : `str`
            File name to write the entries to
        pretty_print : `bool` (default=True)
            Generates the file with newlines and 2 space indentation
        """
        indent = 2 if pretty_print else None
        with open(filename, 'w') as fl:
            json.dump(self.feed_json(entries), fl, indent=indent)
