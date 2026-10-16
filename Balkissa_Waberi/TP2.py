import urllib.request
import requests
from bs4 import BeautifulSoup

nb_pages = 10

def download_file(download_url, filename):
    response = urllib.request.urlopen(download_url)
    file = open(filename + ".pdf", "wb")
    file.write(response.read())
    file.close()

for n_page in range(1, nb_pages):
    url_i = 'https://core.ac.uk/search/?q=EARNING&page=' 
    url_page = url_i + str(n_page)
    print('HTTP GET: %S', url_page)
    response = requests.get(url_page)
    # parse content
    content = BeautifulSoup(response.text, 'lxml')
    # extract urls referencing PDF documents
    all_urls = content.find_all('a', href=True)
    # loop over all urls
for url in all_urls:
    try:
            if 'pdf' in url['href']:
                #init pdf url
                pdf_url=''

                #append base url if no 'https' avaliable in url
                if 'https' not in url ['href']:
                    pdf_url = 'https://core.ac.uk/' + url ['href']
                else:
                    pdf_url = url ['href']
                
                # male HTTP GET request to fetch pdf bytes
                print('HTTP GET: %s', pdf_url)
                url_path = pdf_url
                pdf_response = requests.get(pdf_url)
                
                # extract pdf file name
                filename = urllib.request.unquote(pdf_response.url)
                download_file(url_path, filename)

    except Exception:
         pass