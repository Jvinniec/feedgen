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
        pretty_print : `bool`
            Currently does nothing
        """
        with open(filename, 'w') as fl:
            json.dump(self.feed_json(entries), fl)
