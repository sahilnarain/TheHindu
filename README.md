TheHindu
========

Python script for aggregating news from The Hindu and sending it to a Kindle e-reader.

Program flow:
- Downloads The Hindu's RSS XML.
- Extracts titles and links from the XML.
- Uses HTML tags to build a skeleton page compatible with Kindle.
- Loops through the links to fetch relevant content and aggregate it in the skeleton page.
- Opens the skeleton page as an octet stream and emails it to the Kindle using Gmail's SMTP service.


Dependencies:
- Requires install of BeautifulSoup package for Python
- Uses standard Python libraries for rest of the functions
- Assumes that this script is run on a Windows environment
