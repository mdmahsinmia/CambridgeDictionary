from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import re
import urllib.parse

app = Flask(__name__)

def get_cambridge_audio_url(word):
    """
    Get the audio URL from Cambridge Dictionary.
    """
    try:
        # Encode the word for URL
        encoded_word = urllib.parse.quote(word.lower())
        url = f'https://dictionary.cambridge.org/dictionary/english/{encoded_word}'
        
        # Send request with headers to mimic a browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the UK pronunciation audio element
        audio_element = soup.find('span', {'class': 'uk dpron-i'})
        if audio_element:
            source_element = audio_element.find('source', {'type': 'audio/mpeg'})
            if source_element and 'src' in source_element.attrs:
                audio_url = source_element['src']
                if not audio_url.startswith('http'):
                    audio_url = 'https://dictionary.cambridge.org' + audio_url
                return audio_url
        
        return None
        
    except Exception as e:
        print(f"Error fetching audio for word '{word}': {str(e)}")
        return None

def generate_audio_url(word):
    """
    Generate a URL for audio pronunciation using our proxy route.
    """
    return f'/audio/{urllib.parse.quote(word.lower())}'

@app.route('/audio/<word>')
def get_audio(word):
    try:
        # Get the Cambridge Dictionary audio URL
        audio_url = get_cambridge_audio_url(word)
        
        if audio_url:
            # Forward the request to Cambridge Dictionary
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Referer': 'https://dictionary.cambridge.org/'
            }
            response = requests.get(audio_url, headers=headers, stream=True)
            response.raise_for_status()
            
            # Return the audio file
            return response.content, 200, {
                'Content-Type': 'audio/mpeg',
                'Content-Disposition': f'inline; filename="{word}.mp3"'
            }
    except Exception as e:
        print(f"Error serving audio for word '{word}': {str(e)}")
    
    # If anything fails, return the placeholder
    return send_file('static/audio/placeholder.mp3', mimetype='audio/mpeg')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pronunciation-guide')
