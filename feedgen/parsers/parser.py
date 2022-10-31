
import requests
from lxml.html import fromstring
from lxml.cssselect import CSSSelector
from typing import Any, List


class ParserResult():
    """
    A compressed representation of the parsed results
    """

    def __init__(self, title:str, link:str, descrip:str, extras:dict={}) -> None:
        """
        Parameters
        ----------
        title : `str`
            Title extracted from the result
        link : `str`
            Url associated with the result
        descrip : `str`
            Description of the parsed result
        extras : `dict` (default={})
            Dictionary of extra tags extracted
        """
        self.title   = title
        self.link    = link
        self.descrip = descrip
        self.extras  = extras
    

    def __str__(self) -> str:
        """
        Returns
        -------
        Pretty string representation for printing to the screen
        """
        # Assemble the string
        rep  = f'title: {self.title}\n'
        rep += f'link: {self.link}\n'
        rep += f'description: {self.descrip}'

        for name,tag in self.extras.items():
            rep += f'\n{name}: {tag}'

        return rep


class CSSInnerText(CSSSelector):
    """
    Class used to define a tag that we want to pull out the inner text from.
    """

    def __init__(self, css:str, default:Any=None) -> None:
        """
        Initialize CSSInnerText class

        Parameters
        ----------
        css : `str`
            CSS selection tag
        default : `str`
            Default value to be returned if no valid entry is found
        """
        super().__init__(css=css)
        self.default = default


    def get(self, div:str) -> str:
        """
        Returns the value as defined by the 'getValue' method

        Parameters
        ----------
        div : `str`
            'div' element extracted from webpage

        Returns
        -------
        Value defined by the `getValue()` method
        """
        try:
            return self.getValue(div)
        except IndexError as e:
            if self.default is None:
                raise e
            else:
                return self.default
        

    def getValue(self, div:str, indx:int=0) -> str:
        """
        Returns the value from the inner text of the element

        Parameters
        ----------
        div : `str`
            'div' element extracted from webpage
        indx : `int`
            Index of the element to extract the element from

        Returns
        -------
        Value from the inner text of the element
        """
        return self(div)[indx].text_content()


class CSSAttribute(CSSInnerText):
    """
    Class used for extracting a value from a tags attribute.
    """

    def __init__(self, css:str, attr:str, default:Any=None) -> None:
        """
        Initialize CSSAttribute class

        Parameters
        ----------
        css : `str`
            CSS selection tag
        attr : `str`
            Attribute from which to get the value from.
        default : `Any` (default=None)
            Default value to be returned if no valid entry is found
        """
        super().__init__(css=css, default=default)
        self.attribute = attr

    
    def getValue(self, div:str, indx:int=0) -> str:
        """
        Returns the value from the user defined attribute

        Parameters
        ----------
        div : `str`
            'div' element extracted from webpage
        indx : `int` (default=0)
            Index of the element to extract the element from

        Returns
        -------
        Value from a user defined attribute
        """
        return self(div)[indx].get(self.attribute)


class TagConfig():
    """
    Configuration for tag hierarchy
    """

    def __init__(self, container:CSSInnerText, title:CSSInnerText, 
                       link:CSSInnerText, descrip:CSSInnerText, extras:dict={}) -> None:
        """
        Parameters
        ----------
        container : `CSSInnerText`
            CSS selection for the object that contains a given tag
        title : `CSSInnerText`
            CSS selection for the title tag
        link : `CSSInnerText`
            CSS selection for the URL
        descrip : `CSSInnerText`
            CSS selection for the description
        extras : `dict` (default={})
            Extra CSS selectors with (key,CSS) pairs
        """

        # The top level container
        self.container = container

        # Tag configuration
        self.title   = title
        self.link    = link
        self.descrip = descrip

        # Additional tags
        self.extras = {}
        for name,css in extras.items():
            self.add_tag(name, css)


    def add_tag(self, name:str, css:str) -> None:
        """
        Add a given tag to the extra tags to be extracted

        Parameters
        ----------
        name : `str`
            String to be associated with the extracted tag
        css : `str`
            CSS selection text used to identify what part of the HTML to extract
            as the value of 'name'
        """
        self.extras[name] = css


class Parser():
    """
    Base class for all Parsers. For a default parser, use GoogleNews and set the
    'site' value to the url you want to query
    """

    def __init__(self, limit:int=100, **kwargs) -> None:
        """
        Initialize the parser class
        
        Parameters
        ----------
        limit : `int` (default=100)
            Maximum number of results to return
        kwargs:
            Extra parameters
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


    def get_params(self) -> dict:
        """
        Base method for assembling the parameters for passing to the site for
        querying.

        Returns
        -------
        Dictionary containing parameters to pass to the site 
        """
        return self.url['params']


    def parse_html(self) -> List[ParserResult]:
        """
        Assembles and submits a given query to a website and parses the returned
        HTML to extract the information requested by the user.

        Returns
        -------
        Parsed results from the specified URL
        """
        # Get the HTML text
        req = requests.get(self.url['base'], params=self.get_params())
        req = fromstring(req.text)

        # Resutl to be returned
        results = []

        # Parse the HTML
        for div in self.tag_config.container(req):
            # Get the required tags
            # title   = self.tag_config.title(div)[0].text_content()
            title   = self.tag_config.title.get(div)
            link    = self.tag_config.link.get(div)
            descrip = self.tag_config.descrip.get(div)

            # Parse the extra components
            extras = {
                'src_name': self.name,
                'src_url' : self.url['base']
            }
            for name,tag in self.tag_config.extras.items():
                extras[name] = tag.get(div)

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
            

    def process_link(self, link:str) -> str:
        """
        Test the link by seeing if it can be accessed in its raw form, or see
        if we need to append the link to the base URL

        Parameters
        ----------
        link : `str`
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

    def __init__(self, search_tag:str='q', **kwargs) -> None:
        """Initialize the search parser

        Parameters
        ----------
        search_tag : `str` (default='q')
            String that represents the tag that is used in the search url
        kwargs : 
            Additional parameters
        """
        super().__init__(**kwargs)

        self.search_text = ''
        self.search_tag  = search_tag


    def search_term(self, text:str) -> None:
        """
        Define the search term to be used
        
        Parameters
        ----------
        text : `str`
            Text to be searched for
        """
        self.search_text = text


    def get_params(self) -> dict:
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
