import urllib.request
import requests
from bs4 import BeautifulSoup

nb_page = 100

def download_file(download_url, filename):
    response = urllib.request.urlopen(download_url)
    file = open(filename + ".pdf", 'wb')
    file.write(response.read())
    file.close()
    
for n_page in range(1, nb_pages):
    url_i = 'https://core.ac.uk/search.....'
    url = url_i + str(n_page)
    print('HTTP GET: %53', url)
    response = requests.get(url)
    # parse content
    content = BeautifulSoup(response.text, 'html')
    # extract URLs referencing PDF documents
    all_urls = content.find_all('a', href=True)#('figure')
    # loop over all URLs
    for url in all_urls:
        try:
            if 'pdf' in url['href']:
                # init PDF url
                pdf_url = ''
    
          