import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag

def filter_words(tagged_words):
    """Filter words by allowed parts of speech"""
    filtered = []
    for word, pos in tagged_words:
        if pos in allowed_pos:
            filtered.append(word.lower())
    return filtered

path = 'PATH'

with open(path, 'r', encoding='utf-8') as file:
    all_texts = file.read()

tokens = word_tokenize(all_texts)
pos_tags = pos_tag(tokens, lang='rus')

# Nouns, verbs, adjectives, adverbs
allowed_pos = {'S', 'V', 'A', 'ADV'}

filtered_words = filter_words(pos_tags)

filtered_words = [word for word in filtered_words if len(word) >= 4]

word_counts = {}
for word in filtered_words:
    word_counts[word] = word_counts.get(word, 0) + 1

wordcloud = WordCloud(width=800, height=800, background_color='white', min_font_size=10).generate_from_frequencies(word_counts)

# Show
plt.figure(figsize=(8, 8), facecolor=None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad=0)

plt.show()