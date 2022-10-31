# File: feedgen/parsers/__init__.py
# Author: J. Cardenzana (c) 2022
# =============================================================================
# This file defines the imports and sets up the `feedgen.parsers` submodule.
# =============================================================================

from .parser     import Parser, ParserResult, SearchParser, TagConfig
from .parser     import CSSInnerText, CSSAttribute
from .googlenews import GoogleNews
from .bingnews   import BingNews
from .yahoonews  import YahooNews
