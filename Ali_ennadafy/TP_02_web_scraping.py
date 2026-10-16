import urllib.request
import requests
from bs4 import BeautifulSoup

nb_pages = 1000

def download_file(download_url, filename):

    response = urllib.request.urlopen(download_url)
    file = open(filename + " .pdf", 'wb')
    file.write(response.read())
    file.close()

for n_page in range(1, nb_pages):
    url_i = "https://demo.nopcommerce.com/search?q=computer&page="
    url = url_i + str(n_page)
    print( 'HTTP GET : %s', url)
    response = requests.get(url)
    # parse content
    content = BeautifulSoup(response.text , 'lxml')
    # extract URLs referencing PDF doucuments
    all_urls = content.find_all('a', href=True) #('figure')
    #loop over all URLs

    for url in all_urls:
        try:
            if 'pdf' in url['href']:
                #init PDF url
                    pdf_url = ""

    #append the base url if the pdf url is relative
                    if 'http' not  in url['href']:
                        pdf_url = 'https://demo.nopcommerce.com' + url['href']
                    else:
                        pdf_url = "https://demo.nopcommerce.com" + url['href']

                    #make HTTP GET request to fetch the PDF bytes

                    print("HTTP GET : %s", pdf_url)
                    #extract the filename
                    pdf_filename = pdf_url.
                    download_file(pdf_url, pdf_url.split('/')[-1])
