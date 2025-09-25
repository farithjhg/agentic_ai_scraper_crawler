#!/usr/bin/env python3
"""
Installation script for the Advanced Web Scraper
"""
import subprocess
import sys
import os

def install_dependencies():
    """Install the required dependencies"""
    
    print("🚀 Installing Advanced Web Scraper Dependencies")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("requirements.txt"):
        print("❌ Error: requirements.txt not found")
        print("   Please run this script from the crawler directory")
        return False
    
    try:
        # Install dependencies
        print("📦 Installing dependencies...")
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True)
        
        print("✅ Dependencies installed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def verify_installation():
    """Verify that all dependencies are installed correctly"""
    
    print("\n🔍 Verifying Installation")
    print("=" * 30)
    
    dependencies = [
        ("crawl4ai", "Crawl4AI"),
        ("pydantic", "Pydantic"),
        ("streamlit", "Streamlit"),
        ("plotly", "Plotly"),
        ("pandas", "Pandas"),
        ("trafilatura", "Trafilatura"),
        ("bs4", "BeautifulSoup4"),
        ("lxml", "LXML"),
    ]
    
    all_good = True
    
    for module, name in dependencies:
        try:
            __import__(module)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name} - Not found")
            all_good = False
    
    return all_good

def check_api_key():
    """Check if GROQ API key is set"""
    
    print("\n🔑 API Key Check")
    print("=" * 20)
    
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key:
        print("✅ GROQ_API_KEY found")
        print("🧠 LLM features will be available")
    else:
        print("⚠️ GROQ_API_KEY not found")
        print("💡 To enable LLM features:")
        print("   1. Get a free API key from https://console.groq.com/")
        print("   2. Set it: export GROQ_API_KEY='your-key-here'")
        print("   3. Or add it to your .env file")

def main():
    """Main installation process"""
    
    print("🕷️ Advanced Web Scraper - Installation")
    print("=" * 60)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Installation failed!")
        return 1
    
    # Verify installation
    if not verify_installation():
        print("\n⚠️ Some dependencies are missing. Please check the errors above.")
        return 1
    
    # Check API key
    check_api_key()
    
    print("\n🎉 Installation completed successfully!")
    print("\n📚 Next steps:")
    print("   • CLI: python -m crawler.cli https://example.com")
    print("   • UI:  python -m streamlit run streamlit_app.py")
    print("   • Demo: python demo.py")
    
    return 0

if __name__ == "__main__":
    exit(main())