def pronunciation_guide():
    # UK English phonemes data
    vowels = [
        {
            'symbol': 'ɪ',
            'spellings': 'i, y, e, ui, a',
            'examples': [
                {'word': 'bit', 'pronunciation': 'bɪt', 'audio_url': generate_audio_url('bit')},
                {'word': 'women', 'pronunciation': 'wɪmɪn', 'audio_url': generate_audio_url('women')},
                {'word': 'busy', 'pronunciation': 'bɪzi', 'audio_url': generate_audio_url('busy')}
            ]
        },
        {
            'symbol': 'e',
            'spellings': 'e, ea, a, ai',
            'examples': [
                {'word': 'bed', 'pronunciation': 'bed', 'audio_url': generate_audio_url('bed')},
                {'word': 'head', 'pronunciation': 'hed', 'audio_url': generate_audio_url('head')},
                {'word': 'said', 'pronunciation': 'sed', 'audio_url': generate_audio_url('said')}
            ]
        },
        {
            'symbol': 'æ',
            'spellings': 'a',
            'examples': [
                {'word': 'cat', 'pronunciation': 'kæt', 'audio_url': generate_audio_url('cat')},
                {'word': 'hand', 'pronunciation': 'hænd', 'audio_url': generate_audio_url('hand')},
                {'word': 'apple', 'pronunciation': 'æpl', 'audio_url': generate_audio_url('apple')}
            ]
        },
        {
            'symbol': 'ʌ',
            'spellings': 'u, o, ou, oo',
            'examples': [
                {'word': 'cup', 'pronunciation': 'kʌp', 'audio_url': generate_audio_url('cup')},
                {'word': 'love', 'pronunciation': 'lʌv', 'audio_url': generate_audio_url('love')},
                {'word': 'blood', 'pronunciation': 'blʌd', 'audio_url': generate_audio_url('blood')}
            ]
        },
        {
            'symbol': 'ɒ',
            'spellings': 'o, a, au, ow',
            'examples': [
                {'word': 'hot', 'pronunciation': 'hɒt', 'audio_url': generate_audio_url('hot')},
                {'word': 'wash', 'pronunciation': 'wɒʃ', 'audio_url': generate_audio_url('wash')},
                {'word': 'want', 'pronunciation': 'wɒnt', 'audio_url': generate_audio_url('want')}
            ]
        },
        {
            'symbol': 'ʊ',
            'spellings': 'oo, u, ou',
            'examples': [
                {'word': 'book', 'pronunciation': 'bʊk', 'audio_url': generate_audio_url('book')},
                {'word': 'put', 'pronunciation': 'pʊt', 'audio_url': generate_audio_url('put')},
                {'word': 'could', 'pronunciation': 'kʊd', 'audio_url': generate_audio_url('could')}
            ]
        },
        {
            'symbol': 'iː',
            'spellings': 'ee, ea, e, ie, ei, i',
            'examples': [
                {'word': 'see', 'pronunciation': 'siː', 'audio_url': generate_audio_url('see')},
                {'word': 'meat', 'pronunciation': 'miːt', 'audio_url': generate_audio_url('meat')},
                {'word': 'these', 'pronunciation': 'ðiːz', 'audio_url': generate_audio_url('these')}
            ]
        },
        {
            'symbol': 'ɑː',
            'spellings': 'ar, a, al, er, ear',
            'examples': [
                {'word': 'car', 'pronunciation': 'kɑː', 'audio_url': generate_audio_url('car')},
                {'word': 'father', 'pronunciation': 'fɑːðə', 'audio_url': generate_audio_url('father')},
                {'word': 'heart', 'pronunciation': 'hɑːt', 'audio_url': generate_audio_url('heart')}
            ]
        },
        {
            'symbol': 'ɔː',
            'spellings': 'or, ore, aw, au, al, ar, oor, our',
            'examples': [
                {'word': 'more', 'pronunciation': 'mɔː', 'audio_url': generate_audio_url('more')},
                {'word': 'saw', 'pronunciation': 'sɔː', 'audio_url': generate_audio_url('saw')},
                {'word': 'thought', 'pronunciation': 'θɔːt', 'audio_url': generate_audio_url('thought')}
            ]
        },
        {
            'symbol': 'uː',
            'spellings': 'oo, u, ue, ew, ou, o',
            'examples': [
                {'word': 'food', 'pronunciation': 'fuːd', 'audio_url': generate_audio_url('food')},
                {'word': 'blue', 'pronunciation': 'bluː', 'audio_url': generate_audio_url('blue')},
                {'word': 'through', 'pronunciation': 'θruː', 'audio_url': generate_audio_url('through')}
            ]
        },
        {
            'symbol': 'ɜː',
            'spellings': 'er, ir, ur, ear, or',
            'examples': [
                {'word': 'bird', 'pronunciation': 'bɜːd', 'audio_url': generate_audio_url('bird')},
                {'word': 'work', 'pronunciation': 'wɜːk', 'audio_url': generate_audio_url('work')},
                {'word': 'learn', 'pronunciation': 'lɜːn', 'audio_url': generate_audio_url('learn')}
            ]
        },
        {
            'symbol': 'ə',
            'spellings': 'a, e, i, o, u (unstressed)',
            'examples': [
                {'word': 'about', 'pronunciation': 'əbaʊt', 'audio_url': generate_audio_url('about')},
                {'word': 'mother', 'pronunciation': 'mʌðə', 'audio_url': generate_audio_url('mother')},
                {'word': 'pencil', 'pronunciation': 'pensəl', 'audio_url': generate_audio_url('pencil')}
            ]
        }
    ]
    
    diphthongs = [
        {
            'symbol': 'eɪ',
            'spellings': 'a, ai, ay, ea, ey, ei',
            'examples': [
                {'word': 'face', 'pronunciation': 'feɪs', 'audio_url': generate_audio_url('face')},
                {'word': 'rain', 'pronunciation': 'reɪn', 'audio_url': generate_audio_url('rain')},
                {'word': 'day', 'pronunciation': 'deɪ', 'audio_url': generate_audio_url('day')}
            ]
        },
        {
            'symbol': 'aɪ',
            'spellings': 'i, y, ie, igh, ei, uy',
            'examples': [
                {'word': 'price', 'pronunciation': 'praɪs', 'audio_url': generate_audio_url('price')},
                {'word': 'high', 'pronunciation': 'haɪ', 'audio_url': generate_audio_url('high')},
                {'word': 'buy', 'pronunciation': 'baɪ', 'audio_url': generate_audio_url('buy')}
            ]
        },
        {
            'symbol': 'ɔɪ',
            'spellings': 'oi, oy',
            'examples': [
                {'word': 'choice', 'pronunciation': 'tʃɔɪs', 'audio_url': generate_audio_url('choice')},
                {'word': 'boy', 'pronunciation': 'bɔɪ', 'audio_url': generate_audio_url('boy')},
                {'word': 'noise', 'pronunciation': 'nɔɪz', 'audio_url': generate_audio_url('noise')}
            ]
        },
        {
            'symbol': 'əʊ',
            'spellings': 'o, oa, ow, oe, ol',
            'examples': [
                {'word': 'goat', 'pronunciation': 'gəʊt', 'audio_url': generate_audio_url('goat')},
                {'word': 'show', 'pronunciation': 'ʃəʊ', 'audio_url': generate_audio_url('show')},
                {'word': 'though', 'pronunciation': 'ðəʊ', 'audio_url': generate_audio_url('though')}
            ]
        },
        {
            'symbol': 'aʊ',
            'spellings': 'ou, ow',
            'examples': [
                {'word': 'mouth', 'pronunciation': 'maʊθ', 'audio_url': generate_audio_url('mouth')},
                {'word': 'now', 'pronunciation': 'naʊ', 'audio_url': generate_audio_url('now')},
                {'word': 'house', 'pronunciation': 'haʊs', 'audio_url': generate_audio_url('house')}
            ]
        },
        {
            'symbol': 'ɪə',
            'spellings': 'ear, eer, ere, ier',
            'examples': [
                {'word': 'near', 'pronunciation': 'nɪə', 'audio_url': generate_audio_url('near')},
                {'word': 'here', 'pronunciation': 'hɪə', 'audio_url': generate_audio_url('here')},
                {'word': 'beer', 'pronunciation': 'bɪə', 'audio_url': generate_audio_url('beer')}
            ]
        },
        {
            'symbol': 'eə',
            'spellings': 'air, are, ear, ere, eir',
            'examples': [
                {'word': 'square', 'pronunciation': 'skweə', 'audio_url': generate_audio_url('square')},
                {'word': 'care', 'pronunciation': 'keə', 'audio_url': generate_audio_url('care')},
                {'word': 'their', 'pronunciation': 'ðeə', 'audio_url': generate_audio_url('their')}
            ]
        },
        {
            'symbol': 'ʊə',
            'spellings': 'ure, our',
            'examples': [
                {'word': 'cure', 'pronunciation': 'kjʊə', 'audio_url': generate_audio_url('cure')},
                {'word': 'tour', 'pronunciation': 'tʊə', 'audio_url': generate_audio_url('tour')},
                {'word': 'pure', 'pronunciation': 'pjʊə', 'audio_url': generate_audio_url('pure')}
            ]
        }
    ]
    
    consonants = [
        {
            'symbol': 'p',
            'spellings': 'p, pp',
            'examples': [
                {'word': 'pen', 'pronunciation': 'pen', 'audio_url': generate_audio_url('pen')},
                {'word': 'happy', 'pronunciation': 'hæpi', 'audio_url': generate_audio_url('happy')},
                {'word': 'stop', 'pronunciation': 'stɒp', 'audio_url': generate_audio_url('stop')}
            ]
        },
        {
            'symbol': 'b',
            'spellings': 'b, bb',
            'examples': [
                {'word': 'bad', 'pronunciation': 'bæd', 'audio_url': generate_audio_url('bad')},
                {'word': 'rubber', 'pronunciation': 'rʌbə', 'audio_url': generate_audio_url('rubber')},
                {'word': 'job', 'pronunciation': 'dʒɒb', 'audio_url': generate_audio_url('job')}
            ]
        },
        {
            'symbol': 't',
            'spellings': 't, tt, ed',
            'examples': [
                {'word': 'tea', 'pronunciation': 'tiː', 'audio_url': generate_audio_url('tea')},
                {'word': 'better', 'pronunciation': 'betə', 'audio_url': generate_audio_url('better')},
                {'word': 'walked', 'pronunciation': 'wɔːkt', 'audio_url': generate_audio_url('walked')}
            ]
        },
        {
            'symbol': 'd',
            'spellings': 'd, dd, ed',
            'examples': [
                {'word': 'day', 'pronunciation': 'deɪ', 'audio_url': generate_audio_url('day')},
                {'word': 'ladder', 'pronunciation': 'lædə', 'audio_url': generate_audio_url('ladder')},
                {'word': 'played', 'pronunciation': 'pleɪd', 'audio_url': generate_audio_url('played')}
            ]
        },
        {
            'symbol': 'k',
            'spellings': 'k, c, ck, ch, cc, que',
            'examples': [
                {'word': 'key', 'pronunciation': 'kiː', 'audio_url': generate_audio_url('key')},
                {'word': 'cat', 'pronunciation': 'kæt', 'audio_url': generate_audio_url('cat')},
                {'word': 'school', 'pronunciation': 'skuːl', 'audio_url': generate_audio_url('school')}
            ]
        },
        {
            'symbol': 'g',
            'spellings': 'g, gg, gh, gue',
            'examples': [
                {'word': 'get', 'pronunciation': 'get', 'audio_url': generate_audio_url('get')},
                {'word': 'bigger', 'pronunciation': 'bɪgə', 'audio_url': generate_audio_url('bigger')},
                {'word': 'ghost', 'pronunciation': 'gəʊst', 'audio_url': generate_audio_url('ghost')}
            ]
        },
        {
            'symbol': 'f',
            'spellings': 'f, ff, ph, gh',
            'examples': [
                {'word': 'fat', 'pronunciation': 'fæt', 'audio_url': generate_audio_url('fat')},
                {'word': 'coffee', 'pronunciation': 'kɒfi', 'audio_url': generate_audio_url('coffee')},
                {'word': 'laugh', 'pronunciation': 'lɑːf', 'audio_url': generate_audio_url('laugh')}
            ]
        },
        {
            'symbol': 'v',
            'spellings': 'v, f',
            'examples': [
                {'word': 'voice', 'pronunciation': 'vɔɪs', 'audio_url': generate_audio_url('voice')},
                {'word': 'love', 'pronunciation': 'lʌv', 'audio_url': generate_audio_url('love')},
                {'word': 'of', 'pronunciation': 'ɒv', 'audio_url': generate_audio_url('of')}
            ]
        },
        {
            'symbol': 'θ',
            'spellings': 'th',
            'examples': [
                {'word': 'thin', 'pronunciation': 'θɪn', 'audio_url': generate_audio_url('thin')},
                {'word': 'mouth', 'pronunciation': 'maʊθ', 'audio_url': generate_audio_url('mouth')},
                {'word': 'bath', 'pronunciation': 'bɑːθ', 'audio_url': generate_audio_url('bath')}
            ]
        },
        {
            'symbol': 'ð',
            'spellings': 'th',
            'examples': [
                {'word': 'this', 'pronunciation': 'ðɪs', 'audio_url': generate_audio_url('this')},
                {'word': 'mother', 'pronunciation': 'mʌðə', 'audio_url': generate_audio_url('mother')},
                {'word': 'breathe', 'pronunciation': 'briːð', 'audio_url': generate_audio_url('breathe')}
            ]
        },
        {
            'symbol': 's',
            'spellings': 's, ss, c, ce, sc',
            'examples': [
                {'word': 'sun', 'pronunciation': 'sʌn', 'audio_url': generate_audio_url('sun')},
                {'word': 'miss', 'pronunciation': 'mɪs', 'audio_url': generate_audio_url('miss')},
                {'word': 'city', 'pronunciation': 'sɪti', 'audio_url': generate_audio_url('city')}
            ]
        },
        {
            'symbol': 'z',
            'spellings': 'z, zz, s, ss, x',
            'examples': [
                {'word': 'zoo', 'pronunciation': 'zuː', 'audio_url': generate_audio_url('zoo')},
                {'word': 'buzz', 'pronunciation': 'bʌz', 'audio_url': generate_audio_url('buzz')},
                {'word': 'is', 'pronunciation': 'ɪz', 'audio_url': generate_audio_url('is')}
            ]
        },
        {
            'symbol': 'ʃ',
            'spellings': 'sh, s, ss, ch, t, c, sc',
            'examples': [
                {'word': 'ship', 'pronunciation': 'ʃɪp', 'audio_url': generate_audio_url('ship')},
                {'word': 'sugar', 'pronunciation': 'ʃʊgə', 'audio_url': generate_audio_url('sugar')},
                {'word': 'machine', 'pronunciation': 'məʃiːn', 'audio_url': generate_audio_url('machine')}
            ]
        },
        {
            'symbol': 'ʒ',
            'spellings': 's, si, z, g, j',
            'examples': [
                {'word': 'measure', 'pronunciation': 'meʒə', 'audio_url': generate_audio_url('measure')},
                {'word': 'vision', 'pronunciation': 'vɪʒn', 'audio_url': generate_audio_url('vision')},
                {'word': 'beige', 'pronunciation': 'beɪʒ', 'audio_url': generate_audio_url('beige')}
            ]
        },
        {
            'symbol': 'h',
            'spellings': 'h, wh',
            'examples': [
                {'word': 'hat', 'pronunciation': 'hæt', 'audio_url': generate_audio_url('hat')},
                {'word': 'who', 'pronunciation': 'huː', 'audio_url': generate_audio_url('who')},
                {'word': 'behind', 'pronunciation': 'bɪhaɪnd', 'audio_url': generate_audio_url('behind')}
            ]
        },
        {
            'symbol': 'tʃ',
            'spellings': 'ch, tch, t, c',
            'examples': [
                {'word': 'chair', 'pronunciation': 'tʃeə', 'audio_url': generate_audio_url('chair')},
                {'word': 'church', 'pronunciation': 'tʃɜːtʃ', 'audio_url': generate_audio_url('church')},
                {'word': 'match', 'pronunciation': 'mætʃ', 'audio_url': generate_audio_url('match')},
                {'word': 'nature', 'pronunciation': 'neɪtʃə', 'audio_url': generate_audio_url('nature')}
            ]
        },
        {
            'symbol': 'dʒ',
            'spellings': 'j, g, dg, d, di',
            'examples': [
                {'word': 'judge', 'pronunciation': 'dʒʌdʒ', 'audio_url': generate_audio_url('judge')},
                {'word': 'gem', 'pronunciation': 'dʒem', 'audio_url': generate_audio_url('gem')},
                {'word': 'soldier', 'pronunciation': 'səʊldʒə', 'audio_url': generate_audio_url('soldier')}
            ]
        },
        {
            'symbol': 'm',
            'spellings': 'm, mm, mb, mn, lm',
            'examples': [
                {'word': 'man', 'pronunciation': 'mæn', 'audio_url': generate_audio_url('man')},
                {'word': 'summer', 'pronunciation': 'sʌmə', 'audio_url': generate_audio_url('summer')},
                {'word': 'comb', 'pronunciation': 'kəʊm', 'audio_url': generate_audio_url('comb')}
            ]
        },
        {
            'symbol': 'n',
            'spellings': 'n, nn, kn, gn, pn',
            'examples': [
                {'word': 'no', 'pronunciation': 'nəʊ', 'audio_url': generate_audio_url('no')},
                {'word': 'funny', 'pronunciation': 'fʌni', 'audio_url': generate_audio_url('funny')},
                {'word': 'know', 'pronunciation': 'nəʊ', 'audio_url': generate_audio_url('know')}
            ]
        },
        {
            'symbol': 'ŋ',
            'spellings': 'ng, n',
            'examples': [
                {'word': 'sing', 'pronunciation': 'sɪŋ', 'audio_url': generate_audio_url('sing')},
                {'word': 'think', 'pronunciation': 'θɪŋk', 'audio_url': generate_audio_url('think')},
                {'word': 'tongue', 'pronunciation': 'tʌŋ', 'audio_url': generate_audio_url('tongue')}
            ]
        },
        {
            'symbol': 'l',
            'spellings': 'l, ll',
            'examples': [
                {'word': 'leg', 'pronunciation': 'leg', 'audio_url': generate_audio_url('leg')},
                {'word': 'hello', 'pronunciation': 'heləʊ', 'audio_url': generate_audio_url('hello')},
                {'word': 'feel', 'pronunciation': 'fiːl', 'audio_url': generate_audio_url('feel')}
            ]
        },
        {
            'symbol': 'r',
            'spellings': 'r, rr, wr, rh',
            'examples': [
                {'word': 'red', 'pronunciation': 'red', 'audio_url': generate_audio_url('red')},
                {'word': 'sorry', 'pronunciation': 'sɒri', 'audio_url': generate_audio_url('sorry')},
                {'word': 'write', 'pronunciation': 'raɪt', 'audio_url': generate_audio_url('write')}
            ]
        },
        {
            'symbol': 'j',
            'spellings': 'y, i, j',
            'examples': [
                {'word': 'yes', 'pronunciation': 'jes', 'audio_url': generate_audio_url('yes')},
                {'word': 'onion', 'pronunciation': 'ʌnjən', 'audio_url': generate_audio_url('onion')},
                {'word': 'hallelujah', 'pronunciation': 'hæləluːjə', 'audio_url': generate_audio_url('hallelujah')}
            ]
        },
        {
            'symbol': 'w',
            'spellings': 'w, wh, u, o',
            'examples': [
                {'word': 'wet', 'pronunciation': 'wet', 'audio_url': generate_audio_url('wet')},
                {'word': 'when', 'pronunciation': 'wen', 'audio_url': generate_audio_url('when')},
                {'word': 'queen', 'pronunciation': 'kwiːn', 'audio_url': generate_audio_url('queen')}
            ]
        }
    ]
    
    # Alphabet combination pronunciations
    alphabet_combinations = [
        {
            'combination': 'ch',
            'sounds': [
                {
                    'sound': '/tʃ/ (as in "chair")',
                    'examples': [
                        {'word': 'chair', 'pronunciation': 'tʃeə', 'audio_url': generate_audio_url('chair')},
                        {'word': 'church', 'pronunciation': 'tʃɜːtʃ', 'audio_url': generate_audio_url('church')}
                    ]
                },
                {
                    'sound': '/k/ (as in "chemistry")',
                    'examples': [
                        {'word': 'chemistry', 'pronunciation': 'kemɪstri', 'audio_url': generate_audio_url('chemistry')},
                        {'word': 'chorus', 'pronunciation': 'kɔːrəs', 'audio_url': generate_audio_url('chorus')}
                    ]
                },
                {
                    'sound': '/ʃ/ (as in "chef")',
                    'examples': [
                        {'word': 'chef', 'pronunciation': 'ʃef', 'audio_url': generate_audio_url('chef')},
                        {'word': 'machine', 'pronunciation': 'məʃiːn', 'audio_url': generate_audio_url('machine')}
                    ]
                }
            ]
        },
        {
            'combination': 'gh',
            'sounds': [
                {
                    'sound': '/g/ (as in "ghost")',
                    'examples': [
                        {'word': 'ghost', 'pronunciation': 'gəʊst', 'audio_url': generate_audio_url('ghost')},
                        {'word': 'ghastly', 'pronunciation': 'gɑːstli', 'audio_url': generate_audio_url('ghastly')}
                    ]
                },
                {
                    'sound': '/f/ (as in "laugh")',
                    'examples': [
                        {'word': 'laugh', 'pronunciation': 'lɑːf', 'audio_url': generate_audio_url('laugh')},
                        {'word': 'enough', 'pronunciation': 'ɪnʌf', 'audio_url': generate_audio_url('enough')}
                    ]
                },
                {
                    'sound': 'silent (as in "though")',
                    'examples': [
                        {'word': 'though', 'pronunciation': 'ðəʊ', 'audio_url': generate_audio_url('though')},
                        {'word': 'night', 'pronunciation': 'naɪt', 'audio_url': generate_audio_url('night')}
                    ]
                }
            ]
        },
        {
            'combination': 'th',
            'sounds': [
                {
                    'sound': '/θ/ (voiceless, as in "thin")',
                    'examples': [
                        {'word': 'thin', 'pronunciation': 'θɪn', 'audio_url': generate_audio_url('thin')},
                        {'word': 'bath', 'pronunciation': 'bɑːθ', 'audio_url': generate_audio_url('bath')}
                    ]
                },
                {
                    'sound': '/ð/ (voiced, as in "this")',
                    'examples': [
                        {'word': 'this', 'pronunciation': 'ðɪs', 'audio_url': generate_audio_url('this')},
                        {'word': 'father', 'pronunciation': 'fɑːðə', 'audio_url': generate_audio_url('father')}
                    ]
                }
            ]
        },
        {
            'combination': 'sh',
            'sounds': [
                {
                    'sound': '/ʃ/ (as in "ship")',
                    'examples': [
                        {'word': 'ship', 'pronunciation': 'ʃɪp', 'audio_url': generate_audio_url('ship')},
                        {'word': 'fish', 'pronunciation': 'fɪʃ', 'audio_url': generate_audio_url('fish')}
                    ]
                }
            ]
        },
        {
            'combination': 'ph',
            'sounds': [
                {
                    'sound': '/f/ (as in "phone")',
                    'examples': [
                        {'word': 'phone', 'pronunciation': 'fəʊn', 'audio_url': generate_audio_url('phone')},
                        {'word': 'graph', 'pronunciation': 'grɑːf', 'audio_url': generate_audio_url('graph')}
                    ]
                }
            ]
        },
        {
            'combination': 'ough',
            'sounds': [
                {
                    'sound': '/əʊ/ (as in "though")',
                    'examples': [
                        {'word': 'though', 'pronunciation': 'ðəʊ', 'audio_url': generate_audio_url('though')},
                        {'word': 'dough', 'pronunciation': 'dəʊ', 'audio_url': generate_audio_url('dough')}
                    ]
                },
                {
                    'sound': '/uː/ (as in "through")',
                    'examples': [
                        {'word': 'through', 'pronunciation': 'θruː', 'audio_url': generate_audio_url('through')}
                    ]
                },
                {
                    'sound': '/ʌf/ (as in "tough")',
                    'examples': [
                        {'word': 'tough', 'pronunciation': 'tʌf', 'audio_url': generate_audio_url('tough')},
                        {'word': 'rough', 'pronunciation': 'rʌf', 'audio_url': generate_audio_url('rough')}
                    ]
                },
                {
                    'sound': '/ɔː/ (as in "thought")',
                    'examples': [
                        {'word': 'thought', 'pronunciation': 'θɔːt', 'audio_url': generate_audio_url('thought')},
                        {'word': 'bought', 'pronunciation': 'bɔːt', 'audio_url': generate_audio_url('bought')}
                    ]
                }
            ]
        }
    ]
    
    return render_template('pronunciation_guide.html', vowels=vowels, diphthongs=diphthongs, consonants=consonants, alphabet_combinations=alphabet_combinations)

