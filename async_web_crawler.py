# crawler/async_web_crawler.py
from typing import Dict, Optional, List
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode, BrowserConfig
from base_scraper import BaseScraper, WebContent, ContentType
from llm_extraction import (
    get_llm_strategy_for_content_type,
    get_generic_llm_strategy,
    process_llm_extracted_data,
    check_no_results_llm
)
import asyncio

class AsyncWebScraper(BaseScraper):
    def __init__(self, url: str, config: Optional[Dict] = None):
        super().__init__(url, config)
        self.crawler = None
        self.browser_config = None
    
    def _get_browser_config(self) -> BrowserConfig:
        """Get browser configuration matching the original implementation"""
        browser_config_dict = self.config.get("browser_config", {})
        return BrowserConfig(
            browser_type=browser_config_dict.get("browser_type", "chromium"),
            headless=browser_config_dict.get("headless", False),
            verbose=browser_config_dict.get("verbose", True)
        )
    
    async def scrape_with_pagination(self, 
                                   base_url: str = None,
                                   max_pages: int = 10,
                                   use_llm: bool = True,
                                   content_type: ContentType = None,
                                   follow_links: bool = False,
                                   max_links_per_page: int = 5) -> List[Dict]:
        """Scrape multiple pages with pagination support and optional deep link extraction"""
        if not base_url:
            base_url = self.url
        
        all_items = []
        page_number = 1
        
        while page_number <= max_pages:
            # Construct URL with page parameter
            if "?" in base_url:
                url = f"{base_url}&page={page_number}"
            else:
                url = f"{base_url}?page={page_number}"
            
            print(f"Scraping page {page_number}: {url}")
            
            # Update URL for this page
            original_url = self.url
            self.url = url
            
            try:
                # Scrape the page
                content = await self.scrape(use_llm=use_llm, content_type=content_type)
                
                # Check for no results
                if content.content and await check_no_results_llm(content.content):
                    print(f"No more results found on page {page_number}")
                    break
                
                # Add structured data if available
                if content.structured_data:
                    page_items = content.structured_data.copy()
                    
                    # Follow links if requested
                    if follow_links:
                        page_items = await self._extract_from_links(
                            page_items, max_links_per_page, use_llm, content_type
                        )
                    
                    all_items.extend(page_items)
                    print(f"Found {len(page_items)} items on page {page_number}")
                else:
                    print(f"No structured data found on page {page_number}")
                    # If no structured data and we're using LLM, might be end of results
                    if use_llm:
                        break
                
                page_number += 1
                
            except Exception as e:
                print(f"Error scraping page {page_number}: {e}")
                break
            finally:
                # Restore original URL
                self.url = original_url
        
        print(f"Total items extracted: {len(all_items)}")
        return all_items
    
    async def __aenter__(self):
        """Initialize the crawler when entering the context"""
        try:
            self.browser_config = self._get_browser_config()
            # Create the crawler but don't initialize it yet - let the context manager handle it
            self.crawler = AsyncWebCrawler(config=self.browser_config)
            # Enter the crawler's context manager
            await self.crawler.__aenter__()
            return self
        except Exception as e:
            print(f"Error initializing crawler: {str(e)}")
            raise

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Clean up resources when exiting the context"""
        if hasattr(self, 'crawler') and self.crawler:
            try:
                await self.crawler.__aexit__(exc_type, exc_val, exc_tb)
            except Exception as e:
                print(f"Error during crawler cleanup: {str(e)}")
    
    async def check_no_results(self, url: str = None) -> bool:
        """Check if a page indicates no results are available"""
        check_url = url or self.url
        
        try:
            result = await self.crawler.arun(
                url=check_url,
                config=CrawlerRunConfig(
                    cache_mode=CacheMode.BYPASS,
                    session_id=self.config.get("session_id", "default_session")
                )
            )
            
            if result.success:
                content = ""
                if hasattr(result, 'cleaned_html'):
                    content = result.cleaned_html
                elif hasattr(result, 'markdown'):
                    content = result.markdown
                
                return await check_no_results_llm(content)
            
        except Exception as e:
            print(f"Error checking for no results: {e}")
        
        return False
    
    async def _extract_from_links(self, 
                                items: List[Dict], 
                                max_links_per_page: int,
                                use_llm: bool,
                                content_type: ContentType) -> List[Dict]:
        """Extract additional data by following links in the items"""
        if not items or max_links_per_page <= 0:
            return items
            
        enhanced_items = []
        
        for item in items:
            enhanced_item = item.copy()
            enhanced_item['extracted_from_links'] = []
            
            # Extract links from the item or its structured_data
            links = []
            
            # Check if we have structured_data with links
            if 'structured_data' in item and isinstance(item['structured_data'], list) and len(item['structured_data']) > 0:
                # Get links from the first structured_data item if it exists
                first_item = item['structured_data'][0]
                if isinstance(first_item, dict) and 'links' in first_item and isinstance(first_item['links'], list):
                    links = first_item['links']
            # Fall back to top-level links if none found in structured_data
            if not links and 'links' in item and isinstance(item['links'], list):
                links = item['links']
            
            if not links:
                enhanced_items.append(enhanced_item)
                continue
            
            # Filter out None or empty links and ensure they're strings
            links = [str(link) for link in links if link and str(link).startswith(('http://', 'https://'))]
            
            # Filter out duplicate links while preserving order
            seen_links = set()
            unique_links = []
            for link in links:
                if link not in seen_links:
                    seen_links.add(link)
                    unique_links.append(link)
            
            # Limit the number of links to follow
            links_to_follow = unique_links[:max_links_per_page]
            
            for link in links_to_follow:
                try:
                    print(f"  Following link: {link}")
                    
                    # Create a temporary scraper for this link
                    original_url = self.url
                    self.url = link
                    
                    # Scrape the linked page
                    link_content = await self.scrape(use_llm=use_llm, content_type=content_type)
                    
                    # Add the extracted data
                    link_data = {
                        'url': link,
                        'title': link_content.title,
                        'description': link_content.description,
                        'content_length': len(link_content.content) if link_content.content else 0,
                        'structured_data': link_content.structured_data
                    }
                    
                    enhanced_item['extracted_from_links'].append(link_data)
                    
                    # Restore original URL
                    self.url = original_url
                    
                    # Add a small delay to be respectful
                    await asyncio.sleep(1)
                    
                except Exception as e:
                    print(f"    Error following link {link}: {e}")
                    # Restore original URL in case of error
                    self.url = original_url
                    continue
            
            enhanced_items.append(enhanced_item)
        
        return enhanced_items

    async def scrape(self, use_llm: bool = False, content_type: ContentType = None) -> WebContent:
        """Scrape the webpage using crawl4ai with optional LLM extraction"""
        if not self.crawler:
            return WebContent(
                url=self.url,
                title="Error: Crawler not initialized",
                description="Crawler must be used within an async context manager",
                content_type=ContentType.UNKNOWN
            )
        
        try:
            # Determine if we should use LLM extraction
            llm_strategy = None
            if use_llm:
                if content_type:
                    llm_strategy = get_llm_strategy_for_content_type(content_type)
                else:
                    llm_strategy = get_generic_llm_strategy()
            
            # Configure crawler run
            config_params = {
                "cache_mode": CacheMode.BYPASS,
                "session_id": self.config.get("session_id", "default_session")
            }
            
            # Add LLM strategy if available
            if llm_strategy:
                config_params["extraction_strategy"] = llm_strategy
            
            # Add CSS selector if provided
            css_selector = self.config.get("css_selector")
            if css_selector:
                config_params["css_selector"] = css_selector
            
            result = await self.crawler.arun(
                url=self.url,
                config=CrawlerRunConfig(**config_params)
            )
            
            if not result.success:
                raise Exception(f"Failed to scrape {self.url}: {result.error_message}")
            
            # Extract basic content
            content = ""
            if hasattr(result, 'cleaned_html'):
                content = result.cleaned_html
            elif hasattr(result, 'markdown'):
                content = result.markdown
            elif hasattr(result, 'html'):
                content = result.html
            
            # Process LLM extracted data if available
            structured_data = None
            if llm_strategy and hasattr(result, 'extracted_content') and result.extracted_content:
                extracted_items = process_llm_extracted_data(
                    result.extracted_content,
                    content_type or ContentType.UNKNOWN
                )
                if extracted_items:
                    structured_data = extracted_items
                    print(f"LLM extracted {len(extracted_items)} items")
            
            # Detect content type if not provided
            detected_content_type = content_type or await self.detect_content_type()
            
            return WebContent(
                url=self.url,
                title=result.metadata.get("title", "No title found"),
                description=result.metadata.get("description", ""),
                content=content,
                content_type=detected_content_type,
                structured_data=structured_data
            )
            
        except Exception as e:
            print(f"Error during scraping: {str(e)}")
            return WebContent(
                url=self.url,
                title=f"Error: {str(e)}",
                description="An error occurred during scraping",
                content_type=ContentType.UNKNOWN
            )