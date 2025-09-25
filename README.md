# AI-Powered Web Scraper

A modern web scraping tool with built-in AI capabilities for intelligent data extraction. Extract structured data from any website with minimal configuration.

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## ✨ Features

- **AI-Powered Extraction**: Automatically extract structured data using LLMs
- **Multiple Content Types**: Built-in support for articles, products, listings, and profiles
- **Smart Scraping**: Automatic pagination and link following
- **Web Interface**: User-friendly Streamlit UI for easy interaction
- **API & CLI**: Full programmatic access through Python API and command line

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Chrome or Firefox browser
- API key for your preferred LLM provider (Gemini, Groq, etc.)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ai-web-scraper.git
   cd ai-web-scraper
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -e .
   ```

4. Set up your environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

### Web Interface

Launch the Streamlit web interface:
```bash
streamlit run streamlit_app.py
```

### Command Line Usage

Basic scraping:
```bash
python -m cli https://example.com
```

With AI-powered extraction:
```bash
python -m cli https://news-site.com --llm --content-type article
```

Save results to file:
```bash
python -m cli https://shop.com --llm --content-type product -o products.json
```

## 🛠 Configuration

### Environment Variables

Create a `.env` file with your configuration:
```env
# Required for AI features
GEMINI_API_KEY=your_gemini_api_key
MODEL=gemini/gemini-2.5-flash

# Optional
HEADLESS=true  # Run browser in headless mode
REQUEST_TIMEOUT=30  # Request timeout in seconds
```

## 📖 Advanced Usage

### Pagination Scraping

```bash
# Scrape multiple pages
python -m cli https://example.com --pagination --max-pages 5

# With LLM and CSS selector
python -m cli https://example.com --pagination --llm --css-selector ".product-item"
```

### Following Links

```bash
# Follow links on the page (up to 3 by default)
python -m cli https://example.com --follow-links

# Specify number of links to follow
python -m cli https://example.com --follow-links --max-links 5
```

## 🤖 API Usage

### Basic Scraping

```python
import asyncio
from crawler.scraper_factory import ScraperFactory

async def basic_example():
    scraper = ScraperFactory.create_scraper("https://example.com")
    
    async with scraper as s:
        content = await s.scrape()
        print(f"Title: {content.title}")
        print(f"Content length: {len(content.content)}")
```

### LLM-Powered Extraction

```python
from crawler.base_scraper import ContentType

async def llm_example():
    scraper = ScraperFactory.create_scraper("https://news-site.com")
    
    async with scraper as s:
        content = await s.scrape(
            use_llm=True, 
            content_type=ContentType.ARTICLE
        )
        
        if content.structured_data:
            for article in content.structured_data:
                print(f"Article: {article['title']}")
                print(f"Author: {article.get('author', 'Unknown')}")
```

## 🛠 Configuration

### Content Types

The scraper supports several built-in content types:

- **Article** (`ContentType.ARTICLE`): For news articles and blog posts
- **Product** (`ContentType.PRODUCT`): For e-commerce products
- **Listing** (`ContentType.LISTING`): For directory listings
- **Profile** (`ContentType.PROFILE`): For personal/company profiles
- **Generic** (`ContentType.UNKNOWN`): General purpose extraction

### Browser Configuration

```python
config = {
    "browser_config": {
        "headless": True,        # Run in headless mode
        "verbose": False,        # Disable verbose logging
        "browser_type": "chromium"  # Browser type (chromium, firefox, webkit)
    },
    "css_selector": ".content",  # Target specific content
    "session_id": "my_session"   # For caching sessions
}

scraper = ScraperFactory.create_scraper(url, config=config)
```

### LLM Configuration

Set up your LLM provider in the `.env` file:
```env
# Required for AI features
GEMINI_API_KEY=your_gemini_api_key
MODEL=gemini/gemini-2.5-flash

# Optional
HEADLESS=true
REQUEST_TIMEOUT=30
```

## 📚 Project Structure

```
.
├── crawler/              # Core scraping functionality
│   ├── __init__.py
│   ├── base_scraper.py   # Base scraper class
│   ├── async_web_crawler.py  # Async web crawler
│   └── llm_extraction.py # LLM integration
├── streamlit_app.py      # Web interface
├── cli.py               # Command-line interface
├── requirements.txt      # Project dependencies
└── README.md            # This file
```

## 🚀 Performance Tips

1. **Use headless mode** for production
2. **Limit pagination** with `--max-pages`
3. **Use CSS selectors** to target specific content
4. **Reuse sessions** with the same `session_id`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgements

- Built with [Crawl4AI](https://github.com/crawl4ai/crawl4ai)
- Powered by [LiteLLM](https://github.com/BerriAI/litellm)
- UI powered by [Streamlit](https://streamlit.io/)

---

<div align="center">
  Made with ❤️ for web scraping enthusiasts
</div>
