import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
import nltk
from sklearn.metrics import silhouette_score

nltk.download('punkt')
nltk.download('stopwords')

# Input data
path = "PATH"
data = pd.read_excel(path)

def clean_text(text):
    if pd.isnull(text):
        return ""

    text = re.sub(r'[^\w\s]', '', str(text))

    text = text.lower()

    tokens = word_tokenize(text)

    stop_words = set(stopwords.words('russian'))
    tokens = [word for word in tokens if (word not in stop_words) and (len(word) > 4)]

    stemmer = SnowballStemmer('russian')
    tokens = [stemmer.stem(word) for word in tokens]
    return ' '.join(tokens)

def display_topics(model, feature_names, no_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic %d:" % (topic_idx+1))
        print(" ".join([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]]))

data['clean_text'] = data['Текст поста'].apply(clean_text)

tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=15, max_features=2000000)
tfidf = tfidf_vectorizer.fit_transform(data['clean_text'])

num_topics = 4  # Clusters number
nmf_model = NMF(n_components=num_topics, random_state=42)
nmf_model.fit(tfidf)

no_top_words = 15
feature_names = tfidf_vectorizer.get_feature_names_out()

print("Темы, выявленные с помощью NMF:")
display_topics(nmf_model, feature_names, no_top_words)

# Silhouette Score
silhouette_avg = silhouette_score(tfidf, nmf_model.transform(tfidf).argmax(axis=1))
print(f"Silhouette Score: {silhouette_avg}")