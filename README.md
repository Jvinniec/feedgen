# RSS Gen: an RSS Generator

## Example: Google News
To use this RSS generator to pull information from Google News you would do
something like the following:
```python
# Load the Google News parser and RSS feed generator
from feedgen.parsers import GoogleNews

# Parse Google News results
parser = GoogleNews()            # Create the parser object
parser.search_term('cute cats')  # Define  search text
parser.add_site('npr.org')       # Only get results from npr.org
results = parser.parse_html()    # Run the actual query
```

Once you have the parsed results from the site, you can write out into an RSS-like feed:
```python
from feedgen.writers import RssFeed

# Define the RSS feed
rss_feed = RssFeed(title='My Feed',
               link='https://www.mysite.com',
               descrip='NPR news articles that are relevant to cute cats')
# Write the results
rss_feed.write(results, 'npr_cats.xml')
```

You can also print the results to the screen:
```python
print(results)
```