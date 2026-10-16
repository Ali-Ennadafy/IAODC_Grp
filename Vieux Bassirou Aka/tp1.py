dataset = [
    "Bonjour, mon email est   omar.k@example.com   et mon tel est 0612345678.",
    "Contactez-nous via www.monsite.ma ou https://monsite.ma/contact !!",
    "Le prix est 250 MAD le 17/09/2026, livraison rapide #NLP #IA @client_service",
    "<p>Merci pour votre commande</p>   <br> Numero: +212 6-61-22-33-44",
    "  Service   nul...    remboursement demande  le 05-08-2026  , prix 1200,50 MAD ",
    "Great service! Contact: sales@company.com or call 0522-334455 #satisfied",
    "Facture N° INV-2026-00457 total: 3999.99 MAD TVA 20% date: 2026/09/01",
    "Aucun probleme, tout est parfait :) suivez-nous @companyOfficial https://x.com/companyOfficial"
]


import re
email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'

phone_pattern = r'(\+212|0|00212)?[6-9]\d{8}\b'

url_pattern = r'(https?://|www\.)[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'

date_pattern = r'\b\d{2}/\d{2}/\d{4}\b'

price_pattern = r'\b\d+(?:[.,]\d+)?\s*MAD\b'            

hashtag_pattern = r'#\w+\b'

multi_space_pattern = r'\s{2,}'

def clean_text(text):
    text = re.sub(email_pattern, '', text)
    text = re.sub(phone_pattern, '', text)
    text = re.sub(url_pattern, '', text)
    text = re.sub(date_pattern, '', text)
    text = re.sub(price_pattern, '', text)
    text = re.sub(hashtag_pattern, '', text)
    text = re.sub(multi_space_pattern, ' ', text)
    return text.strip()
for text in dataset:
    cleaned_text = clean_text(text)
    print(cleaned_text)

def extract_information(text):
    emails = re.findall(email_pattern, text)
    phones = re.findall(phone_pattern, text)
    urls = re.findall(url_pattern, text)
    dates = re.findall(date_pattern, text)
    prices = re.findall(price_pattern, text)
    hashtags = re.findall(hashtag_pattern, text)

    return {
        "emails": emails,
        "phones": phones,
        "urls": urls,
        "dates": dates,
        "prices": prices,
        "hashtags": hashtags
    }
print("\nExtracted Information:")
for text in dataset:
    info = extract_information(text)
    print(info)

import pandas as pd
data = pd.DataFrame([extract_information(text) for text in dataset])
data.insert(0, 'original_text', dataset)
print(data.to_string())
entities=extract_information(text)
lignes=[
    'origine_text':text,
    'emails': entities['emails'],
    'phones': entities['phones'],
    'urls': entities['urls'],
    'dates': entities['dates'],
    'prices': entities['prices'],
    'mentions': entities['mentions'],
    'hashtags': entities['hashtags']

]
