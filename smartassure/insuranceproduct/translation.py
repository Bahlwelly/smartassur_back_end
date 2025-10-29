import requests

LIBRE_URL = 'http://localhost:5000'

def translate_text (text, target_lang, source_lang = 'en') :
    payload = {
        "q": text,
        "source": source_lang,
        "target": target_lang,
        "format": "text"
    }

    if source_lang : 
        payload['source'] = source_lang

    try :
        response = requests.post(f"{LIBRE_URL}/translate", json=payload, timeout=15)
        response.raise_for_status()
        return response.json().get('translatedText')
    except Exception as e :
        print('Translation Error : ', e)
        return None