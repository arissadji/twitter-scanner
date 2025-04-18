import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os

# Configuration du chemin vers ton ChromeDriver (ajuste si besoin)
CHROMEDRIVER_PATH = "C:/Users/Administrateur/Documents/chromedriver-win64/chromedriver.exe"

# Fonction pour récupérer les tweets via Selenium
def get_tweets(username, password):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get("https://twitter.com/login")
        time.sleep(3)

        # Entrer username
        user_input = driver.find_element(By.NAME, "text")
        user_input.send_keys(username)
        user_input.submit()
        time.sleep(3)

        # Entrer password
        password_input = driver.find_element(By.NAME, "password")
        password_input.send_keys(password)
        password_input.submit()
        time.sleep(5)

        # Aller sur le profil
        driver.get(f"https://twitter.com/{username}")
        time.sleep(5)

        # Récupérer les tweets
        tweets_elements = driver.find_elements(By.XPATH, '//div[@data-testid="tweetText"]')
        tweets = [tweet.text for tweet in tweets_elements[:10]]

        driver.quit()
        return tweets
    except Exception as e:
        driver.quit()
        return [f"Erreur : {str(e)}"]

# Interface Streamlit
st.title("🕵️‍♂️ Twitter Account Scanner")
st.markdown("Entrez vos identifiants pour scanner les derniers tweets.")

username = st.text_input("Nom d'utilisateur Twitter")
password = st.text_input("Mot de passe", type="password")

if st.button("Scanner les tweets"):
    if username and password:
        st.write("🔍 Scan en cours, veuillez patienter...")
        tweets = get_tweets(username, password)
        st.write("### Résultats du scan :")
        for tweet in tweets:
            st.write(f"- {tweet}")
    else:
        st.warning("Veuillez entrer un nom d'utilisateur **et** un mot de passe.")