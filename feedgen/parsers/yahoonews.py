
from .parser import SearchParser, TagConfig

class YahooNews(SearchParser):
    """
    Yahoo News parser
    """

    def __init__(self, **kwargs):
        """
        """
        super().__init__(search_tag='p', **kwargs)

        self.name = 'Yahoo News'
        self.type = 'yahoonews'

        # Define the URL and query parameters
        self.url['base'] = 'https://news.search.yahoo.com/search?'
        self.url['params'] = {}

        # Tags to be parsed
        self.tag_config = TagConfig(
            container = 'div.NewsArticle',
            title     = 'h4.s-title',
            link      = 'h4.s-title a',
            descrip   = 'p.s-desc'
        )
