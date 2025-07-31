from PIL import Image, ImageEnhance, ImageFilter
import cv2
import numpy as np
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class ImageProcessor:
    def __init__(self):
        self.target_size = (512, 512)
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
    
    def preprocess_image(self, image_path: str) -> Image.Image:
        try:
            image = Image.open(image_path)
            
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            processed_image = self._enhance_image(image)
            
            processed_image = self._resize_image(processed_image)
            
            logger.info(f"Image preprocessed successfully: {image_path}")
            return processed_image
            
        except Exception as e:
            logger.error(f"Error preprocessing image {image_path}: {e}")
            raise e
    
    def _enhance_image(self, image: Image.Image) -> Image.Image:
        try:
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.2)
            
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(1.1)
            
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(1.05)
            
            return image
            
        except Exception as e:
            logger.warning(f"Image enhancement failed, using original: {e}")
            return image
    
    def _resize_image(self, image: Image.Image) -> Image.Image:
        try:
            original_size = image.size
            image.thumbnail(self.target_size, Image.Resampling.LANCZOS)
            
            new_image = Image.new('RGB', self.target_size, (0, 0, 0))
            
            paste_x = (self.target_size[0] - image.size[0]) // 2
            paste_y = (self.target_size[1] - image.size[1]) // 2
            
            new_image.paste(image, (paste_x, paste_y))
            
            logger.debug(f"Image resized from {original_size} to {self.target_size}")
            return new_image
            
        except Exception as e:
            logger.error(f"Error resizing image: {e}")
            raise e
    
    def validate_image(self, image_path: str) -> bool:
        try:
            with Image.open(image_path) as img:
                img.verify()
            
            file_extension = image_path.lower().split('.')[-1]
            if f'.{file_extension}' not in self.supported_formats:
                logger.warning(f"Unsupported format: {file_extension}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Image validation failed for {image_path}: {e}")
            return False
    
    def get_image_metadata(self, image_path: str) -> dict:
        try:
            with Image.open(image_path) as img:
                return {
                    'format': img.format,
                    'mode': img.mode,
                    'size': img.size,
                    'has_transparency': img.mode in ('RGBA', 'LA') or 'transparency' in img.info
                }
        except Exception as e:
            logger.error(f"Error getting image metadata: {e}")
            return {}
    
    def apply_clahe(self, image: Image.Image) -> Image.Image:
        try:
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            enhanced = clahe.apply(gray)
            
            enhanced_rgb = cv2.cvtColor(enhanced, cv2.COLOR_GRAY2RGB)
            
            return Image.fromarray(enhanced_rgb)
            
        except Exception as e:
            logger.warning(f"CLAHE enhancement failed, using original: {e}")
            return image