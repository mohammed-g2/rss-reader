# Rss reader

### Installation
- create virtual environment `python -m venv .venv` and activate it `.venv\Scripts\activate`
- install dependencies: `pip install -r requirements.txt`
- initialize the application: `flask init`
- run the application: `flask run`

### How to use
- find a website that offers rss file "xml format"
- go to add new feed page
- fill the form with the tag names from the xml file
- the rss feed will be available in home page
- the app will run a scraping job once every 24 hours for all rss feeds stored