# Cambridge Dictionary Web Application

A modern web application that provides UK English dictionary definitions using the Cambridge Dictionary API. This application displays word definitions, pronunciations, parts of speech, and example sentences in a user-friendly interface.

## Features

- Search for any English word
- View UK English definitions
- See UK English pronunciation in IPA format
- Browse example sentences for each sense of the word
- View different forms of the word (noun/verb/adjective)
- Modern, responsive user interface
- Supports idioms and phrasal verbs
- Comprehensive UK English pronunciation guide with IPA symbols

## Installation

1. Clone this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Run the Flask application:

```bash
python app.py
```

2. Open your web browser and navigate to `http://127.0.0.1:5000`
3. Enter a word in the search box and click "Search"

## Dependencies

- Flask: Web framework for the backend
- Requests: For making HTTP requests
- BeautifulSoup4: For parsing HTML content
- lxml: XML/HTML parser for BeautifulSoup

## Project Structure

```
├── app.py                 # Flask application
├── requirements.txt       # Project dependencies
├── static/                # Static files
│   ├── css/               # CSS stylesheets
│   │   ├── style.css      # Main stylesheet
│   │   └── pronunciation.css # Pronunciation guide stylesheet
│   └── js/                # JavaScript files
│       └── script.js      # Main JavaScript file
├── templates/             # HTML templates
│   ├── index.html         # Main dictionary page
│   └── pronunciation_guide.html # UK English pronunciation guide
```

## Example

Searching for the word "run" will display:
- Meanings (as noun, verb, idiom, phrasal verb)
- IPA: /rʌn/ (UK)
- All examples for each meaning

This application uses web scraping with BeautifulSoup to fetch dictionary data from the Cambridge Dictionary website and Flask to serve it through a web interface.