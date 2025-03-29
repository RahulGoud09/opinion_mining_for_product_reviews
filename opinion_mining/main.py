import os
from dotenv import load_dotenv
from opinion_mining.data_collection.review_scraper import ReviewScraper
from opinion_mining.preprocessing.text_processor import TextProcessor
from opinion_mining.sentiment_analysis.sentiment_analyzer import SentimentAnalyzer
from opinion_mining.utils.logger import setup_logger

# Load environment variables
load_dotenv()

# Setup logging
logger = setup_logger()

def main():
    """
    Main execution function for the Opinion Mining project.
    """
    try:
        # Initialize components
        scraper = ReviewScraper()
        processor = TextProcessor()
        analyzer = SentimentAnalyzer()

        # Example product URL (replace with actual product URL)
        product_url = "https://www.amazon.com/product-reviews/B084DWCZY6"
        
        # Example workflow
        logger.info("Starting review collection...")
        reviews = scraper.collect_reviews(product_url=product_url)
        
        if not reviews:
            logger.warning("No reviews were collected. Please check the product URL and try again.")
            return
            
        logger.info(f"Successfully collected {len(reviews)} reviews")
        
        logger.info("Preprocessing reviews...")
        processed_reviews = processor.preprocess_reviews(reviews)
        
        logger.info("Analyzing sentiment...")
        sentiment_results = analyzer.analyze_sentiment(processed_reviews)
        
        # Print summary
        positive_count = sum(1 for r in sentiment_results if r['sentiment']['combined']['label'] == 'positive')
        negative_count = sum(1 for r in sentiment_results if r['sentiment']['combined']['label'] == 'negative')
        neutral_count = sum(1 for r in sentiment_results if r['sentiment']['combined']['label'] == 'neutral')
        
        logger.info(f"Analysis complete! Results:")
        logger.info(f"Positive reviews: {positive_count}")
        logger.info(f"Negative reviews: {negative_count}")
        logger.info(f"Neutral reviews: {neutral_count}")
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    main() 