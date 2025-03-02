#!/bin/bash

# Download NLTK stopwords
python -c "import nltk; nltk.download('stopwords')"

# Download SpaCy model
python -m spacy download en_core_web_sm
