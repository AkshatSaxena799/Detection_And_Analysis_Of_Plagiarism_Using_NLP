from serpapi import GoogleSearch
from flask import Flask, render_template, request
import requests
import difflib
import googlesearch as gs
from bs4 import BeautifulSoup
import requests
import math
import text_filter as filter

app = Flask(__name__)


def ngrams(input_text, n):
    # Create a list of n-grams for the input text
    input_text = input_text.lower()
    input_text = input_text.replace(" ", "")
    output = []
    for i in range(len(input_text)-n+1):
        output.append(input_text[i:i+n])
    return output


def ngram_containment(ngram_query, ngram_doc):
    # Calculate the n-gram containment between the query and the document
    ngram_query = set(ngram_query)
    ngram_doc = set(ngram_doc)
    if len(ngram_query) == 0:
        return 0.0
    return len(ngram_query.intersection(ngram_doc)) / float(len(ngram_query))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    input_text = filter.removeStopWord(request.form['input_text'])
    input_text=input_text.strip()
    # Search for top 5 results for input text on Google
    params = {
        "q": input_text,
        "location": " Bengaluru, Karnataka,  India",
        "hl": "en",
        "gl": "us",
        "google_domain": "google.com",
        "api_key": "API KEY"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    Parentlinks = results["organic_results"]
    search_results = []
    for i in range(5):
        search_results.append(Parentlinks[i]["link"])
    print(search_results)
    # Create an empty list to store the similarity results
    similarity_results = []
    dict_res = {}
    ngram_query = set(ngrams(input_text, 3))

    # Loop through each search result and extract content
    for result in search_results:
        try:
            # Get the HTML content of the search result
            response = requests.get(result)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract the text content from the HTML
            content = soup.get_text()

            # Calculate the n-gram containment between the query and the content
            ngram_content = set(ngrams(content, 3))
            containment = ngram_containment(ngram_query, ngram_content)

            # Add the containment and source of the content to the list
            similarity_results.append(
                {'url': result, 'containment': containment})
            dict_res[result] = math.ceil(containment*100)

        except Exception as e:
            # Handle any errors that occur during the search or extraction of content
            print(f"Error in processing {result}: {e}")

    # Render a template to display the similarity results
    return render_template('results.html', similarity_results=similarity_results)


if __name__ == '__main__':
    app.run(debug=True)
