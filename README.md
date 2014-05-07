TheHindu
========

Python script for aggregating news from The Hindu and sending it to a Kindle e-reader.

Program flow:
1. Downloads The Hindu's RSS XML.
2. Extracts titles and links from the XML.
3. Uses HTML tags to build a skeleton page compatible with Kindle.
4. Loops through the links to fetch relevant content and aggregate it in the skeleton page.
5. Opens the skeleton page as an octet stream and emails it to the Kindle using Gmail's SMTP service.


# Requires install of BeautifulSoup package for Python
# Uses standard Python libraries for rest of the functions
# Assumes that this script is run on a Windows environment
