# crawler/examples.py
"""
Examples demonstrating the enhanced web scraper with LLM capabilities
"""
import asyncio
import json
from crawler.scraper_factory import ScraperFactory
from crawler.base_scraper import ContentType

async def example_basic_scraping():
    """Basic scraping without LLM"""
    print("=== Basic Scraping Example ===")
    
    scraper = ScraperFactory.create_scraper("https://example.com")
    
    async with scraper as s:
        content = await s.scrape()
        print(f"Title: {content.title}")
        print(f"Content length: {len(content.content) if content.content else 0}")
        print(f"Content type: {content.content_type.value}")

async def example_llm_scraping():
    """LLM-powered structured data extraction"""
    print("\n=== LLM Scraping Example ===")
    
    scraper = ScraperFactory.create_scraper("https://jubilusrooms.com/")
    
    async with scraper as s:
        # Try generic LLM extraction
        content = await s.scrape(use_llm=True)
        print(f"Title: {content.title}")
        print(f"LLM extracted items: {len(content.structured_data) if content.structured_data else 0}")
        
        if content.structured_data:
            print("First extracted item:", json.dumps(content.structured_data[0], indent=2))

async def example_pagination_scraping():
    """Pagination scraping with LLM"""
    print("\n=== Pagination Scraping Example ===")
    
    # Configure with CSS selector for venue listings
    config = {
        "css_selector": "[class^='info-container']"
    }
    
    scraper = ScraperFactory.create_scraper("https://jubilusrooms.com/", config=config)
    
    async with scraper as s:
        items = await s.scrape_with_pagination(
            max_pages=3,  # Limit for demo
            use_llm=True,
            content_type=ContentType.LISTING
        )
        
        print(f"Total items extracted: {len(items)}")
        if items:
            print("Sample item:", json.dumps(items[0], indent=2))

async def example_targeted_extraction():
    """Targeted extraction for specific content types"""
    print("\n=== Targeted Content Extraction ===")
    
    # Example URLs for different content types
    examples = [
        ("https://example.com", ContentType.UNKNOWN, "Generic content"),
        # Add more examples as needed
    ]
    
    for url, content_type, description in examples:
        print(f"\nExtracting {description} from {url}")
        
        scraper = ScraperFactory.create_scraper(url)
        async with scraper as s:
            content = await s.scrape(use_llm=True, content_type=content_type)
            print(f"  Title: {content.title}")
            print(f"  Structured items: {len(content.structured_data) if content.structured_data else 0}")

async def main():
    """Run all examples"""
    print("Web Scraper with LLM - Examples\n")
    
    # Check if GROQ_API_KEY is available
    import os
    if not os.getenv("GROQ_API_KEY"):
        print("⚠️  GROQ_API_KEY not found. LLM features will be limited.")
        print("   Set your API key: export GROQ_API_KEY='your-key-here'\n")
    
    try:
        await example_basic_scraping()
        await example_llm_scraping()
        # await example_pagination_scraping()  # Uncomment to test pagination
        await example_targeted_extraction()
        
    except Exception as e:
        print(f"Error in examples: {e}")

if __name__ == "__main__":
    asyncio.run(main())
