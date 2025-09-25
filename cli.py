# crawler/cli.py
import asyncio
import json
import argparse
from scraper_factory import ScraperFactory
from base_scraper import ContentType

async def main():
    parser = argparse.ArgumentParser(description="Web Scraper CLI with LLM Support")
    parser.add_argument("url", help="URL to scrape")
    parser.add_argument("--output", "-o", help="Output file (JSON)")
    parser.add_argument("--llm", action="store_true", help="Use LLM for structured data extraction")
    parser.add_argument("--content-type", "-t", 
                       choices=["article", "product", "listing", "profile", "unknown"],
                       help="Content type for targeted LLM extraction")
    parser.add_argument("--pagination", "-p", action="store_true", 
                       help="Enable pagination scraping")
    parser.add_argument("--max-pages", type=int, default=10,
                       help="Maximum pages to scrape (default: 10)")
    parser.add_argument("--css-selector", help="CSS selector to target specific content")
    parser.add_argument("--follow-links", action="store_true", 
                       help="Follow links found in extracted data for deeper extraction")
    parser.add_argument("--max-links", type=int, default=3,
                       help="Maximum links to follow per page (default: 3)")
    args = parser.parse_args()
    
    try:
        # Parse content type
        content_type = None
        if args.content_type:
            content_type = ContentType(args.content_type)
        
        # Create scraper with configuration
        config = {}
        if args.css_selector:
            config["css_selector"] = args.css_selector
        
        scraper = ScraperFactory.create_scraper(args.url, config=config)
        
        # Use the context manager to ensure proper cleanup
        async with scraper as s:
            if args.pagination:
                # Scrape with pagination
                print(f"Starting pagination scraping (max {args.max_pages} pages)...")
                items = await s.scrape_with_pagination(
                    max_pages=args.max_pages,
                    use_llm=args.llm,
                    content_type=content_type,
                    follow_links=args.follow_links,
                    max_links_per_page=args.max_links
                )
                
                result = {
                    "url": args.url,
                    "scraping_mode": "pagination",
                    "total_items": len(items),
                    "items": items,
                    "llm_used": args.llm,
                    "content_type": content_type.value if content_type else "unknown"
                }
            else:
                # Single page scraping
                content = await s.scrape(use_llm=args.llm, content_type=content_type)
                
                result = {
                    "url": content.url,
                    "title": content.title,
                    "description": content.description,
                    "content_type": content.content_type.value,
                    "content_length": len(content.content) if content.content else 0,
                    "content_preview": content.content[:500] + "..." if content.content and len(content.content) > 500 else content.content,
                    "llm_used": args.llm,
                    "structured_data_count": len(content.structured_data) if content.structured_data else 0
                }
                
                # Add structured data if available
                if content.structured_data:
                    result["structured_data"] = content.structured_data
            
            if args.output:
                with open(args.output, "w", encoding="utf-8") as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                print(f"Results saved to {args.output}")
            else:
                print(json.dumps(result, indent=2))
                
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    asyncio.run(main())