import spacy
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os

class WordFreq:
    @staticmethod
    def generate_word_cloud(text, n):
        # Load the spaCy English model
        nlp = spacy.load('en_core_web_sm')

        # Process the text with spaCy
        doc = nlp(text)

        # Filter out stop words and punctuation marks
        words = [token.text for token in doc if not token.is_stop and not token.is_punct]

        # Count word frequencies
        word_counts = Counter(words)

        # Select the top n words
        top_n_words = dict(word_counts.most_common(n))

        # Generate word cloud image
        wordcloud = WordCloud()
        wordcloud = WordCloud(background_color='white')
        wordcloud.generate_from_frequencies(top_n_words)

        # Save the word cloud image
        image_path = "static/wordcloud.png"  # Image path relative to the current directory
        wordcloud.to_file(image_path)

        return image_path
