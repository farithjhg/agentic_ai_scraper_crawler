# base_scraper.py
from dataclasses import dataclass
from typing import Dict, List, Optional, TypeVar, Generic, Type
from pydantic import BaseModel, Field
from dataclasses import dataclass
from enum import Enum
import json

class ContentType(str, Enum):
    ARTICLE = "article"
    PRODUCT = "product"
    LISTING = "listing"
    PROFILE = "profile"
    UNKNOWN = "unknown"

@dataclass
class WebContent:
    url: str
    title: str = "Untitled"
    description: Optional[str] = None
    content: Optional[str] = None
    metadata: Dict = Field(default_factory=dict)
    links: List[Dict] = Field(default_factory=list)
    images: List[Dict] = Field(default_factory=list)
    content_type: ContentType = ContentType.UNKNOWN
    structured_data: Optional[Dict] = None

class BaseScraper:
    def __init__(self, url: str, config: Optional[Dict] = None):
        self.url = url
        self.config = config or {}
        self.content = WebContent(url=url)
    
    async def detect_content_type(self) -> ContentType:
        """Detect the type of content on the page"""
        # Implement content type detection logic
        # This is a simplified example - you'd want to make this more sophisticated
        if "/product/" in self.url.lower():
            return ContentType.PRODUCT
        elif "/article/" in self.url.lower():
            return ContentType.ARTICLE
        return ContentType.UNKNOWN
    
    async def extract_metadata(self, html: str) -> Dict:
        """Extract common metadata from HTML"""
        # This would be implemented to extract OpenGraph, Twitter Cards, etc.
        return {}
    
    async def extract_main_content(self, html: str) -> str:
        """Extract the main content from the page"""
        # This would use libraries like trafilatura or readability-lxml
        return ""
    
    async def extract_links(self, html: str) -> List[Dict]:
        """Extract all links from the page"""
        return []
    
    async def extract_images(self, html: str) -> List[Dict]:
        """Extract all images from the page"""
        return []
    
    async def extract_structured_data(self, html: str) -> Optional[Dict]:
        """Extract structured data (JSON-LD, Microdata, RDFa)"""
        return None
    
    async def scrape(self) -> WebContent:
        """Main scraping method to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement this method")