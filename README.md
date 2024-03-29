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
There's also the ability to generate a JSON formatted feed:
```python
from feedgen.writers import JsonFeed

# Define the RSS feed
jsn_feed = JsonFeed(title='My Feed',
                    link='https://www.mysite.com',
                    descrip='NPR news articles that are relevant to cute cats')
# Write the results
jsn_feed.write(results, 'npr_cats.json')
```

You can also print the results to the screen:
```python
print(results)
```

## Validating RSS Feeds
There is also an RSS validator class that can be used to validate the RSS feeds generated by this library. This is particularly useful when you want to automate the process of generating RSS feeds and validate the written XML. To use the RSS validator class:

```Python
# Import the RSS validator
from feedgen.validators import RssValidator

# Create the RSS Validator
validator = RssValidator(schema_filename='path/to/shcema.xml')

# Validate on our previously generated NPR Cats news feed
if validator.validate(rss_feed='npr_cats.xml'):
    print('RSS is valid!')
else:
    print('RSS is not valid :(')
```
A sample RSS schema file that can be used directly with `feedgen` is available in [feedgen/validators/rss_schema.xml](feedgen/validators/rss_schema.xml).