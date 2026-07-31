import streamlit as st
import requests

# 1. Title of the App
st.title("🎵 Dynamic Singer Dashboard")

# 2. Get Singer Name from User
singer = st.text_input("Enter a Singer's Name:", value="Taylor Swift")

if singer:
    # Fetch singer data and picture from iTunes API
    url = f"https://itunes.apple.com/search?term={singer}&entity=song&limit=5"
    response = requests.get(url).json()

    if response.get("results"):
        # Get the album/artist image from the first result
        first_track = response["results"][0]
        image_url = first_track["artworkUrl100"].replace("100x100bb", "600x600bb")

        # Set a colorful background using custom CSS & display the image
        st.markdown(
            f"""
            <style>
            .stApp {{
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #7928ca 100%);
                color: white;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

        st.subheader(f"Dashboard for: {singer.title()}")
        st.image(image_url, caption=f"Artist Spotlight: {singer.title()}", width=300)

        # Display Top Songs
        st.write("### 🎶 Popular Songs:")
        for track in response["results"]:
            st.write(f"- **{track['trackName']}** *(Album: {track['collectionName']})*")
    else:
        st.error("Singer not found! Try another name.")
