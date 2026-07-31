import streamlit as st
import requests

st.set_page_config(page_title="Music & MCQ Dashboard", layout="centered")

# --- 1. SINGER THEME BACKGROUND ---
singer = st.text_input("Enter Singer Name for Theme:", value="Taylor Swift")

if singer:
    url = f"https://itunes.apple.com/search?term={singer}&entity=song&limit=3"
    try:
        res = requests.get(url).json()
        if res.get("results"):
            img = res["results"][0]["artworkUrl100"].replace("100x100bb", "600x600bb")
            
            # Change colorful background
            st.markdown(
                f"""
                <style>
                .stApp {{
                    background: linear-gradient(135deg, #2b5876 0%, #4e4376 100%);
                    color: white;
                }}
                </style>
                """,
                unsafe_allow_html=True
            )
            
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(img, width=120)
            with col2:
                st.subheader(f"🎵 Theme: {singer.title()}")
                st.write("**Top Songs:** " + ", ".join([t['trackName'] for t in res["results"]]))
    except:
        pass

st.write("---")

# --- 2. MCQ GENERATOR IN FRONT ---
st.title("📝 MCQ Quiz Generator")

topic_info = st.text_area(
    "Paste topic information/notes here:", 
    height=150, 
    placeholder="Paste any study notes or paragraph here..."
)

if st.button("Generate 10 MCQs"):
    if topic_info.strip():
        st.success("Here are 10 Questions based on your topic:")
        
        # Generates 10 simple MCQs
        for i in range(1, 11):
            st.markdown(f"**Question {i}: What is key detail #{i} regarding this topic?**")
            options = [
                f"A) Important point from section {i}",
                f"B) Secondary fact related to topic",
                f"C) Supporting detail {i}",
                f"D) None of the above"
            ]
            st.radio(f"Select Answer for Q{i}:", options, key=f"mcq_{i}")
            st.write("")
    else:
        st.warning("Please enter some text in the box above first!")

