from flask import Blueprint,request, render_template
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer

summarize = Blueprint('example_blueprint', __name__)

@summarize.route('/summarize', methods= ["POST"])
def index():
    form_data = dict(request.form)
    print(form_data)
    text=form_data['text']
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    
    # Remove stopwords and stem the remaining words
    stop_words = set(stopwords.words('english'))
    ps = PorterStemmer()
    stemmed_words = [ps.stem(word) for word in words if not word in stop_words]
    
    # Calculate the frequency of each stemmed word
    freq_dist = nltk.FreqDist(stemmed_words)
    
    # Sort the sentences by their total frequency of important words
    sentence_scores = {}
    for i, sentence in enumerate(sentences):
        words_in_sentence = word_tokenize(sentence)
        stemmed_words_in_sentence = [ps.stem(word) for word in words_in_sentence if not word in stop_words]
        sentence_scores[i] = sum([freq_dist[word] for word in stemmed_words_in_sentence])
    
    top_n_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:2]
    summary = " ".join([sentences[i] for i in sorted(top_n_sentences)])
    
    return render_template("home.html",summary_text=summary)
