import os
import urllib.parse
import requests
from bs4 import BeautifulSoup


nb_pages = 10

base_url = "https://core.ac.uk/works/6946354/?t=460298cb3a0368a490b123425c0077e6-6946354&search=q="

# Folder for downloaded PDFs
os.makedirs("pdfs", exist_ok=True)


def download_file(pdf_url, filename):
    try:
        response = requests.get(pdf_url, timeout=60)
        response.raise_for_status()

        filepath = os.path.join("pdfs", filename)

        with open(filepath, "wb") as file:
            file.write(response.content)

        print(f"Downloaded: {filepath}")

    except requests.RequestException as e:
        print(f"Download error: {e}")


for n_page in range(1, nb_pages + 1):

    # Build page URL
    url = f"{base_url}?page={n_page}"

    print(f"\nHTTP GET: {url}")

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

    except requests.RequestException as e:
        print(f"Page error: {e}")
        continue

    # Parse HTML
    soup = BeautifulSoup(response.text, "lxml")

    # Find all links
    links = soup.find_all("a", href=True)

    print(f"Found {len(links)} links")

    for link in links:

        href = link["href"]

        # Look for PDF links
        if ".pdf" not in href.lower():
            continue

        # Convert relative URL → absolute URL
        pdf_url = urllib.parse.urljoin(url, href)

        print(f"PDF found: {pdf_url}")

        # Get filename
        parsed_url = urllib.parse.urlparse(pdf_url)
        filename = os.path.basename(parsed_url.path)

        if not filename:
            filename = f"document_{n_page}.pdf"

        if not filename.lower().endswith(".pdf"):
            filename += ".pdf"

        download_file(pdf_url, filename)
=======
nb_pages = 10

def downoald_file(downoald_url, filename):
    response = urllib.request.urlopen(downoald_url)
    file = open(filename + ".pdf", 'wb')
    file.write(response.read())
    file.close()

for n_page in range(1, nb_pages):
    url_i = 'https://core.ac.uk/search......'
    url = url_i = str(n_page)
    print('HTTP GET: %s', url)
    response = requests.get(url)
    # parse content
    content = BeautifulSoup(response.text, 'lxml')
    # extract URLs referencing PDF documents
    all_urls = content.find_all('a', href=True)#('figure)
    # loop over al URLs
    for url in all_urls:
        try:
            if 'pdf' in url['href']:
                #init PDF url
                pdf_url = ''
                #append base URL if no 'https' available in URL
                if 'https' not in url['href']:
                    pdf_url = 'https://core.ac.uk/' + url['href']
                else:
                    pdf_url = url['href']
                # make HTTP GET request to fetch PDF bytes
                    print('HTTP GET:%s', pdf_url)
                    url_patch = pdf_url
                    pdf_response = requests.get(pdf_url)
                # extract PDF file name
                    filename = urllib.request.unquote(pdf_response.url)
                    downoald_file(url_path, filename)
        except:
            pasS
