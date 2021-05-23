import json
import datetime

from ..parsers.parser import ParserResult

class JsonFeed():

    def __init__(self, title, link, descrip):
        """
        Construct an JSON Feed object

        Parameters
        ----------
        title: str
            The name of the channel that you're creating
        link: str
            Link to HTML site hosting this feed
        descrip: str
            Description of this feed 
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


    def feed_json(self, entries):
        """
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


    def write(self, entries, filename, pretty_print=True):
        """
        Writes parsed site data to a given file
        """
        with open(filename, 'w') as fl:
            json.dump(self.feed_json(entries), fl)
