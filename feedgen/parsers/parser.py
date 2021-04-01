
import requests
from lxml.html import fromstring
from lxml.cssselect import CSSSelector


class ParserResult():
    """
    A compressed representation of the parsed results
    """

    def __init__(self, title, link, descrip, extras={}):
        """
        """
        self.title   = title
        self.link    = link
        self.descrip = descrip
        self.extras  = extras
    

    def __str__(self):
        """
        Pretty string representation for printing
        """
        # Assemble the string
        rep  = f'title: {self.title}\n'
        rep += f'link: {self.link}\n'
        rep += f'description: {self.descrip}'

        for name,tag in self.extras.items():
            rep += f'{name}: {tag}'

        return rep


class TagConfig():
    """
    Configuration for tag hierarchy
    """

    def __init__(self, container, title, link, descrip, extras={}):

        # The top level container
        self.container = CSSSelector(container)

        # Tag configuration
        self.title   = CSSSelector(css=title)
        self.link    = CSSSelector(css=link)
        self.descrip = CSSSelector(css=descrip)

        # Additional tags
        self.extras = {}
        for name,css in extras.items():
            self.add_tag(name, css)


    def add_tag(self, name, css):
        """
        """
        self.extra_tags[tag] = CSSSelector(css=css)


class Parser():
    """
    Base class for all Parsers. For a default parser, use GoogleNews and set the
    'site' value to the url you want to query
    """

    def __init__(self, limit=100, **kwargs):
        """
        Initialize the parser class
        """
        self.name = 'default'
        self.type = 'default'
        self.url = {
            'base': None,
            'params': {}
        }

        # Limit the number of returned results
        self.limit = limit

        # Note that the inheriting class must instatiate a tag_config variable
        self.tag_config = None


    def get_params(self):
        """
        Base method for assembling the parameters for passing to the site for
        querying.
        """
        return self.url['params']


    def parse_html(self):
        """
        Assembles and submits a given query to a website and parses the returned
        HTML to extract the information requested by the user.

        Returns
        -------
        Parsed results from the specified URL
        """
        # Get the HTML text
        req = requests.get(self.url['base'], params=self.get_params())
        print(req.url)
        req = fromstring(req.text)

        # Resutl to be returned
        results = []

        # Parse the HTML
        for div in self.tag_config.container(req):
            # Get the required tags
            title   = self.tag_config.title(div)[0].text_content()
            link    = self.tag_config.link(div)[0].get('href')
            descrip = self.tag_config.descrip(div)[0].text_content()

            # Parse the extra components
            extras = {}
            for name,tag in self.tag_config.extras.items():
                extras[name] = tag(div)[0].text_content()

            # Assemble the parsed results
            res = ParserResult(
                title   = title,
                link    = self.process_link(link),
                descrip = descrip,
                extras  = extras)
            
            results.append(res)

            # Quit when we've reached our limit
            if len(results) >= self.limit:
                break

        return results
            

    def process_link(self, link):
        """
        Test the link by seeing if it can be accessed in its raw form, or see
        if we need to append the link to the base URL

        Parameters
        ----------
        link : string
            Link to be tested

        Return
        ------
        Formatted link
        """
        # Check if the url is properly formatted
        return link


class SearchParser(Parser):
    """
    Subclass of the Parser class that specifically adds a 'search_text' and 
    'search_tag' parameters that can be used to specify the text to search with
    and what tag to pass to the URL.
    """

    def __init__(self, search_tag='q', **kwargs):
        """Initialize the search parser
        """
        super().__init__(**kwargs)

        self.search_text = ''
        self.search_tag  = search_tag


    def search_term(self, text: str):
        """
        Define the search term to be used
        
        text: str
            Text to be searched for
        """
        self.search_text = text


    def get_params(self):
        """
        Assemble the parameters to be passed to the site query. This class
        also formats the search text for submission to the query.

        Returns
        -------
        Python dict() containing parameters to submit to query
        """
        # Add the search term to the query parameters
        self.url['params'][self.search_tag] = self.search_text

        return super().get_params()