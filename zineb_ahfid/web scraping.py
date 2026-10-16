import urllib.request
import request
from bs4 import beautifulSoup
nb_pages = 1000
def download_file(download_url,filename):
    response = urllib.request.urlopen(download_url)
    file = open(filename+".pdf","wb")
    file.write(response.read())
    file.close()

for nb_pages in range (1,nb_pages):
    url_i = "https://www.hackster.io/  "
    url_i = url_i + str(n_page)
    print ('HTTP GET':)