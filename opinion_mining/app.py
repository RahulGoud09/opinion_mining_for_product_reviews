from flask import Flask, render_template, request, jsonify
from .data_collection.review_scraper import ReviewScraper
from .preprocessing.text_processor import TextProcessor
from .sentiment_analysis.sentiment_analyzer import SentimentAnalyzer
from .utils.logger import setup_logger
import json
import os
import traceback

# Get the absolute path to the templates directory
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
app = Flask(__name__, template_folder=template_dir)
logger = setup_logger()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            # Get input data
            product_url = request.form.get('product_url', '')
            review_text = request.form.get('review_text', '')
            
            logger.info(f"Received request - URL: {product_url}, Text: {review_text[:50]}...")
            
            # Initialize components
            scraper = ReviewScraper()
            processor = TextProcessor()
            analyzer = SentimentAnalyzer()
            
            # Collect reviews
            reviews = []
            if product_url:
                logger.info(f"Collecting reviews from URL: {product_url}")
                reviews = scraper.collect_reviews(product_url, max_reviews=10)
                logger.info(f"Collected {len(reviews)} reviews")
            elif review_text:
                logger.info("Processing direct review text input")
                # Create a single review from the text input
                reviews = [{
                    'rating': 0.0,  # Default rating for text input
                    'title': 'User Review',
                    'text': review_text,
                    'date': '2024-03-15',
                    'verified': False
                }]
                logger.info("Created single review from text input")
            
            if not reviews:
                logger.warning("No reviews found")
                return render_template('predict.html', error="No reviews found. Please try again.")
            
            # Process and analyze reviews
            processed_reviews = []
            sentiments = []
            
            for i, review in enumerate(reviews):
                try:
                    # Process review text
                    processed_text = processor._preprocess_text(review['text'])
                    processed_reviews.append({
                        'original': review['text'],
                        'processed': processed_text,
                        'rating': review['rating'],
                        'title': review['title'],
                        'date': review['date'],
                        'verified': review['verified']
                    })
                    
                    # Analyze sentiment
                    review_data = [{
                        'processed_text': processed_text,
                        'rating': review['rating']
                    }]
                    sentiment_results = analyzer.analyze_sentiment(review_data)
                    sentiment = sentiment_results[0]['sentiment']['combined']['label']
                    sentiments.append(sentiment)
                    logger.info(f"Processed review {i+1}/{len(reviews)} - Sentiment: {sentiment}")
                except Exception as e:
                    logger.error(f"Error processing review {i+1}: {str(e)}")
                    logger.error(traceback.format_exc())
                    raise
            
            # Calculate statistics
            total_reviews = len(reviews)
            positive_count = sum(1 for s in sentiments if s == 'positive')
            negative_count = sum(1 for s in sentiments if s == 'negative')
            neutral_count = sum(1 for s in sentiments if s == 'neutral')
            
            # Calculate percentages
            positive_percent = (positive_count / total_reviews) * 100
            negative_percent = (negative_count / total_reviews) * 100
            neutral_percent = (neutral_count / total_reviews) * 100
            
            # Calculate average rating
            avg_rating = sum(review['rating'] for review in reviews) / total_reviews
            
            # Generate insights
            insights = []
            if positive_count > negative_count:
                insights.append("Overall positive sentiment from customers")
            elif negative_count > positive_count:
                insights.append("Overall negative sentiment from customers")
            else:
                insights.append("Mixed customer sentiment")
            
            if avg_rating >= 4.0:
                insights.append("High average rating indicates customer satisfaction")
            elif avg_rating <= 2.0:
                insights.append("Low average rating suggests customer dissatisfaction")
            
            # Prepare results
            results = {
                'total_reviews': total_reviews,
                'positive_count': positive_count,
                'negative_count': negative_count,
                'neutral_count': neutral_count,
                'positive_percent': round(positive_percent, 1),
                'negative_percent': round(negative_percent, 1),
                'neutral_percent': round(neutral_percent, 1),
                'avg_rating': round(avg_rating, 1),
                'insights': insights,
                'reviews': processed_reviews,
                'sentiments': sentiments
            }
            
            logger.info("Successfully processed all reviews")
            return render_template('predict.html', results=results)
            
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            logger.error(traceback.format_exc())
            return render_template('predict.html', error=f"An error occurred: {str(e)}")
    
    return render_template('predict.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 