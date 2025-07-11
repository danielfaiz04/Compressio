import spacy
from textblob import TextBlob
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Download necessary NLTK data
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except Exception:
    nltk.download('vader_lexicon')

# Load spaCy models
# Ensure these models are downloaded. You might need to run:
# python -m spacy download en_core_web_sm
# python -m spacy download id_core_news_sm
try:
    nlp_en = spacy.load("en_core_web_sm")
    logging.info("Loaded spaCy English model (en_core_web_sm).")
except OSError:
    logging.warning("spaCy English model (en_core_web_sm) not found. Please run 'python -m spacy download en_core_web_sm'")
    nlp_en = None

try:
    nlp_id = spacy.load("id_core_news_sm")
    logging.info("Loaded spaCy Indonesian model (id_core_news_sm).")
except OSError:
    logging.warning("spaCy Indonesian model (id_core_news_sm) not found. Please run 'python -m spacy download id_core_news_sm'")
    nlp_id = None

sia = SentimentIntensityAnalyzer()

def detect_language(text: str) -> str:
    """
    Detects the language of the given text using TextBlob.
    """
    try:
        return TextBlob(text).detect_language()
    except Exception as e:
        logging.warning(f"Language detection failed: {e}")
        return "en" # Default to English if detection fails

def detect_sensitive_entities(text):
    # Fungsi dummy, selalu mengembalikan list kosong
    return []

def analyze_sentiment(text: str) -> dict:
    """
    Analyzes the sentiment of the given text.
    Returns a dictionary with 'compound', 'neg', 'neu', 'pos' scores.
    """
    return sia.polarity_scores(text)

if __name__ == "__main__":
    # Example Usage
    text_en = "John Doe lives in New York and works at Google. His email is john.doe@example.com. He was born on 1990-01-15."
    text_id = "Bapak Budi Santoso tinggal di Jakarta. Nomor KTP beliau adalah 1234567890123456. Emailnya budi@contoh.com."

    print(f"\n--- English Text Analysis ---")
    print("Sensitive Entities:")
    for ent in detect_sensitive_entities(text_en):
        print(f"  - {ent.text} ({ent.label_})")
    print(f"Sentiment: {analyze_sentiment(text_en)}")

    print(f"\n--- Indonesian Text Analysis ---")
    print("Sensitive Entities:")
    for ent in detect_sensitive_entities(text_id):
        print(f"  - {ent.text} ({ent.label_})")
    print(f"Sentiment: {analyze_sentiment(text_id)}")

    text_mixed = "This is good. Ini bagus sekali. I love it."
    print(f"\n--- Mixed Language Analysis (will detect dominant) ---")
    print(f"Detected Language: {detect_language(text_mixed)}")
    print("Sensitive Entities:")
    for ent in detect_sensitive_entities(text_mixed):
        print(f"  - {ent.text} ({ent.label_})")
    print(f"Sentiment: {analyze_sentiment(text_mixed)}") 