@app.route('/search', methods=['POST', 'GET'])
def search():
    # Get the word from either POST form data or GET query parameters
    if request.method == 'POST':
        word = request.form.get('word', '')
    else:
        word = request.args.get('word', '')
    if not word:
        return jsonify({'error': 'No word provided'})
    
    try:
        # Scrape Cambridge Dictionary for the word
        entry = scrape_cambridge_dictionary(word)
        return jsonify(entry)
    except Exception as e:
        return jsonify({'error': str(e)})

def scrape_cambridge_dictionary(word):
    # Format the URL for the Cambridge Dictionary
    url = f'https://dictionary.cambridge.org/dictionary/english/{word.lower().replace(" ", "-")}'
    
    # Set a user agent to avoid being blocked
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Make the request
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code != 200:
        raise Exception(f'Failed to retrieve data: HTTP {response.status_code}')
    
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Initialize the entry dictionary
    entry = {
        'word': word,
        'pronunciation': '',
        'audio_url': '',
        'parts_of_speech': []
    }
    
    # Extract UK pronunciation and audio URL
    uk_pron_div = soup.find('span', class_='uk dpron-i')
    if uk_pron_div:
        ipa_span = uk_pron_div.find('span', class_='ipa')
        if ipa_span:
            entry['pronunciation'] = ipa_span.text
            
        # Extract audio URL
        audio_source = uk_pron_div.find('source', type='audio/mpeg')
        if audio_source and 'src' in audio_source.attrs:
            audio_url = audio_source['src']
            if audio_url.startswith('//'):
                audio_url = 'https:' + audio_url
            elif audio_url.startswith('/'):
                audio_url = 'https://dictionary.cambridge.org' + audio_url
            entry['audio_url'] = audio_url
    
    # Find all parts of speech sections
    pos_sections = soup.find_all('div', class_='pr dictionary')
    
    for pos_section in pos_sections:
        # Find the part of speech
        pos_header = pos_section.find('div', class_='pos-header')
        if not pos_header:
            continue
            
        pos_type = pos_header.find('span', class_='pos')
        if not pos_type:
            continue
            
        pos_entry = {
            'type': pos_type.text,
            'definitions': []
        }
        
        # Find all definition blocks
        def_blocks = pos_section.find_all('div', class_='def-block')
        
        for def_block in def_blocks:
            # Extract definition
            def_div = def_block.find('div', class_='def')
            if not def_div:
                continue
                
            def_text = def_div.text.strip()
            
            # Extract examples
            examples = []
            example_divs = def_block.find_all('div', class_='examp')
            for example_div in example_divs:
                example_text = example_div.text.strip()
                examples.append(example_text)
            
            def_entry = {
                'text': def_text,
                'examples': examples
            }
            
            pos_entry['definitions'].append(def_entry)
        
        if pos_entry['definitions']:
            entry['parts_of_speech'].append(pos_entry)
    
    # If no parts of speech were found, try to find idioms or phrasal verbs
    if not entry['parts_of_speech']:
        idiom_sections = soup.find_all('div', class_='idiom-block')
        for idiom_section in idiom_sections:
            idiom_header = idiom_section.find('div', class_='idiom-title')
            if not idiom_header:
                continue
                
            pos_entry = {
                'type': 'idiom',
                'definitions': []
            }
            
            # Find all definition blocks within the idiom
            def_blocks = idiom_section.find_all('div', class_='def-block')
            
            for def_block in def_blocks:
                # Extract definition
                def_div = def_block.find('div', class_='def')
                if not def_div:
                    continue
                    
                def_text = def_div.text.strip()
                
                # Extract examples
                examples = []
                example_divs = def_block.find_all('div', class_='examp')
                for example_div in example_divs:
                    example_text = example_div.text.strip()
                    examples.append(example_text)
                
                def_entry = {
                    'text': def_text,
                    'examples': examples
                }
                
                pos_entry['definitions'].append(def_entry)
            
            if pos_entry['definitions']:
                entry['parts_of_speech'].append(pos_entry)
    
    # If still no definitions found, try to find a different format
    if not entry['parts_of_speech']:
        entry_bodies = soup.find_all('div', class_='entry-body')
        for entry_body in entry_bodies:
            pos_headers = entry_body.find_all('div', class_='pos-header')
            for pos_header in pos_headers:
                pos_type_span = pos_header.find('span', class_='pos')
                if not pos_type_span:
                    continue
                    
                pos_type = pos_type_span.text
                
                pos_entry = {
                    'type': pos_type,
                    'definitions': []
                }
                
                # Find the corresponding entry body block
                entry_body_block = pos_header.find_next('div', class_='pos-body')
                if not entry_body_block:
                    continue
                    
                # Find all sense blocks
                sense_blocks = entry_body_block.find_all('div', class_='sense-block')
                
                for sense_block in sense_blocks:
                    # Extract definition
                    def_div = sense_block.find('div', class_='def')
                    if not def_div:
                        continue
                        
                    def_text = def_div.text.strip()
                    
                    # Extract examples
                    examples = []
                    example_divs = sense_block.find_all('div', class_='examp')
                    for example_div in example_divs:
                        example_text = example_div.text.strip()
                        examples.append(example_text)
                    
                    def_entry = {
                        'text': def_text,
                        'examples': examples
                    }
                    
                    pos_entry['definitions'].append(def_entry)
                
                if pos_entry['definitions']:
                    entry['parts_of_speech'].append(pos_entry)
    
    # If no definitions were found, raise an exception
    if not entry['parts_of_speech']:
        raise Exception('No definitions found for this word')
    
    return entry

if __name__ == '__main__':
    app.run(debug=True)