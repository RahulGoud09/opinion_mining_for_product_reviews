import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from typing import List, Dict
import pandas as pd
from ..utils.logger import setup_logger

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')

logger = setup_logger()

class TextProcessor:
    """
    A class for preprocessing text data from product reviews.
    """
    
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        
    def preprocess_reviews(self, reviews: List[Dict]) -> List[Dict]:
        """
        Preprocess a list of review dictionaries.
        
        Args:
            reviews (List[Dict]): List of review dictionaries
            
        Returns:
            List[Dict]: List of preprocessed review dictionaries
        """
        processed_reviews = []
        
        for review in reviews:
            try:
                processed_text = self._preprocess_text(review['text'])
                review['processed_text'] = processed_text
                processed_reviews.append(review)
            except Exception as e:
                logger.error(f"Error preprocessing review: {str(e)}")
                continue
                
        return processed_reviews
    
    def _preprocess_text(self, text: str) -> str:
        """
        Preprocess a single text string.
        
        Args:
            text (str): Input text to preprocess
            
        Returns:
            str: Preprocessed text
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and numbers
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stopwords and lemmatize
        tokens = [self.lemmatizer.lemmatize(token) 
                 for token in tokens 
                 if token not in self.stop_words]
        
        # Join tokens back into text
        return ' '.join(tokens)
    
    def detect_fake_reviews(self, reviews: List[Dict]) -> List[Dict]:
        """
        Detect potential fake reviews using various heuristics.
        
        Args:
            reviews (List[Dict]): List of review dictionaries
            
        Returns:
            List[Dict]: List of reviews with fake review detection results
        """
        for review in reviews:
            review['is_potentially_fake'] = self._check_fake_review(review)
        return reviews
    
    def _check_fake_review(self, review: Dict) -> bool:
        """
        Check if a review is potentially fake using various heuristics.
        
        Args:
            review (Dict): Review dictionary
            
        Returns:
            bool: True if review is potentially fake, False otherwise
        """
        # Check for extreme ratings
        if review['rating'] in [1, 5]:
            return True
            
        # Check for very short reviews
        if len(review['text'].split()) < 5:
            return True
            
        # Check for repetitive text
        words = review['text'].lower().split()
        if len(set(words)) / len(words) < 0.5:
            return True
            
        # Check for verified purchase status
        if not review.get('verified', False):
            return True
            
        return False 