import streamlit as st
import requests
import random
import re

st.set_page_config(page_title="Pure Streamlit MCQ & Singer App", layout="centered")

# --- 1. SINGER THEME BACKGROUND ---
singer = st.text_input("Enter Singer Name for Theme:", value="Taylor Swift")

if singer:
    url = f"https://itunes.apple.com/search?term={singer}&entity=song&limit=3"
    try:
        res = requests.get(url).json()
        if res.get("results"):
            img = res["results"][0]["artworkUrl100"].replace("100x100bb", "600x600bb")
            
            st.markdown(
                f"""
                <style>
                .stApp {{
                    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                    color: white;
                }}
                /* Fix text visibility in Streamlit inputs */
                .stTextArea textarea {{
                    color: #000000 !important;
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
    except Exception:
        pass

st.write("---")

# --- 2. PURE PYTHON MCQ GENERATOR (NO API NEEDED) ---
st.title("📝 Text-Based MCQ Generator")

topic_info = st.text_area(
    "Paste topic information/notes here:", 
    height=180, 
    placeholder="Paste your study notes here..."
)

if st.button("Generate MCQs from Text"):
    if not topic_info.strip():
        st.warning("Please paste some text in the box above first!")
    else:
        # Split text into individual sentences
        sentences = [s.strip() for s in re.split(r'[.!?]\s+', topic_info) if len(s.strip().split()) > 4]
        
        # Collect all significant words from text to use as options
        all_words = list(set(re.findall(r'\b[A-Za-z]{4,}\b', topic_info)))
        
        if len(sentences) == 0:
            st.error("Please enter a longer text with full sentences.")
        else:
            st.success("🎯 Questions Created directly from your notes:")
            
            # Loop up to 10 questions (or as many sentences as available)
            num_q = min(10, len(sentences))
            for i in range(num_q):
                sentence = sentences[i]
                words_in_sentence = [w for w in re.findall(r'\b[A-Za-z]{4,}\b', sentence) if w.lower() not in ['this', 'that', 'with', 'from', 'have', 'been', 'which', 'they', 'your', 'more']]
                
                if words_in_sentence:
                    target_word = words_in_sentence[0] # Pick a key word to test
                    question_text = sentence.replace(target_word, "_______")
                    
                    # Create choices containing the correct word + random distractor words
                    wrong_choices = [w for w in all_words if w.lower() != target_word.lower()]
                    random.shuffle(wrong_choices)
                    choices = wrong_choices[:3] + [target_word]
                    random.shuffle(choices) # Shuffle order of options
                    
                    st.markdown(f"**Q{i+1}: Fill in the blank based on your notes:**")
                    st.write(f"*{question_text}*")
                    
                    user_ans = st.radio(
                        f"Select answer for Q{i+1}:", 
                        [f"A) {choices[0]}", f"B) {choices[1]}", f"C) {choices[2]}", f"D) {choices[3]}"], 
                        key=f"pure_mcq_{i}"
                    )
                    st.write("---")
