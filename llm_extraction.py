# crawler/llm_extraction.py
import os
import json
from typing import Dict, List, Optional, Any, Type
from pydantic import BaseModel
from crawl4ai import LLMExtractionStrategy
from base_scraper import ContentType
from dotenv import load_dotenv
load_dotenv()

class GenericDataModel(BaseModel):
    """Generic data model for flexible content extraction"""
    title: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    links: Optional[List[str]] = None
    images: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None

class ArticleModel(BaseModel):
    """Model for article content"""
    title: str
    author: Optional[str] = None
    publish_date: Optional[str] = None
    content: str
    tags: Optional[List[str]] = None
    category: Optional[str] = None

class ProductModel(BaseModel):
    """Model for product information"""
    name: str
    price: Optional[str] = None
    description: Optional[str] = None
    rating: Optional[float] = None
    reviews: Optional[int] = None
    availability: Optional[str] = None
    images: Optional[List[str]] = None

class ContactModel(BaseModel):
    """Model for contact information"""
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    website: Optional[str] = None

def get_llm_strategy_for_content_type(
    content_type: ContentType,
    custom_model: Optional[Type[BaseModel]] = None,
    custom_instruction: Optional[str] = None
) -> Optional[LLMExtractionStrategy]:
    """
    Returns an LLM extraction strategy based on content type.
    
    Args:
        content_type: The type of content to extract
        custom_model: Optional custom Pydantic model for extraction
        custom_instruction: Optional custom instruction for the LLM
        
    Returns:
        LLMExtractionStrategy or None if no API key is available
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Warning: GROQ_API_KEY not found. LLM extraction will be skipped.")
        return None
    
    # Select model and instruction based on content type
    if custom_model and custom_instruction:
        model = custom_model
        instruction = custom_instruction
    else:
        model, instruction = _get_default_model_and_instruction(content_type)
    
    return LLMExtractionStrategy(
        provider=os.getenv("MODEL"),
        api_token=os.getenv("GEMINI_API_KEY"),
        schema=model.model_json_schema(),
        extraction_type="schema",
        instruction=instruction,
        input_format="markdown",
        verbose=True,
    )

def _get_default_model_and_instruction(content_type: ContentType) -> tuple[Type[BaseModel], str]:
    """Get default model and instruction for a content type"""
    
    if content_type == ContentType.ARTICLE:
        return ArticleModel, (
            "Extract article information including title, author, publish date, "
            "main content, tags, and category from the following content."
        )
    
    elif content_type == ContentType.PRODUCT:
        return ProductModel, (
            "Extract product information including name, price, description, "
            "rating, number of reviews, availability status, and image URLs "
            "from the following content."
        )
    
    elif content_type == ContentType.PROFILE:
        return ContactModel, (
            "Extract contact information including name, email, phone, "
            "address, and website from the following content."
        )
    
    else:  # Generic or unknown content
        return GenericDataModel, (
            "Extract general information including title, description, "
            "main content, links, images, and any relevant metadata "
            "from the following content."
        )

def get_generic_llm_strategy(
    instruction: str = None,
    model_class: Type[BaseModel] = None
) -> Optional[LLMExtractionStrategy]:
    """
    Get a generic LLM strategy with custom parameters.
    
    Args:
        instruction: Custom instruction for the LLM
        model_class: Custom Pydantic model class
        
    Returns:
        LLMExtractionStrategy or None if no API key
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None
    
    # Use defaults if not provided
    if not model_class:
        model_class = GenericDataModel
    
    if not instruction:
        instruction = (
            "Extract all relevant information from the following content. "
            "Focus on identifying key data points, structured information, "
            "and important details that would be valuable for analysis."
        )
    
    return LLMExtractionStrategy(
        provider="groq/deepseek-r1-distill-llama-70b",
        api_token=api_key,
        schema=model_class.model_json_schema(),
        extraction_type="schema",
        instruction=instruction,
        input_format="markdown",
        verbose=True,
    )

def process_llm_extracted_data(
    extracted_content: str,
    content_type: ContentType
) -> List[Dict]:
    """
    Process and validate LLM extracted content.
    
    Args:
        extracted_content: JSON string from LLM extraction
        content_type: Type of content that was extracted
        
    Returns:
        List of validated data dictionaries
    """
    try:
        # Parse the JSON content
        if not extracted_content:
            return []
        
        data = json.loads(extracted_content)
        if not data:
            return []
        
        # Ensure data is a list
        if not isinstance(data, list):
            data = [data]
        
        processed_data = []
        for item in data:
            # Clean up the item
            if isinstance(item, dict):
                # Remove error keys if they're False
                if item.get("error") is False:
                    item.pop("error", None)
                
                # Validate that the item has meaningful content
                if _is_valid_extracted_item(item, content_type):
                    processed_data.append(item)
        
        return processed_data
    
    except json.JSONDecodeError as e:
        print(f"Error parsing extracted content: {e}")
        return []
    except Exception as e:
        print(f"Error processing extracted data: {e}")
        return []

def _is_valid_extracted_item(item: Dict, content_type: ContentType) -> bool:
    """Check if an extracted item is valid based on content type"""
    
    if content_type == ContentType.ARTICLE:
        return bool(item.get("title") and item.get("content"))
    
    elif content_type == ContentType.PRODUCT:
        return bool(item.get("name"))
    
    elif content_type == ContentType.PROFILE:
        return bool(item.get("name") or item.get("email") or item.get("phone"))
    
    else:  # Generic content
        # Check if item has at least one meaningful field
        meaningful_fields = ["title", "description", "content", "name"]
        return any(item.get(field) for field in meaningful_fields)

async def check_no_results_llm(
    content: str,
    no_results_indicators: List[str] = None
) -> bool:
    """
    Use LLM to intelligently detect if a page indicates no results.
    
    Args:
        content: The page content to analyze
        no_results_indicators: List of phrases that indicate no results
        
    Returns:
        True if no results are detected, False otherwise
    """
    if not no_results_indicators:
        no_results_indicators = [
            "No Results Found",
            "No results",
            "Nothing found",
            "0 results",
            "No matches",
            "No items found",
            "Empty results",
            "No data available"
        ]
    
    # Simple text-based check first
    content_lower = content.lower()
    for indicator in no_results_indicators:
        if indicator.lower() in content_lower:
            return True
    
    # Could be enhanced with LLM analysis for more sophisticated detection
    return False
