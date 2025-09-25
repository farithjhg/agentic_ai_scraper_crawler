# scraper_factory.py
from typing import Optional, Type
from base_scraper import BaseScraper
from async_web_crawler import AsyncWebScraper

class ScraperFactory:
    @staticmethod
    def create_scraper(
        url: str,
        scraper_type: str = "default",
        config: Optional[dict] = None
    ) -> BaseScraper:
        """Factory method to create a scraper instance
        
        Args:
            url: The URL to scrape
            scraper_type: Type of scraper to create ('default', 'crawl4ai', etc.)
            config: Configuration dictionary for the scraper
            
        Returns:
            An instance of a BaseScraper implementation
        """
        config = config or {}
        
        if scraper_type == "crawl4ai":
            return AsyncWebScraper(url, config)
        
        # Default to the async web crawler
        return AsyncWebScraper(url, config)