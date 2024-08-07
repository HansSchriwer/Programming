# To make the program more sophisticated, we can incorporate additional NLP techniques such as summarization, topic modeling, and sentiment analysis. 
We'll use spaCy for basic NLP, gensim for topic modeling, nltk for summarization, and TextBlob for sentiment analysis.
First, install the additional libraries:

pip install gensim nltk textblob
python -m textblob.download_corpora

## Next, here's the enhanced code:

import fitz  # PyMuPDF
from pdfminer.high_level import extract_text as extract_text_pdf
from docx import Document
import spacy
from collections import Counter
from gensim.summarization import summarize
from gensim.models import LdaModel
from gensim.corpora import Dictionary
from nltk.tokenize import sent_tokenize
from textblob import TextBlob

# Load the spaCy model
nlp = spacy.load('en_core_web_sm')

def extract_text_from_pdf(file_path):
    try:
        text = extract_text_pdf(file_path)
    except Exception as e:
        text = ''
    return text

def extract_text_from_word(file_path):
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def extract_key_points(text):
    doc = nlp(text)
    # Extracting the most common named entities
    entities = [ent.text for ent in doc.ents]
    entity_freq = Counter(entities).most_common(10)

    # Extracting the most common nouns and noun chunks
    noun_chunks = list(doc.noun_chunks)
    chunk_freq = Counter([chunk.text for chunk in noun_chunks]).most_common(10)

    return entity_freq, chunk_freq

def summarize_text(text):
    try:
        summary = summarize(text)
    except ValueError:
        summary = 'Text too short to summarize'
    return summary

def extract_topics(text, num_topics=5, num_words=5):
    # Tokenize the text and prepare for LDA
    sentences = [sent_tokenize(paragraph) for paragraph in text.split('\n') if paragraph]
    flat_sentences = [sentence for sublist in sentences for sentence in sublist]
    texts = [[word for word in sentence.lower().split()] for sentence in flat_sentences]

    # Create a dictionary and corpus for LDA
    dictionary = Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]

    # Build the LDA model
    lda = LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=10)
    topics = lda.print_topics(num_words=num_words)
    return topics

def sentiment_analysis(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment
    return sentiment

def main(file_path):
    if file_path.endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        text = extract_text_from_word(file_path)
    else:
        raise ValueError('Unsupported file format!')

    if text:
        # Extract key points
        entities, chunks = extract_key_points(text)

        # Summarize text
        summary = summarize_text(text)

        # Extract topics
        topics = extract_topics(text)

        # Sentiment analysis
        sentiment = sentiment_analysis(text)

        print('Most common named entities:')
        for entity, freq in entities:
            print(f'{entity}: {freq}')

        print('\nMost common noun chunks:')
        for chunk, freq in chunks:
            print(f'{chunk}: {freq}')

        print('\nSummary of the document:')
        print(summary)

        print('\nTopics in the document:')
        for topic in topics:
            print(topic)

        print('\nSentiment of the document:')
        print(f'Polarity: {sentiment.polarity}, Subjectivity: {sentiment.subjectivity}')
    else:
        print('No text found in the document!')

if __name__ == "__main__":
    # Replace 'your_document.pdf' or 'your_document.docx' with your file path
    main('your_document.pdf')

### Explanation of the New Features:
1.	Summarization: Uses gensim.summarization.summarize to provide a summary of the text.
2.	Topic Modeling: Uses gensim.models.LdaModel to extract topics from the text.
3.	Sentiment Analysis: Uses TextBlob to analyze the sentiment of the text.
Usage:
•	Replace 'your_document.pdf' or 'your_document.docx' with the path to your document.
•	The script will print the most common named entities, noun chunks, a summary, topics, and sentiment analysis to provide a comprehensive insight into the main information.
