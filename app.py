import streamlit as st
import snscrape.modules.twitter as sntwitter

def get_tweets(username, max_tweets=20):
    tweets = []
    for i, tweet in enumerate(sntwitter.TwitterUserScraper(username).get_items()):
        if i >= max_tweets:
            break
        tweets.append(tweet.content)
    return tweets

# Streamlit UI
st.title("Twitter Scanner with snscrape")
st.write("Entrez un nom d'utilisateur Twitter pour scanner ses tweets publics.")

username = st.text_input("Nom d'utilisateur (sans @)", value="elonmusk")

if st.button("Scanner"):
    if username:
        with st.spinner("Récupération des tweets..."):
            try:
                tweets = get_tweets(username)
                if tweets:
                    st.success(f"{len(tweets)} tweets trouvés !")
                    for tweet in tweets:
                        st.write(f"🔹 {tweet}")
                else:
                    st.warning("Aucun tweet trouvé pour cet utilisateur.")
            except Exception as e:
                st.error(f"Erreur lors du scan : {e}")
    else:
        st.warning("Veuillez entrer un nom d'utilisateur.")