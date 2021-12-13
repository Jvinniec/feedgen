
from lxml import etree

class RssValidator():
    """
    Validator class for RSS feeds
    """

    def __init__(self, 
                 schema_filename : str):
        """
        """
        schema_doc = etree.parse(schema_filename)
        self.schema = etree.XMLSchema(schema_doc)

    def validate(self, 
                 rss_feed : str) -> bool:
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
