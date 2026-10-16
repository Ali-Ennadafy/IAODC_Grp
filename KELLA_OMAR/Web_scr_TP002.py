import urllib.request
import requests
from bs4 import BeautifulSoup
import os

# 1. Création du dossier IAODC s'il n'existe pas
output_folder = "IAODC"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    print(f"Dossier créé : {output_folder}")

nb_pages = 10

# En-têtes HTTP pour simuler un vrai navigateur et éviter d'être bloqué
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def download_file(download_url, filename):
    try:
        # Chemin complet pour stocker le fichier dans le dossier IAODC
        filepath = os.path.join(output_folder, filename + ".pdf")
        
        # Téléchargement via requests avec les en-têtes
        response = requests.get(download_url, headers=headers, timeout=15)
        
        if response.status_code == 200 and len(response.content) > 0:
            with open(filepath, 'wb') as file:
                file.write(response.content)
            print(f"  [+] Téléchargé avec succès : {filepath}")
        else:
            print(f"  [-] Échec du téléchargement (Code HTTP {response.status_code})")
    except Exception as e:
        print(f"  [-] Erreur de téléchargement : {e}")

# Boucle principale
for n_page in range(1, nb_pages):
    # Requête ciblée sur le Machine Learning
    url_i = 'https://core.ac.uk/search?q="machine+learning"&page='
    url = url_i + str(n_page)
    print(f"\n--- Navigation Page {n_page} : {url} ---")
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        # Parse content (utilise html.parser nativement)
        content = BeautifulSoup(response.text, 'html.parser')
        
        # extract URLs referencing PDF documents
        all_urls = content.find_all('a', href=True)
        
        # loop over all URLs
        for idx, url_item in enumerate(all_urls):
            try:
                href = url_item['href']
                if 'pdf' in href.lower():
                    # init PDF url
                    pdf_url = ''
                    
                    # append base URL if no 'https' available in URL
                    if 'https' not in href:
                        pdf_url = 'https://core.ac.uk/' + href.lstrip('/')
                    else:
                        pdf_url = href
                    
                    print(f"HTTP GET PDF: {pdf_url}")
                    url_path = pdf_url
                    
                    # extract PDF file name
                    unquoted_url = urllib.request.unquote(pdf_url)
                    base_name = os.path.basename(unquoted_url).split('?')[0].replace('.pdf', '')
                    
                    # Si aucun nom valide n'est trouvé dans l'URL
                    if not base_name or len(base_name) < 3:
                        filename = f"ml_paper_p{n_page}_{idx}"
                    else:
                        filename = base_name
                    
                    # Téléchargement vers le dossier IAODC
                    download_file(url_path, filename)
            except Exception as e:
                print(f"  [-] Erreur lors du traitement du lien : {e}")
                pass
    except Exception as e:
        print(f"[-] Erreur d'accès à la page {n_page} : {e}")
        pass