
from .parser import SearchParser, TagConfig

class BingNews(SearchParser):
    """
    Parser that pulls results from 'https://news.bing.com'
    """

    def __init__(self, **kwargs):
        """
        Initializes the Bing News parser
        """
        super().__init__(search_tag='q', **kwargs)

        self.name = 'Bing News'
        self.type = 'bingnews'

        # Define the URL and query parameters
        self.url['base'] = 'https://news.bing.com/'
        self.url['params'] = {}

        # Tags to be parsed
        self.tag_config = TagConfig(
            container = 'div.news-card',
            title     = 'a.title',
            link      = 'a.title',
            descrip   = 'div.snippet'
        )
        
        # Sites to have Google News
        self.sites = []


    def add_site(self, site):
        """
        Append a site to the list of sites to restrict querying to

        Parameters
        ----------
        site: str
            Site to be queried (examples: 'wsj.com', 'npr.org')
        """
        self.sites.append(site)


    def get_params(self):
        """
        Assemble query parameters

        Returns
        -------
        Python dict() object of the form <name,value>
        """
        # Setup the search term
        search_term = self.search_text

        # Assemble the sites
        if len(self.sites) > 0:
            search_term += ' site:' + ('OR site:'.join(self.sites))

        return super().get_params()
