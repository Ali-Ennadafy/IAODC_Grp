from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests
import pandas as pd
import os


options = Options()

options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")


driver = webdriver.Chrome(options=options)


try:

    driver.get("https://unsplash.com/s/photos/computer")

    print("Site ouvert :", driver.current_url)


    WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located(
            (By.TAG_NAME, "img") ))


    images = driver.find_elements(By.TAG_NAME,"img")


    urls = []

    for image in images:

        src = image.get_attribute("src")

        if src and "images.unsplash.com" in src:

            if src not in urls:

                urls.append(src)

        if len(urls) == 10:
            break


    print("\nNombre d'images trouvées :", len(urls))

    for i, url in enumerate(urls, start=1):

        print(i, ":", url)


    os.makedirs("images",exist_ok=True)


    for i, url in enumerate(urls, start=1):

        try:

            response = requests.get(url,timeout=60)

            if response.status_code == 200:

                nom_fichier = f"images/image_{i}.jpg"

                with open(nom_fichier,"wb") as fichier:

                    fichier.write(
                        response.content)

                print("Téléchargée :",nom_fichier)

            else:

                print("Erreur HTTP :",response.status_code )

        except Exception as e:

            print("Erreur téléchargement :",e )


    df = pd.DataFrame({"URL": urls})

    df.to_csv("images.csv",index=False)

    print("\nFichier images.csv créé !")


finally:

    driver.quit()


print("\nSCRAPING TERMINÉ !")
