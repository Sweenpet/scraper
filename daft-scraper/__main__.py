from daft_repo import DaftRepo
from loader import PropertyUrlLoader
from scrapers import DaftPropertyScraper

def main(args=None):
    path = "/home/peter/Projects/DaftScraper/PropertyUrls/"
    repo = DaftRepo()
    scraper = DaftPropertyScraper(repo)
    scraper.action()

if __name__ == "__main__":
    main()