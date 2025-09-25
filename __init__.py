# crawler/__init__.py
"""
Advanced Web Scraper with LLM Support

A powerful, generalized web scraper built on top of Crawl4AI with intelligent 
LLM-powered data extraction capabilities.
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .base_scraper import BaseScraper, WebContent, ContentType
from .async_web_crawler import AsyncWebScraper
from .scraper_factory import ScraperFactory
from .llm_extraction import (
    get_llm_strategy_for_content_type,
    get_generic_llm_strategy,
    process_llm_extracted_data
)

__all__ = [
    "BaseScraper",
    "WebContent", 
    "ContentType",
    "AsyncWebScraper",
    "ScraperFactory",
    "get_llm_strategy_for_content_type",
    "get_generic_llm_strategy",
    "process_llm_extracted_data",
]