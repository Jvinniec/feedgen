# Update the path so that we pull from the current version of the code
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__),'..'))

from feedgen.parsers import GoogleNews, BingNews, YahooNews
from feedgen.writers import JsonFeed

if __name__ == '__main__':
    # Define the parser
    parser = GoogleNews(limit=10)

    # Define the search term
    parser.search_term('cats')

    # Google supports a 'site' keyword that can be chained to search only
    # specific sites
    parser.add_site('npr.org')

    # Run the actual parser
    results = parser.parse_html()

    # Save the result to an RSS file
    jsn = JsonFeed(title='test',
                   link='https://www.github.com',
                   descrip='This is only a test')
    jsn.write(results, 'test.json', pretty_print=True)

    # Print the titles
    # for res in results:
    #     print(res.title)
    #     print(f'   link: {res.link}')
