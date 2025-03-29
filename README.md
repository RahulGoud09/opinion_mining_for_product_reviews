# Opinion Mining for Product Reviews

A powerful web application that analyzes product reviews using advanced Natural Language Processing (NLP) techniques to provide detailed sentiment analysis and insights.

## Features

- **Multi-source Review Collection**: Collect reviews from product URLs or direct text input
- **Advanced Sentiment Analysis**: 
  - TextBlob-based sentiment analysis
  - Transformer-based sentiment analysis using DistilBERT
  - Rating-based sentiment analysis
  - Combined sentiment scoring
- **Fake Review Detection**: Identify potentially fake reviews using various metrics
- **Comprehensive Analysis**:
  - Overall sentiment analysis
  - Sentiment distribution visualization
  - Key insights generation
  - Individual review analysis
- **Modern UI**: Responsive and user-friendly interface

## Installation

1. Clone the repository:
```bash
git clone https://github.com/RahulGoud09/opinion_mining_for_product_reviews.git
cd opinion_mining_for_product_reviews
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Flask application:
```bash
python opinion_mining/app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Enter a product URL or review text and click "Analyze" to get detailed sentiment analysis.

## Project Structure

```
opinion_mining/
├── app.py                 # Main Flask application
├── data_collection/       # Review collection modules
├── preprocessing/         # Text preprocessing modules
├── sentiment_analysis/    # Sentiment analysis modules
├── templates/            # HTML templates
└── static/              # Static files (CSS, JS)
```

## Dependencies

- Flask >= 2.0.1
- NLTK >= 3.6.3
- TextBlob >= 0.15.3
- Transformers >= 4.11.3
- NumPy >= 1.21.2
- Pandas >= 1.3.3
- scikit-learn >= 0.24.2

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- NLTK for text processing
- TextBlob for sentiment analysis
- Hugging Face Transformers for advanced NLP
- Bootstrap for UI components 