import requests
import base64
import io
from PIL import Image
import logging
import asyncio
import os
from typing import Optional, Dict, Any
import aiohttp
import json

logger = logging.getLogger(__name__)

class MedGemmaModel:
    def __init__(self):
        self.model_name = "google/medgemma-4b-it"
        self.hf_api_url = f"https://api-inference.huggingface.co/models/{self.model_name}"
        self.is_loaded = False
        self.api_token = os.getenv("HUGGINGFACE_API_TOKEN")
        
        if not self.api_token:
            logger.warning("HUGGINGFACE_API_TOKEN not found. You'll need to set this environment variable.")
        
    async def load_model(self):
        """Initialize the Hugging Face API connection"""
        try:
            logger.info("Initializing Hugging Face Inference API connection...")
            
            # Test API connection
            if await self._test_api_connection():
                self.is_loaded = True
                logger.info("✅ Hugging Face API connection established successfully")
            else:
                raise Exception("Failed to connect to Hugging Face API")
                
        except Exception as e:
            logger.error(f"❌ Error connecting to Hugging Face API: {e}")
            raise e
    
    async def _test_api_connection(self) -> bool:
        """Test if the API is accessible and the model is available"""
        try:
            headers = {"Authorization": f"Bearer {self.api_token}"} if self.api_token else {}
            
            # Create a small test image
            test_image = Image.new('RGB', (100, 100), color='white')
            
            async with aiohttp.ClientSession() as session:
                # Convert image to base64
                buffered = io.BytesIO()
                test_image.save(buffered, format="PNG")
                img_base64 = base64.b64encode(buffered.getvalue()).decode()
                
                # Test payload
                payload = {
                    "inputs": {
                        "image": img_base64,
                        "text": "Test connection"
                    },
                    "parameters": {
                        "max_new_tokens": 10
                    }
                }
                
                async with session.post(
                    self.hf_api_url,
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        return True
                    elif response.status == 503:
                        # Model is loading
                        logger.info("Model is loading on Hugging Face. This may take a few minutes...")
                        return True
                    else:
                        logger.error(f"API test failed with status {response.status}")
                        return False
                        
        except Exception as e:
            logger.error(f"API connection test failed: {e}")
            return False
    
    def _create_tb_focused_prompt(self) -> str:
        return """You are an expert radiologist specializing in tuberculosis detection from chest X-rays. 

Please analyze this chest X-ray image carefully and provide a detailed report focusing on:

1. Overall image quality and positioning
2. Lung fields examination (upper, middle, lower zones)
3. Specific signs of tuberculosis including:
   - Cavitary lesions
   - Consolidation patterns
   - Pleural effusion
   - Hilar lymphadenopathy
   - Miliary patterns
   - Fibrotic changes
   - Calcifications
4. Other relevant findings
5. Clinical correlation recommendations

Pay special attention to any findings that could suggest active or inactive tuberculosis. If you see any suspicious lesions, describe their location, size, and characteristics in detail.

Provide your assessment with confidence levels for any TB-related findings."""

    async def analyze_image(self, image: Image.Image) -> str:
        if not self.is_loaded:
            raise Exception("API connection not established")
        
        try:
            # Convert image to base64
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode()
            
            # Create the prompt
            prompt = self._create_tb_focused_prompt()
            user_prompt = "Please analyze this chest X-ray for tuberculosis and other findings:"
            
            # Prepare the API request
            headers = {
                "Authorization": f"Bearer {self.api_token}",
                "Content-Type": "application/json"
            } if self.api_token else {"Content-Type": "application/json"}
            
            # Try multiple API formats as HF API can vary
            payloads_to_try = [
                # Format 1: Standard multimodel format
                {
                    "inputs": {
                        "image": img_base64,
                        "text": f"{prompt}\n\n{user_prompt}"
                    },
                    "parameters": {
                        "max_new_tokens": 500,
                        "temperature": 0.3,
                        "top_p": 0.9,
                        "do_sample": True
                    }
                },
                # Format 2: Alternative format
                {
                    "inputs": f"{prompt}\n\n{user_prompt}",
                    "image": img_base64,
                    "parameters": {
                        "max_new_tokens": 500,
                        "temperature": 0.3
                    }
                },
                # Format 3: Simple format
                {
                    "inputs": {
                        "question": f"{prompt}\n\n{user_prompt}",
                        "image": img_base64
                    }
                }
            ]
            
            async with aiohttp.ClientSession() as session:
                for i, payload in enumerate(payloads_to_try):
                    try:
                        logger.info(f"Trying API format {i+1}/3...")
                        
                        async with session.post(
                            self.hf_api_url,
                            headers=headers,
                            json=payload,
                            timeout=aiohttp.ClientTimeout(total=120)  # 2 minutes timeout
                        ) as response:
                            
                            if response.status == 200:
                                result = await response.json()
                                return self._parse_api_response(result)
                            
                            elif response.status == 503:
                                error_text = await response.text()
                                if "loading" in error_text.lower():
                                    # Model is still loading, wait and retry
                                    logger.info("Model is loading, retrying in 30 seconds...")
                                    await asyncio.sleep(30)
                                    continue
                                else:
                                    raise Exception(f"Service unavailable: {error_text}")
                            
                            elif response.status == 422:
                                error_text = await response.text()
                                logger.warning(f"Format {i+1} failed with validation error: {error_text}")
                                continue  # Try next format
                            
                            else:
                                error_text = await response.text()
                                raise Exception(f"API request failed with status {response.status}: {error_text}")
                                
                    except asyncio.TimeoutError:
                        logger.warning(f"Format {i+1} timed out, trying next format...")
                        continue
                    except Exception as e:
                        logger.warning(f"Format {i+1} failed: {e}")
                        if i == len(payloads_to_try) - 1:  # Last format failed
                            raise e
                        continue
                
                raise Exception("All API formats failed")
            
        except Exception as e:
            logger.error(f"Error during image analysis: {e}")
            raise e
    
    def _parse_api_response(self, response) -> str:
        """Parse the API response and extract the generated text"""
        try:
            # Handle different response formats
            if isinstance(response, list) and len(response) > 0:
                first_item = response[0]
                if isinstance(first_item, dict):
                    # Check for 'generated_text' field
                    if 'generated_text' in first_item:
                        return first_item['generated_text']
                    # Check for 'answer' field (VQA format)
                    elif 'answer' in first_item:
                        return first_item['answer']
                    # Check for 'text' field
                    elif 'text' in first_item:
                        return first_item['text']
                elif isinstance(first_item, str):
                    return first_item
            
            elif isinstance(response, dict):
                # Direct dict response
                if 'generated_text' in response:
                    return response['generated_text']
                elif 'answer' in response:
                    return response['answer']
                elif 'text' in response:
                    return response['text']
            
            elif isinstance(response, str):
                return response
            
            # Fallback: return string representation
            logger.warning(f"Unexpected response format: {type(response)}")
            return str(response)
            
        except Exception as e:
            logger.error(f"Error parsing API response: {e}")
            return f"Error parsing response: {str(e)}"
    
    def get_model_info(self) -> Dict[str, Any]:
        return {
            "model_name": self.model_name,
            "api_url": self.hf_api_url,
            "is_loaded": self.is_loaded,
            "supports_multimodal": True,
            "max_tokens": 500,
            "deployment": "huggingface_api"
        }