# File: feedgen/validators/rss_validator.py
# Author: J. Cardenzana (c) 2022
# =============================================================================
# Defines the RssValidator class that is used (in conjunction with an RSS 
# schema file) to validate that an RSS feed is properly formatted.
# =============================================================================

from lxml import etree
import os

class RssValidator():
    """
    Validator class for RSS feeds
    """

    def __init__(self, schema_filename:str=os.path.join(os.path.dirname(__file__),'rss_schema.xml')) -> None:
        """
        Contructor for RssValidator class

        Parameters
        ----------
        schema_filename : `str`
            Filename containing schema definition for an RSS format. By default
            this is 'feedgen/validators/rss_schema.xml'
        """
        schema_doc = etree.parse(schema_filename)
        self.schema = etree.XMLSchema(schema_doc)


    def validate(self, rss_feed:str) -> bool:
        """
        Based on the validator that was supplied at construction time
        check if the supplied file is a validly formatted

        Parameters
        ----------
        rss_feed : str
            Filename of RSS feed stored as XML

        Returns
        -------
        True if rss_feed is considered valid, otherwise false, and some
        errors are printed.
        """
        # Open the file for validation
        xml_doc = etree.parse(rss_feed)
        return self.schema.assertValid(xml_doc) is None
