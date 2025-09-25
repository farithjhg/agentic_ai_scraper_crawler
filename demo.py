# crawler/demo.py
"""
Demo script showcasing the enhanced web scraper capabilities
"""
import asyncio
import json
from datetime import datetime
from crawler.scraper_factory import ScraperFactory
from crawler.base_scraper import ContentType

async def demo_basic_scraping():
    """Demo: Basic web scraping"""
    print("🕷️ Demo 1: Basic Web Scraping")
    print("=" * 50)
    
    scraper = ScraperFactory.create_scraper("https://example.com")
    
    async with scraper as s:
        content = await s.scrape()
        
        print(f"✅ URL: {content.url}")
        print(f"📄 Title: {content.title}")
        print(f"📝 Content Length: {len(content.content) if content.content else 0}")
        print(f"🏷️ Content Type: {content.content_type.value}")
    
    print("\n")

async def demo_llm_extraction():
    """Demo: LLM-powered structured data extraction"""
    print("🧠 Demo 2: LLM-Powered Extraction")
    print("=" * 50)
    
    scraper = ScraperFactory.create_scraper("https://jubilusrooms.com/")
    
    async with scraper as s:
        content = await s.scrape(use_llm=True, content_type=ContentType.LISTING)
        
        print(f"✅ URL: {content.url}")
        print(f"📄 Title: {content.title}")
        print(f"🤖 LLM Extraction: {'✅ Success' if content.structured_data else '❌ Failed'}")
        
        if content.structured_data:
            item = content.structured_data[0]
            print(f"🏢 Extracted Title: {item.get('title', 'N/A')}")
            print(f"📍 Address: {item.get('metadata', {}).get('address', 'N/A')}")
            print(f"📞 Phone: {item.get('metadata', {}).get('phone', 'N/A')}")
            print(f"🔗 Links Found: {len(item.get('links', []))}")
            print(f"🖼️ Images Found: {len(item.get('images', []))}")
    
    print("\n")

async def demo_deep_link_extraction():
    """Demo: Deep link extraction"""
    print("🔗 Demo 3: Deep Link Extraction")
    print("=" * 50)
    
    scraper = ScraperFactory.create_scraper("https://jubilusrooms.com/")
    
    async with scraper as s:
        # First get the main page data
        content = await s.scrape(use_llm=True, content_type=ContentType.LISTING)
        
        if content.structured_data and content.structured_data[0].get('links'):
            print("🔍 Found links, now extracting from first 2 links...")
            
            # Extract from links manually for demo
            links = content.structured_data[0]['links'][:2]
            extracted_data = []
            
            for i, link in enumerate(links):
                try:
                    print(f"  📥 Extracting from: {link}")
                    
                    # Create new scraper for the link
                    link_scraper = ScraperFactory.create_scraper(link)
                    async with link_scraper as ls:
                        link_content = await ls.scrape(use_llm=True)
                        
                        extracted_data.append({
                            'url': link,
                            'title': link_content.title,
                            'content_length': len(link_content.content) if link_content.content else 0,
                            'structured_items': len(link_content.structured_data) if link_content.structured_data else 0
                        })
                        
                        print(f"    ✅ Title: {link_content.title}")
                        print(f"    📄 Content: {len(link_content.content) if link_content.content else 0} chars")
                    
                    # Be respectful with delays
                    await asyncio.sleep(1)
                    
                except Exception as e:
                    print(f"    ❌ Error: {str(e)}")
            
            print(f"\n📊 Summary: Extracted data from {len(extracted_data)} links")
        else:
            print("❌ No links found for deep extraction")
    
    print("\n")

async def demo_pagination_scraping():
    """Demo: Pagination scraping (limited for demo)"""
    print("📄 Demo 4: Pagination Scraping")
    print("=" * 50)
    
    scraper = ScraperFactory.create_scraper("https://jubilusrooms.com/")
    
    async with scraper as s:
        print("🔄 Testing pagination (max 2 pages for demo)...")
        
        items = await s.scrape_with_pagination(
            max_pages=2,
            use_llm=True,
            content_type=ContentType.LISTING,
            follow_links=False  # Disable for demo speed
        )
        
        print(f"📊 Total items extracted: {len(items)}")
        
        if items:
            print("📋 Sample items:")
            for i, item in enumerate(items[:3]):  # Show first 3
                print(f"  {i+1}. {item.get('title', 'Untitled')[:50]}...")
    
    print("\n")

async def main():
    """Run all demos"""
    print("🚀 Advanced Web Scraper - Demo Suite")
    print("=" * 60)
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check API key
    import os
    if os.getenv("GROQ_API_KEY"):
        print("✅ GROQ API Key found - LLM features enabled")
    else:
        print("⚠️ GROQ API Key not found - LLM features limited")
        print("   Set your key: export GROQ_API_KEY='your-key-here'")
    
    print("\n")
    
    try:
        # Run demos
        await demo_basic_scraping()
        await demo_llm_extraction()
        await demo_deep_link_extraction()
        await demo_pagination_scraping()
        
        print("🎉 All demos completed successfully!")
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
    
    print(f"⏰ Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    asyncio.run(main())
