from transformers import pipeline
from textblob import TextBlob
from typing import List, Dict
import numpy as np
from ..utils.logger import setup_logger

logger = setup_logger()

class SentimentAnalyzer:
    """
    A class for analyzing sentiment in product reviews using multiple approaches.
    """
    
    def __init__(self):
        try:
            # Initialize the transformer pipeline for sentiment analysis
            self.transformer_analyzer = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english"
            )
        except Exception as e:
            logger.error(f"Error initializing transformer model: {str(e)}")
            self.transformer_analyzer = None
    
    def analyze_sentiment(self, reviews: List[Dict]) -> List[Dict]:
        """
        Analyze sentiment for a list of reviews using multiple methods.
        
        Args:
            reviews (List[Dict]): List of review dictionaries
            
        Returns:
            List[Dict]: List of reviews with sentiment analysis results
        """
        analyzed_reviews = []
        
        for review in reviews:
            try:
                # Get sentiment from different methods
                textblob_sentiment = self._analyze_textblob(review['processed_text'])
                transformer_sentiment = self._analyze_transformer(review['processed_text'])
                
                # Consider rating in sentiment analysis
                rating_sentiment = self._get_rating_sentiment(review['rating'])
                
                # Combine results with weighted approach
                review['sentiment'] = {
                    'textblob': textblob_sentiment,
                    'transformer': transformer_sentiment,
                    'rating': rating_sentiment,
                    'combined': self._combine_sentiments(textblob_sentiment, transformer_sentiment, rating_sentiment)
                }
                analyzed_reviews.append(review)
                
            except Exception as e:
                logger.error(f"Error analyzing sentiment for review: {str(e)}")
                review['sentiment'] = {
                    'textblob': None,
                    'transformer': None,
                    'rating': None,
                    'combined': None
                }
                analyzed_reviews.append(review)
                
        return analyzed_reviews
    
    def _analyze_textblob(self, text: str) -> Dict:
        """
        Analyze sentiment using TextBlob.
        
        Args:
            text (str): Input text
            
        Returns:
            Dict: Sentiment analysis results
        """
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            
            # Convert polarity to sentiment label with more nuanced thresholds
            if polarity > 0.3:
                label = 'positive'
            elif polarity < -0.3:
                label = 'negative'
            else:
                label = 'neutral'
                
            return {
                'label': label,
                'score': abs(polarity)
            }
        except Exception as e:
            logger.error(f"Error in TextBlob analysis: {str(e)}")
            return None
    
    def _analyze_transformer(self, text: str) -> Dict:
        """
        Analyze sentiment using the transformer model.
        
        Args:
            text (str): Input text
            
        Returns:
            Dict: Sentiment analysis results
        """
        try:
            if self.transformer_analyzer:
                result = self.transformer_analyzer(text)[0]
                return {
                    'label': result['label'].lower(),
                    'score': result['score']
                }
            return None
        except Exception as e:
            logger.error(f"Error in transformer analysis: {str(e)}")
            return None
    
    def _get_rating_sentiment(self, rating: float) -> Dict:
        """
        Convert numerical rating to sentiment.
        
        Args:
            rating (float): Numerical rating (0-5)
            
        Returns:
            Dict: Sentiment analysis results
        """
        try:
            if rating >= 4.5:
                label = 'positive'
                score = 1.0
            elif rating >= 4.0:
                label = 'positive'
                score = 0.8
            elif rating >= 3.5:
                label = 'neutral'
                score = 0.6
            elif rating >= 3.0:
                label = 'neutral'
                score = 0.4
            elif rating >= 2.0:
                label = 'negative'
                score = 0.3
            else:
                label = 'negative'
                score = 0.1
                
            return {
                'label': label,
                'score': score
            }
        except Exception as e:
            logger.error(f"Error in rating sentiment analysis: {str(e)}")
            return None
    
    def _combine_sentiments(self, textblob: Dict, transformer: Dict, rating: Dict) -> Dict:
        """
        Combine sentiment analysis results from different methods.
        
        Args:
            textblob (Dict): TextBlob sentiment results
            transformer (Dict): Transformer sentiment results
            rating (Dict): Rating-based sentiment results
            
        Returns:
            Dict: Combined sentiment analysis results
        """
        try:
            # Initialize weights
            weights = {
                'textblob': 0.3,
                'transformer': 0.4,
                'rating': 0.3
            }
            
            # Initialize sentiment scores
            sentiment_scores = {
                'positive': 0.0,
                'negative': 0.0,
                'neutral': 0.0
            }
            
            # Add TextBlob results
            if textblob:
                sentiment_scores[textblob['label']] += textblob['score'] * weights['textblob']
            
            # Add transformer results
            if transformer:
                sentiment_scores[transformer['label']] += transformer['score'] * weights['transformer']
            
            # Add rating results
            if rating:
                sentiment_scores[rating['label']] += rating['score'] * weights['rating']
            
            # Get the sentiment with highest score
            max_sentiment = max(sentiment_scores.items(), key=lambda x: x[1])
            
            return {
                'label': max_sentiment[0],
                'score': max_sentiment[1],
                'details': {
                    'textblob': textblob,
                    'transformer': transformer,
                    'rating': rating
                }
            }
        except Exception as e:
            logger.error(f"Error combining sentiments: {str(e)}")
            return None 