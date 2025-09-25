# Advanced Web Scraper - Usage Guide

## Quick Start

### 1. Installation

```bash
# Navigate to the crawler directory
cd crawler

# Install dependencies
python install.py

# Or manually install
pip install -r requirements.txt
```

### 2. Set up API Key (Optional, for LLM features)

```bash
# Get a free API key from https://console.groq.com/
export GROQ_API_KEY="your-groq-api-key-here"

# Or add to .env file
echo "GROQ_API_KEY=your-groq-api-key-here" > .env
```

### 3. Basic Usage

#### Command Line Interface

```bash
# Basic scraping
python -m crawler.cli https://example.com

# With LLM extraction
python -m crawler.cli https://example.com --llm

# Save to file
python -m crawler.cli https://example.com --llm -o results.json

# Pagination scraping
python -m crawler.cli https://example.com --pagination --max-pages 5

# Deep link extraction
python -m crawler.cli https://example.com --llm --follow-links --max-links 3
```

#### Streamlit Web Interface

```bash
# Launch the web interface
python -m streamlit run streamlit_app.py

# Or use the launcher
python ../run_streamlit.py
```

#### Python API

```python
import asyncio
from crawler import ScraperFactory, ContentType

async def example():
    scraper = ScraperFactory.create_scraper("https://example.com")
    
    async with scraper as s:
        # Basic scraping
        content = await s.scrape()
        
        # LLM-powered extraction
        content = await s.scrape(use_llm=True, content_type=ContentType.ARTICLE)
        
        # Pagination with deep links
        items = await s.scrape_with_pagination(
            max_pages=5,
            use_llm=True,
            follow_links=True,
            max_links_per_page=3
        )

asyncio.run(example())
```

## Features Overview

### 🕷️ Core Scraping
- **Universal compatibility**: Works with any website
- **Async/await**: High-performance concurrent operations
- **Browser automation**: Chromium-based rendering
- **Content extraction**: HTML, markdown, and cleaned text

### 🧠 LLM Integration
- **Smart extraction**: AI-powered structured data extraction
- **Content type detection**: Articles, products, listings, profiles
- **Custom models**: Support for custom Pydantic models
- **Validation**: Automatic data cleaning and validation

### 🔗 Advanced Features
- **Pagination support**: Automatic multi-page scraping
- **Deep link extraction**: Follow and extract from linked pages
- **CSS selectors**: Target specific page elements
- **Rate limiting**: Respectful crawling with delays

### 📊 Data Export
- **JSON output**: Structured data export
- **CSV support**: Tabular data format
- **Real-time streaming**: Live data processing
- **Analytics**: Built-in data analysis tools

## Command Line Options

```
usage: python -m crawler.cli [-h] [--output OUTPUT] [--llm] 
                             [--content-type {article,product,listing,profile,unknown}]
                             [--pagination] [--max-pages MAX_PAGES] 
                             [--css-selector CSS_SELECTOR]
                             [--follow-links] [--max-links MAX_LINKS]
                             url

positional arguments:
  url                   URL to scrape

options:
  -h, --help            show this help message and exit
  --output OUTPUT, -o OUTPUT
                        Output file (JSON)
  --llm                 Use LLM for structured data extraction
  --content-type {article,product,listing,profile,unknown}, -t {article,product,listing,profile,unknown}
                        Content type for targeted LLM extraction
  --pagination, -p      Enable pagination scraping
  --max-pages MAX_PAGES Maximum pages to scrape (default: 10)
  --css-selector CSS_SELECTOR
                        CSS selector to target specific content
  --follow-links        Follow links found in extracted data
  --max-links MAX_LINKS Maximum links to follow per page (default: 3)
```

## Examples

### E-commerce Scraping
```bash
# Extract product information
python -m crawler.cli https://shop.example.com/products --llm --content-type product --pagination --max-pages 5
```

### News Article Extraction
```bash
# Extract article content with deep links
python -m crawler.cli https://news.example.com --llm --content-type article --follow-links --max-links 2
```

### Directory Scraping
```bash
# Scrape business listings
python -m crawler.cli https://directory.example.com --llm --content-type listing --css-selector ".business-card"
```

### Custom Configuration
```python
# Advanced Python usage
import asyncio
from crawler import ScraperFactory, ContentType

async def custom_scraping():
    config = {
        "browser_config": {
            "headless": True,
            "verbose": False
        },
        "css_selector": ".main-content"
    }
    
    scraper = ScraperFactory.create_scraper("https://example.com", config=config)
    
    async with scraper as s:
        content = await s.scrape(
            use_llm=True,
            content_type=ContentType.ARTICLE
        )
        
        print(f"Title: {content.title}")
        print(f"Extracted items: {len(content.structured_data)}")

asyncio.run(custom_scraping())
```

## Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Reinstall dependencies
   pip install -r requirements.txt
   ```

2. **Browser Issues**
   ```bash
   # Install browser dependencies (Linux)
   sudo apt-get install chromium-browser
   
   # Or use headless mode
   python -m crawler.cli https://example.com --headless
   ```

3. **LLM Errors**
   ```bash
   # Check API key
   echo $GROQ_API_KEY
   
   # Test without LLM
   python -m crawler.cli https://example.com
   ```

4. **Memory Issues**
   ```bash
   # Reduce concurrent operations
   python -m crawler.cli https://example.com --max-pages 2 --max-links 1
   ```

### Performance Tips

1. **Use headless mode** for production
2. **Limit pagination** to avoid infinite loops
3. **Use CSS selectors** to target specific content
4. **Enable rate limiting** for respectful crawling
5. **Cache results** for repeated scraping

## API Reference

### Classes

- **`ScraperFactory`**: Factory for creating scraper instances
- **`AsyncWebScraper`**: Main scraper implementation
- **`WebContent`**: Data model for scraped content
- **`ContentType`**: Enum for content types

### Functions

- **`get_llm_strategy_for_content_type()`**: Get LLM strategy for content type
- **`get_generic_llm_strategy()`**: Get generic LLM strategy
- **`process_llm_extracted_data()`**: Process and validate LLM output

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

MIT License - see LICENSE file for details.
