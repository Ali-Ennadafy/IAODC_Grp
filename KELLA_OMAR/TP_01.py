import re
import pandas as pd
dataset = [
    "Bonjour, mon email est   omar.k9999@example.com   et mon tel est 0612345678.",
    "Contactez-nous via www.monsite.ma ou https://monsite.ma/contact !!",
    "Le prix est 250 MAD le 17/09/2026, livraison rapide #IA @client_service",
    "<p>Merci pour votre commande</p>   <br> Numero: +212 6-61-22-33-44",
    "  Service   nul...    remboursement demande le 05-08-2026  , prix 1200,50 MAD ",
    "Great service! Contact: sales@company.com or call 0522-334455 #satisfied",
    "Facture N° INV-2026-00457 total: 3999.99 MAD TVA 20% date: 2026/09/01",
    "Aucun probleme, tout est parfait :) suivez-nous @companyOfficial https://x.com/companyOfficial"
]

 # email : partie_local @ domaine . extension   

email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

 #tele : indicateur c'est +212 ou 0 suivi de 9 chiffres Numero: +212 6-61-22-33-44
phone_pattern = r'(?:\+212|0)[\s\-]?[5-7](?:[\s\-]?\d){8}'

# date JJ/MM/AAAA ou AAAA/MM/JJ ou JJ-MM-AAAA ou AAAA-MM-JJ
date_pattern = r'\b(?:\d{2}/\d{2}/\d{4}|\d{4}/\d{2}/\d{2}|\d{2}-\d{2}-\d{4}|\d{4}-\d{2}-\d{2})\b'

#prix
prix_pattern = r'\b\d+(?:[.,]\d+)?\s*(?:MAD|EUR|USD)\b'

#hastags et mentions
hashtag_pattern = r'#\w+'
mention_pattern = r'@\w+'

#balises html
html_pattern = r'<[^>]+>'

#url wite ou wwww 
url_pattern = r'\b(?:https?://|www\.)[^\s]+\b'

# espaces multiples
multiple_spaces_pattern = r'\s{2,}'

def clean_text(text):
    text = re.sub(email_pattern, '[EMAIL]', text)
    text = re.sub(phone_pattern, '[PHONE]', text)
    text = re.sub(date_pattern, '[DATE]', text)
    text = re.sub(prix_pattern, '[PRICE]', text)
    text = re.sub(hashtag_pattern, '', text)
    text = re.sub(mention_pattern, '', text)
    text = re.sub(html_pattern, '[HTML]', text)
    text = re.sub(url_pattern, '[URL]', text)
    text = re.sub(multiple_spaces_pattern, ' ', text)
    return text.strip()
for text in dataset:
    cleaned_text = clean_text(text)
    print(cleaned_text)

def extract_entities(text):
    emails = re.findall(email_pattern, text)
    phones = re.findall(phone_pattern, text)
    dates = re.findall(date_pattern, text)
    prices = re.findall(prix_pattern, text)
    hashtags = re.findall(hashtag_pattern, text)
    mentions = re.findall(mention_pattern, text)
    urls = re.findall(url_pattern, text)
    
    return {
        'emails': emails,
        'phones': phones,
        'dates': dates,
        'prices': prices,
        'hashtags': hashtags,
        'mentions': mentions,
        'urls': urls
    }
#"creat a dataframe to store the extracted entities"

df = pd.DataFrame(columns=['original_text', 'emails', 'phones', 'dates', 'prices', 'hashtags', 'mentions', 'urls'])
lignes = []
for text in dataset:
    entities = extract_entities(text)
    ligne = {
        'original_text': text,
        'emails': entities['emails'],
        'phones': entities['phones'],
        'dates': entities['dates'],
        'prices': entities['prices'],
        'hashtags': entities['hashtags'],
        'mentions': entities['mentions'],
        'urls': entities['urls']
    }
    lignes.append(ligne)
df = pd.DataFrame(lignes)
print(df.to_string())
#data= pd.DataFrame([extract_entities(text) for text in dataset])
# data.insert(0, 'original_text', dataset)
# print(data.to_string())
