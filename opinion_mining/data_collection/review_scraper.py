import requests
from bs4 import BeautifulSoup
import pandas as pd
from typing import List, Dict
import time
import random
from ..utils.logger import setup_logger
import re

logger = setup_logger()

class ReviewScraper:
    """
    A class to scrape product reviews from various e-commerce platforms.
    """
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        # Sample data for different product categories
        self.sample_data = {
            'electronics': [
                {
                    'rating': 5.0,
                    'title': 'Exceptional Performance!',
                    'text': 'This laptop exceeded all my expectations. The battery life is outstanding, lasting over 10 hours on a single charge. The performance is smooth, handling multiple applications without any lag. The build quality is premium, and the keyboard is comfortable for long typing sessions.',
                    'date': '2024-03-15',
                    'verified': True
                },
                {
                    'rating': 4.0,
                    'title': 'Great Product with Minor Issues',
                    'text': 'Overall, this is a solid laptop. The performance is good, and the display is crisp. However, the fan can get quite loud under heavy load, and the battery life could be better. The price is reasonable for the features offered.',
                    'date': '2024-03-14',
                    'verified': True
                },
                {
                    'rating': 2.0,
                    'title': 'Disappointing Experience',
                    'text': 'The laptop started having issues within the first week. The screen occasionally flickers, and the battery drains very quickly. Customer service was unhelpful, and the warranty process is complicated. Would not recommend.',
                    'date': '2024-03-13',
                    'verified': False
                },
                {
                    'rating': 5.0,
                    'title': 'Best Purchase Ever!',
                    'text': 'I\'ve been using this laptop for 3 months now, and it\'s been perfect. The SSD makes everything lightning fast, and the 16GB RAM handles all my multitasking needs. The build quality is excellent, and the trackpad is very responsive.',
                    'date': '2024-03-12',
                    'verified': True
                },
                {
                    'rating': 3.0,
                    'title': 'Mixed Feelings',
                    'text': 'The laptop works well for basic tasks, but struggles with more demanding applications. The battery life is average, and the speakers are quite weak. The price is good, but you get what you pay for.',
                    'date': '2024-03-11',
                    'verified': True
                },
                {
                    'rating': 1.0,
                    'title': 'Complete Waste of Money',
                    'text': 'This is the worst laptop I\'ve ever owned. It overheats constantly, the keyboard is unresponsive, and the screen has dead pixels. The customer service was terrible, and they refused to accept the return. Stay away from this product!',
                    'date': '2024-03-10',
                    'verified': False
                },
                {
                    'rating': 4.0,
                    'title': 'Solid Choice for Professionals',
                    'text': 'A reliable laptop that handles work tasks well. The performance is consistent, and the build quality is good. The only downsides are the mediocre battery life and the slightly heavy weight. Overall, a good investment.',
                    'date': '2024-03-09',
                    'verified': True
                },
                {
                    'rating': 5.0,
                    'title': 'Perfect for My Needs',
                    'text': 'Exactly what I was looking for in a laptop. The performance is exceptional, the battery life is great, and the design is sleek. The fingerprint scanner is a nice touch for security. Highly recommended!',
                    'date': '2024-03-08',
                    'verified': True
                }
            ],
            'clothing': [
                {
                    'rating': 5.0,
                    'title': 'Perfect Fit and Quality!',
                    'text': 'These jeans fit perfectly and are incredibly comfortable. The material is high-quality denim that feels durable. The stitching is well done, and the color is exactly as shown in the pictures. Will definitely buy again!',
                    'date': '2024-03-15',
                    'verified': True
                },
                {
                    'rating': 4.0,
                    'title': 'Good Quality, Slightly Tight',
                    'text': 'The quality of the fabric is excellent, and the design is stylish. However, they run a bit small in the waist. I recommend sizing up. The color is rich and the material feels premium.',
                    'date': '2024-03-14',
                    'verified': True
                },
                {
                    'rating': 2.0,
                    'title': 'Poor Quality Material',
                    'text': 'The material is very thin and feels cheap. The stitching is coming undone after just two washes. The fit is inconsistent, and the color fades quickly. Not worth the money.',
                    'date': '2024-03-13',
                    'verified': False
                },
                {
                    'rating': 5.0,
                    'title': 'Stylish and Comfortable',
                    'text': 'Love the design and the comfort. The material is high quality and feels great against the skin. The fit is perfect, and the color is exactly as advertised. These are now my go-to jeans!',
                    'date': '2024-03-12',
                    'verified': True
                },
                {
                    'rating': 3.0,
                    'title': 'Average Quality',
                    'text': 'The jeans are okay for the price. The material is decent but not exceptional. They fit alright but stretch out after wearing. The color is slightly different from the picture.',
                    'date': '2024-03-11',
                    'verified': True
                },
                {
                    'rating': 1.0,
                    'title': 'Terrible Quality',
                    'text': 'These jeans are extremely poor quality. The material is paper-thin, the stitching is weak, and they ripped after the first wear. The sizing is completely off, and the color is nothing like the picture.',
                    'date': '2024-03-10',
                    'verified': False
                },
                {
                    'rating': 4.0,
                    'title': 'Great Value',
                    'text': 'Nice jeans at a reasonable price. The quality is good, and they fit well. The material is comfortable and durable. Would recommend for everyday wear.',
                    'date': '2024-03-09',
                    'verified': True
                },
                {
                    'rating': 3.0,
                    'title': 'Decent Product',
                    'text': 'The jeans are okay but nothing special. The material is average, and the fit is slightly loose. The color is nice, but they don\'t feel as premium as expected.',
                    'date': '2024-03-08',
                    'verified': False
                }
            ],
            'books': [
                {
                    'rating': 5.0,
                    'title': 'A Masterpiece!',
                    'text': 'This book is absolutely brilliant. The storytelling is captivating, and the character development is outstanding. The plot twists kept me on the edge of my seat, and the writing style is elegant and engaging. A must-read!',
                    'date': '2024-03-15',
                    'verified': True
                },
                {
                    'rating': 4.0,
                    'title': 'Engaging Read',
                    'text': 'A well-written book with an interesting plot. The characters are well-developed, and the story flows naturally. The ending could have been better, but overall, it\'s a satisfying read.',
                    'date': '2024-03-14',
                    'verified': True
                },
                {
                    'rating': 2.0,
                    'title': 'Disappointing',
                    'text': 'The story is slow and the characters are flat. The plot is predictable, and the writing style is dull. The book failed to engage me, and I struggled to finish it.',
                    'date': '2024-03-13',
                    'verified': False
                },
                {
                    'rating': 5.0,
                    'title': 'Couldn\'t Put It Down!',
                    'text': 'An absolutely gripping read from start to finish. The plot twists are masterfully crafted, and the character development is exceptional. The author\'s writing style is engaging and keeps you hooked.',
                    'date': '2024-03-12',
                    'verified': True
                },
                {
                    'rating': 4.0,
                    'title': 'Well-Written',
                    'text': 'The author\'s writing style is engaging and the story flows well. The characters are interesting, and the plot is well-structured. A few parts could have been more detailed.',
                    'date': '2024-03-11',
                    'verified': True
                },
                {
                    'rating': 3.0,
                    'title': 'Average Story',
                    'text': 'The book is okay but nothing special. The plot is predictable, and the characters are somewhat one-dimensional. The writing is decent but not exceptional.',
                    'date': '2024-03-10',
                    'verified': True
                },
                {
                    'rating': 5.0,
                    'title': 'A New Favorite',
                    'text': 'This book has become one of my all-time favorites. The character development is outstanding, and the world-building is rich and detailed. The plot is complex but well-executed.',
                    'date': '2024-03-09',
                    'verified': True
                },
                {
                    'rating': 2.0,
                    'title': 'Not Worth the Hype',
                    'text': 'The book didn\'t live up to the hype. The story is confusing and hard to follow. The characters are poorly developed, and the plot lacks coherence. Would not recommend.',
                    'date': '2024-03-08',
                    'verified': False
                }
            ],
            'default': [
                {
                    'rating': 5.0,
                    'title': 'Excellent Product!',
                    'text': 'This product exceeded all my expectations. The quality is outstanding, and it works perfectly. The design is elegant, and the functionality is exactly what I needed. Highly recommended!',
                    'date': '2024-03-15',
                    'verified': True
                },
                {
                    'rating': 4.0,
                    'title': 'Good Value',
                    'text': 'A solid product that delivers on its promises. The quality is good, and the performance is reliable. The price is reasonable for what you get. Would recommend to others.',
                    'date': '2024-03-14',
                    'verified': True
                },
                {
                    'rating': 3.0,
                    'title': 'Mixed Feelings',
                    'text': 'The product works but has some limitations. The quality is decent, but there are some minor issues. The price is fair, but you get what you pay for.',
                    'date': '2024-03-13',
                    'verified': False
                },
                {
                    'rating': 5.0,
                    'title': 'Perfect!',
                    'text': 'Exactly what I was looking for. The quality is exceptional, and the performance is outstanding. The design is beautiful, and it\'s very user-friendly. Worth every penny!',
                    'date': '2024-03-12',
                    'verified': True
                },
                {
                    'rating': 4.0,
                    'title': 'Worth the Money',
                    'text': 'Good product overall. The quality is reliable, and it works well. The design is nice, and the functionality meets my needs. Would buy again.',
                    'date': '2024-03-11',
                    'verified': True
                },
                {
                    'rating': 2.0,
                    'title': 'Not Worth It',
                    'text': 'The product is overpriced and doesn\'t work as advertised. The quality is poor, and it broke quickly. The customer service was unhelpful. Would not recommend.',
                    'date': '2024-03-10',
                    'verified': False
                },
                {
                    'rating': 5.0,
                    'title': 'Best Purchase Ever!',
                    'text': 'This is the best product I\'ve ever bought. The quality is top-notch, and it works perfectly. The design is beautiful, and it\'s very durable. Highly recommended!',
                    'date': '2024-03-09',
                    'verified': True
                },
                {
                    'rating': 3.0,
                    'title': 'Decent Product',
                    'text': 'The product is okay but nothing special. The quality is average, and it works fine. The price is reasonable, but there are better options available.',
                    'date': '2024-03-08',
                    'verified': True
                }
            ]
        }
    
    def collect_reviews(self, product_url=None, max_reviews=10):
        """
        Collect reviews from a product URL or return sample data
        
        Args:
            product_url (str): URL of the product to analyze
            max_reviews (int): Maximum number of reviews to return (default: 10)
            
        Returns:
            List[Dict]: List of review dictionaries
        """
        try:
            if product_url:
                # Extract category from URL
                category = self._extract_category(product_url)
                logger.info(f"Using sample data for category: {category}")
                reviews = self.sample_data.get(category, self.sample_data['default'])
                # Return only the requested number of reviews
                return reviews[:max_reviews]
            else:
                logger.info("No URL provided, using default sample data")
                return self.sample_data['default'][:max_reviews]
        except Exception as e:
            logger.error(f"Error collecting reviews: {str(e)}")
            return []

    def _extract_category(self, url):
        """
        Extract product category from URL
        """
        url_lower = url.lower()
        if any(word in url_lower for word in ['electronics', 'phone', 'laptop', 'computer', 'gadget']):
            return 'electronics'
        elif any(word in url_lower for word in ['clothing', 'shirt', 'dress', 'shoes', 'fashion']):
            return 'clothing'
        elif any(word in url_lower for word in ['book', 'novel', 'reading', 'literature']):
            return 'books'
        return 'default'

    def _clean_text(self, text):
        """
        Clean review text
        """
        if not text:
            return ""
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text.strip()

    def _extract_rating(self, rating_element):
        """
        Extract rating from HTML element
        """
        try:
            if rating_element:
                rating_text = rating_element.get_text().strip()
                # Extract first number from text
                rating_match = re.search(r'(\d+(?:\.\d+)?)', rating_text)
                if rating_match:
                    return float(rating_match.group(1))
        except Exception as e:
            logger.error(f"Error extracting rating: {str(e)}")
        return 0.0
    
    def _scrape_amazon(self, product_url: str) -> List[Dict]:
        """
        Scrape reviews from Amazon.
        
        Args:
            product_url (str): URL of the Amazon product
            
        Returns:
            List[Dict]: List of dictionaries containing review data
        """
        reviews = []
        page = 1
        
        while True:
            try:
                # Construct review URL
                review_url = f"{product_url}/ref=cm_cr_arp_d_paging_btm_next_{page}?ie=UTF8&reviewerType=all_reviews&pageNumber={page}"
                
                # Add delay to avoid rate limiting
                time.sleep(random.uniform(1, 3))
                
                response = requests.get(review_url, headers=self.headers)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract reviews
                review_elements = soup.find_all('div', {'data-hook': 'review'})
                
                if not review_elements:
                    break
                    
                for review in review_elements:
                    review_data = {
                        'rating': self._extract_rating(review.find('i', {'data-hook': 'review-star-rating'})),
                        'title': self._clean_text(review.find('a', {'data-hook': 'review-title'})),
                        'text': self._clean_text(review.find('span', {'data-hook': 'review-body'})),
                        'date': self._clean_text(review.find('span', {'data-hook': 'review-date'})),
                        'verified': bool(review.find('span', {'data-hook': 'avp-badge'}))
                    }
                    reviews.append(review_data)
                
                page += 1
                
            except Exception as e:
                logger.error(f"Error scraping Amazon page {page}: {str(e)}")
                break
                
        return reviews
    
    def _extract_title(self, review_element) -> str:
        """Extract title from review element."""
        try:
            title_element = review_element.find('a', {'data-hook': 'review-title'})
            return title_element.text.strip()
        except:
            return ""
    
    def _extract_text(self, review_element) -> str:
        """Extract review text from review element."""
        try:
            text_element = review_element.find('span', {'data-hook': 'review-body'})
            return text_element.text.strip()
        except:
            return ""
    
    def _extract_date(self, review_element) -> str:
        """Extract date from review element."""
        try:
            date_element = review_element.find('span', {'data-hook': 'review-date'})
            return date_element.text.strip()
        except:
            return ""
    
    def _is_verified(self, review_element) -> bool:
        """Check if review is verified purchase."""
        try:
            verified_element = review_element.find('span', {'data-hook': 'avp-badge'})
            return bool(verified_element)
        except:
            return False 