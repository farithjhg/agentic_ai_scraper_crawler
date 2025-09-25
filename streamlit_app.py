# crawler/streamlit_app.py
import streamlit as st
import asyncio
import json
import os
from datetime import datetime
import pandas as pd
from scraper_factory import ScraperFactory
from base_scraper import ContentType
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="🕷️ Advanced Web Scraper",
    page_icon="🕷️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .feature-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }
    
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .error-box {
        background: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🕷️ Advanced Web Scraper with LLM</h1>', unsafe_allow_html=True)
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Basic settings
        st.subheader("🌐 Basic Settings")
        url = st.text_input("🔗 URL to scrape", placeholder="https://example.com")
        
        # LLM settings
        st.subheader("🧠 LLM Settings")
        use_llm = st.checkbox("🤖 Use LLM for extraction", value=False)
        
        content_type = st.selectbox(
            "📋 Content Type",
            options=["unknown", "article", "product", "listing", "profile"],
            index=0,
            help="Select the type of content for targeted extraction"
        )
        
        # Advanced settings
        st.subheader("🔧 Advanced Settings")
        
        # Pagination
        use_pagination = st.checkbox("📄 Enable pagination", value=False)
        max_pages = st.slider("📊 Max pages", min_value=1, max_value=20, value=5)
        
        # Deep link extraction
        follow_links = st.checkbox("🔗 Follow links for deeper extraction", value=False)
        max_links = st.slider("🔢 Max links per page", min_value=1, max_value=10, value=3)
        
        # CSS Selector
        css_selector = st.text_input("🎯 CSS Selector (optional)", placeholder=".content, #main")
        
        # Browser settings
        st.subheader("🌐 Browser Settings")
        headless = st.checkbox("👻 Headless mode", value=True)
        
        # API Key check
        st.subheader("🔑 API Configuration")
        gemini_key = os.getenv("GEMINI_API_KEY")
        if gemini_key:
            st.success("✅ GEMINI API Key found")
        else:
            st.warning("⚠️ GEMINI API Key not found. LLM features will be limited.")
            st.info("Set your API key: `export GEMINI_API_KEY='your-key'`")
        model = os.getenv("MODEL")
        if model:
            st.success("✅ Model found")
        else:
            st.warning("⚠️ Model not found. LLM features will be limited.")
            st.info("Set your Model: `export MODEL='your-model'`")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🚀 Scraping Controls")
        
        # Action buttons
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        
        with col_btn1:
            scrape_button = st.button("🕷️ Start Scraping", type="primary", use_container_width=True)
        
        with col_btn2:
            if st.button("🧹 Clear Results", use_container_width=True):
                if 'scraping_results' in st.session_state:
                    del st.session_state.scraping_results
                st.rerun()
        
        with col_btn3:
            if st.button("💾 Download Results", use_container_width=True):
                if 'scraping_results' in st.session_state:
                    st.download_button(
                        label="📥 Download JSON",
                        data=json.dumps(st.session_state.scraping_results, indent=2),
                        file_name=f"scraping_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
    
    with col2:
        st.subheader("📊 Quick Stats")
        if 'scraping_results' in st.session_state:
            results = st.session_state.scraping_results
            
            if results.get('scraping_mode') == 'pagination':
                st.metric("📄 Total Items", results.get('total_items', 0))
                st.metric("🧠 LLM Used", "Yes" if results.get('llm_used') else "No")
                st.metric("🔗 Links Followed", "Yes" if follow_links else "No")
            else:
                st.metric("📝 Title Length", len(results.get('title', '')))
                st.metric("📄 Content Length", results.get('content_length', 0))
                st.metric("🔍 Structured Items", results.get('structured_data_count', 0))
    
    # Scraping execution
    if scrape_button and url:
        if not url.startswith(('http://', 'https://')):
            st.error("❌ Please enter a valid URL starting with http:// or https://")
            return
        
        with st.spinner("Scraping in progress..."):
            # Show progress
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Run scraping
                status_text.text("🚀 Initializing scraper...")
                progress_bar.progress(20)
                
                results = asyncio.run(run_scraping(
                    url=url,
                    use_llm=use_llm,
                    content_type=ContentType(content_type),
                    use_pagination=use_pagination,
                    max_pages=max_pages,
                    follow_links=follow_links,
                    max_links=max_links,
                    css_selector=css_selector if css_selector else None,
                    headless=headless,
                    progress_callback=lambda p, msg: (progress_bar.progress(p), status_text.text(msg))
                ))
            
                progress_bar.progress(100)
                status_text.text("✅ Scraping completed!")
                
                # Store results in session state
                st.session_state.scraping_results = results
                
                # Show success message
                st.markdown('<div class="success-box">🎉 Scraping completed successfully!</div>', unsafe_allow_html=True)
            
            except Exception as e:
                st.markdown(f'<div class="error-box">❌ Error: {str(e)}</div>', unsafe_allow_html=True)
                progress_bar.empty()
                status_text.empty()
    
    # Display results
    if 'scraping_results' in st.session_state:
        display_results(st.session_state.scraping_results)

async def run_scraping(url, use_llm, content_type, use_pagination, max_pages, 
                      follow_links, max_links, css_selector, headless, progress_callback):
    """Run the scraping operation"""
    
    # Configure scraper
    config = {
        "browser_config": {
            "headless": headless,
            "verbose": False
        }
    }
    
    if css_selector:
        config["css_selector"] = css_selector
    
    progress_callback(40, "🔧 Creating scraper...")
    scraper = ScraperFactory.create_scraper(url, config=config)
    
    progress_callback(60, "🕷️ Starting extraction...")
    
    async with scraper as s:
        if use_pagination:
            items = await s.scrape_with_pagination(
                max_pages=max_pages,
                use_llm=use_llm,
                content_type=content_type,
                follow_links=follow_links,
                max_links_per_page=max_links
            )
            
            return {
                "url": url,
                "scraping_mode": "pagination",
                "total_items": len(items),
                "items": items,
                "llm_used": use_llm,
                "content_type": content_type.value,
                "follow_links": follow_links,
                "timestamp": datetime.now().isoformat()
            }
        else:
            content = await s.scrape(use_llm=use_llm, content_type=content_type)
            
            return {
                "url": content.url,
                "title": content.title,
                "description": content.description,
                "content_type": content.content_type.value,
                "content_length": len(content.content) if content.content else 0,
                "llm_used": use_llm,
                "structured_data_count": len(content.structured_data) if content.structured_data else 0,
                "structured_data": content.structured_data,
                "timestamp": datetime.now().isoformat()
            }

def display_results(results):
    """Display scraping results in a nice format"""
    
    st.header("📊 Scraping Results")
    
    # Create tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Overview", "📄 Raw Data", "📊 Analytics", "🔍 Deep Links"])
    
    with tab1:
        st.subheader("📋 Overview")
        
        # Basic info
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("🌐 URL", "", results.get('url', 'N/A'))
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("📅 Timestamp", "", results.get('timestamp', 'N/A')[:19])
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("🤖 LLM Used", "", "Yes" if results.get('llm_used') else "No")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Mode-specific display
        if results.get('scraping_mode') == 'pagination':
            st.subheader("📄 Pagination Results")
            
            items = results.get('items', [])
            if items:
                # Create a summary table
                summary_data = []
                for i, item in enumerate(items):
                    summary_data.append({
                        "Item #": i + 1,
                        "Title": item.get('title', 'N/A')[:50] + "..." if len(item.get('title', '')) > 50 else item.get('title', 'N/A'),
                        "Links": len(item.get('links', [])),
                        "Images": len(item.get('images', [])),
                        "Deep Links": len(item.get('extracted_from_links', []))
                    })
                
                df = pd.DataFrame(summary_data)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No items extracted")
        
        else:
            st.subheader("📄 Single Page Results")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Title:**", results.get('title', 'N/A'))
                st.write("**Content Type:**", results.get('content_type', 'N/A'))
                st.write("**Content Length:**", results.get('content_length', 0))
            
            with col2:
                st.write("**Description:**", results.get('description', 'N/A')[:200] + "..." if len(results.get('description', '')) > 200 else results.get('description', 'N/A'))
                st.write("**Structured Items:**", results.get('structured_data_count', 0))
    
    with tab2:
        st.subheader("📄 Raw Data")
        
        # JSON display with syntax highlighting
        st.json(results)
    
    with tab3:
        st.subheader("📊 Analytics")
        
        if results.get('scraping_mode') == 'pagination':
            items = results.get('items', [])
            if items:
                # Create analytics charts
                
                # Links distribution
                links_data = [len(item.get('links', [])) for item in items]
                fig_links = px.histogram(x=links_data, title="Distribution of Links per Item", 
                                       labels={'x': 'Number of Links', 'y': 'Count'})
                st.plotly_chart(fig_links, use_container_width=True)
                
                # Images distribution
                images_data = [len(item.get('images', [])) for item in items]
                fig_images = px.histogram(x=images_data, title="Distribution of Images per Item",
                                        labels={'x': 'Number of Images', 'y': 'Count'})
                st.plotly_chart(fig_images, use_container_width=True)
                
                # Deep links analysis
                if any(item.get('extracted_from_links') for item in items):
                    deep_links_data = [len(item.get('extracted_from_links', [])) for item in items]
                    fig_deep = px.bar(x=range(1, len(deep_links_data) + 1), y=deep_links_data,
                                     title="Deep Links Extracted per Item",
                                     labels={'x': 'Item Number', 'y': 'Deep Links Count'})
                    st.plotly_chart(fig_deep, use_container_width=True)
            else:
                st.info("No data available for analytics")
        else:
            st.info("Analytics are available for pagination mode only")
    
    with tab4:
        st.subheader("🔍 Deep Links Analysis")
        
        if results.get('scraping_mode') == 'pagination':
            items = results.get('items', [])
            deep_link_items = [item for item in items if item.get('extracted_from_links')]
            
            if deep_link_items:
                for i, item in enumerate(deep_link_items):
                    with st.expander(f"🔗 Item {i+1}: {item.get('title', 'Untitled')[:50]}..."):
                        
                        st.write("**Original Item:**")
                        st.write(f"- Title: {item.get('title', 'N/A')}")
                        st.write(f"- Description: {item.get('description', 'N/A')[:100]}...")
                        
                        st.write("**Extracted from Links:**")
                        for j, link_data in enumerate(item.get('extracted_from_links', [])):
                            st.write(f"**Link {j+1}:** {link_data.get('url', 'N/A')}")
                            st.write(f"- Title: {link_data.get('title', 'N/A')}")
                            st.write(f"- Description: {link_data.get('description', 'N/A')}")
                            st.write(f"- Content Length: {link_data.get('content_length', 0)}")
                            
                            if link_data.get('structured_data'):
                                st.write(f"- Structured Data Items: {len(link_data['structured_data'])}")
                                with st.expander(f"View structured data from link {j+1}"):
                                    st.json(link_data['structured_data'])
                            st.write("---")
            else:
                st.info("No deep link extraction data available")
        else:
            st.info("Deep link analysis is available for pagination mode only")

if __name__ == "__main__":
    main()
