
from .parser import SearchParser, TagConfig
from .parser import CSSInnerText, CSSAttribute
import datetime

class GoogleNews(SearchParser):
    """
    Parser that pulls news results from 'https://news.google.com'
    """

    def __init__(self, **kwargs) -> None:
        """
        Initializes the Google News parser

        Parameters
        ----------
        kwargs
            List of extra parameters to pass to the `SearchParser` parent class
        """
        super().__init__(search_tag='q', **kwargs)

        self.name = 'Google News'
        self.type = 'googlenews'

        # Define the URL and query parameters
        self.url['base'] = 'https://news.google.com/'
        self.url['params'] = {}

        # Tags to be parsed
        self.tag_config = TagConfig(
            container = CSSInnerText('div.NiLAwe'),
            title     = CSSInnerText('h3.ipQwMb'),
            link      = CSSAttribute('a.VDXfz', attr='href'),
            descrip   = CSSInnerText('h3.ipQwMb'),
            extras = {
                'pubDate': CSSAttribute('time.WW6dff', attr='datetime',
                                        default=datetime.datetime.now().isoformat())
            }
        ) 
        
        # Sites to have Google News
        self.sites = []


    def add_site(self, site:str) -> None:
        """
        Append a site to the list of sites to restrict querying to

        Parameters
        ----------
        site : `str`
            Site to be queried (examples: 'wsj.com', 'npr.org')
        """
        self.sites.append(site)


    def get_params(self) -> dict:
        """
        Return a dictionary of parameters to pass to the query

        Returns
        -------
        Python dict() object of the form <name,value>
        """
        # Assemble the sites
        if len(self.sites) > 0:
            self.search_text += ' site:' + ('OR site:'.join(self.sites))

        return super().get_params()


    def process_link(self, link:str) -> str:
        """
        Google links are given as './article/...'. In order for them to function
        properly, we need to format them to strip the initial './' and append
        the result to 'https://news.google.com/'

        Parameters
        ----------
        link : `str`
            Link to be processed

        Return
        ------
        Formatted link
        """
        return self.url['base'] + link[2:]
