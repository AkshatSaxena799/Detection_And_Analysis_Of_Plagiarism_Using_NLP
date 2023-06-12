import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag
import nltk
nltk.data.path.append("/path/to/nltk_data")
nltk.download('averaged_perceptron_tagger')


def removeStopWord(text):

    # Tokenize the text into individual words
    words = word_tokenize(text.lower())

    # Remove stop words from the list of words
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if not word in stop_words]

    # Tag each word with its part of speech
    tagged_words = pos_tag(filtered_words)

    # Remove words that are not nouns, verbs, or adjectives
    relevant_tags = ['NN', 'NNS', 'NNP', 'NNPS', 'VB', 'VBD',
                     'VBG', 'VBN', 'VBP', 'VBZ', 'JJ', 'JJR', 'JJS']
    relevant_words = [word for word,
                      tag in tagged_words if tag in relevant_tags]

    # Join the relevant words back into a string
    relevant_text = ' '.join(relevant_words)

    # returnthe relevant text
    return relevant_text
