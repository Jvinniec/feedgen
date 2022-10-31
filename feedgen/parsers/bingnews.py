
from .parser import SearchParser, TagConfig
from .parser import CSSInnerText, CSSAttribute

class BingNews(SearchParser):
    """
    Parser that pulls results from 'https://news.bing.com'
    """

    def __init__(self, **kwargs) -> None:
        """
        Initializes the Bing News parser

        Parameters
        ----------
        kwargs
            List of extra parameters to pass to the `SearchParser` parent class
        """
        super().__init__(search_tag='q', **kwargs)

        self.name = 'Bing News'
        self.type = 'bingnews'

        # Define the URL and query parameters
        self.url['base'] = 'https://news.bing.com/'
        self.url['params'] = {}

        # Tags to be parsed
        self.tag_config = TagConfig(
            container = CSSInnerText('div.news-card'),
            title     = CSSInnerText('a.title'),
            link      = CSSAttribute('a.title', 'href'),
            descrip   = CSSInnerText('div.snippet')
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
        Assemble query parameters

        Returns
        -------
        Python dict() object of the form <name,value>
        """
        # Assemble the sites
        if len(self.sites) > 0:
            self.search_text += ' site:' + ('OR site:'.join(self.sites))

        return super().get_params()
