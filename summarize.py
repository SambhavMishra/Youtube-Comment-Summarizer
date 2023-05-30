import nltk 
nltk.download('punkt') 
nltk.download('stopwords') 
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize, sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
from transformers import T5Tokenizer, T5ForConditionalGeneration
from heapq import nlargest
import re


class summarize():
    def __init__(self, n=3):
        self.n = n

    def extractive(self, text):
        # Preprocessing 
        text = re.sub(r'[A-Za-z]:\\.*?(\s|$)', '', text)

        # Remove stopwords 
        stop_words = set(stopwords.words('english')) 
        words = word_tokenize(text) 
        words = [word for word in words if not word.lower() in stop_words] 

        # Tokenize text 
        sentences = sent_tokenize(text)
        words = [word_tokenize(sentence) for sentence in sentences] 

        # Text representation 
        # Generate TF-IDF representation of the text 
        tfidf = TfidfVectorizer()
        tfidf_matrix = tfidf.fit_transform(sentences)

        # Sentence scoring 
        # Using frequency-based sentence scoring
        word_freq = defaultdict(int) 
        for sentence in sentences:
            for word in word_tokenize(sentence):
                word_freq[word] += 1

        sent_scores = defaultdict(int) 
        for sentence in sentences:
            for word in word_tokenize(sentence):
                if word in word_freq:
                    sent_scores[sentence] += word_freq[word] 

        # Select top n sentences with highest scores 
        n = self.n 
        summary_sentences = nlargest(n, sent_scores, key=sent_scores.get)

        # Summary generation 
        summary = ' '.join(summary_sentences)

        # Post-processing 
        summary = summary.replace('\n', ' ').replace('\r', '') 
        self.extractive_summary = summary.strip()

        return self.extractive_summary 
    
    def abstractive(self):
        model_path = 'abstractive_summarizer'  # Path to the saved model directory

        # Load the saved model
        tokenizer = T5Tokenizer.from_pretrained('t5-base')
        model = T5ForConditionalGeneration.from_pretrained(model_path)

        model.eval()
        input_text = 'summarize: ' + self.extractive_summary + ' </s>'
        input_ids = tokenizer.encode(input_text, return_tensors='pt')

        output_ids = model.generate(input_ids=input_ids, max_length=150, num_beams=2)

        summary = tokenizer.decode(output_ids[0], skip_special_tokens=True)
        return summary


if __name__ == "__main__":
    sum = summarize() 
    text = """Text summarization is a natural language processing (NLP) technique that involves the process of creating a shorter version of a longer text while retaining its most important information. The following are the general steps involved in text summarization in NLP:

    Preprocessing: This step involves cleaning and preparing the text for summarization. It may include removing stop words, punctuation, and special characters, tokenization, and sentence segmentation.
"""

    print(sum.abstractive(text))
