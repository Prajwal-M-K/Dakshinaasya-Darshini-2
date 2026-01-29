import streamlit as st
from logic import (
    get_lifestyle_recommendations, 
    parse_recommendations, 
    generate_all_images_fast
)

# --------------------------------------------------
# 1. Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Dakshinaasya Darshini",
    layout="wide"
)

# --------------------------------------------------
# 2. Custom Styling (Extended with Soul Analysis Box)
# --------------------------------------------------
MIRROR_FRAME_URL = "https://images.unsplash.com/photo-1594901691854-f7b30c100778?q=80&w=2000&auto=format&fit=crop"

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("{MIRROR_FRAME_URL}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    .stApp > div:first-child {{
        background: rgba(255, 255, 255, 0.75); 
        backdrop-filter: blur(10px);
        padding: 50px;
        border-radius: 20px;
        margin: 20px;
    }}

    .section-title {{
        font-family: 'Playfair Display', serif;
        font-size: 3rem;
        color: #2c1810; 
        text-align: center;
    }}
    
    .sub-label {{
        color: #5d4037;
        text-transform: uppercase;
        letter-spacing: 0.2em;
        font-size: 0.8rem;
        text-align: center;
        margin-bottom: 2rem;
    }}

    /* SOUL ANALYSIS BOX STYLING */
    .insight-container {{
        background: rgba(212, 175, 55, 0.08);
        border-left: 4px solid #d4af37;
        padding: 25px;
        margin: 30px auto;
        max-width: 850px;
        border-radius: 0 15px 15px 0;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.05);
        animation: fadeInEffect 2s ease-out;
    }}

    .insight-header {{
        font-family: 'Playfair Display', serif;
        font-size: 0.9rem;
        color: #d4af37;
        letter-spacing: 0.3em;
        margin-bottom: 10px;
        font-weight: bold;
    }}

    .insight-body {{
        font-family: 'Playfair Display', serif;
        font-style: italic;
        font-size: 1.4rem;
        color: #3e2723;
        line-height: 1.6;
    }}

    /* LOADER STYLING */
    .loader-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 40px;
    }}

    .mandala-sun {{
        width: 60px;
        height: 60px;
        border: 3px double #d4af37;
        border-radius: 50%;
        border-top: 3px solid #3e2723;
        animation: spin 3s linear infinite;
        position: relative;
    }}

    @keyframes spin {{ 100% {{ transform: rotate(360deg); }} }}

    @keyframes fadeInEffect {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    .stTextInput input {{
        background-color: rgba(255,255,255,0.5) !important;
        border-bottom: 2px solid #8d6e63 !important;
    }}

    .stButton > button {{
        background-color: #3e2723;
        color: #d7ccc8;
        border: 1px solid #d4af37; 
        width: 100%;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# 3. Header Section
# --------------------------------------------------
st.markdown("<h1 class='section-title'>The MIND - An Ancient Mirror</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-label'>Reflecting the soul's deep impressions</p>", unsafe_allow_html=True)

# --------------------------------------------------
# 4. User Input
# --------------------------------------------------
user_input = st.text_input(
    label="Whisper your preferences to the glass",
    placeholder="e.g. Sandalwood, Temple bells, Rain on stone"
)

# --------------------------------------------------
# 5. Logic
# --------------------------------------------------
if st.button("Invoke Reflection"):
    if user_input:
        interests = [i.strip() for i in user_input.split(",")]

        # --- A. SHOW THE ANCIENT PROPHECY VERSE ---
        st.markdown(
            """
            <div style="font-family: 'Playfair Display', serif; font-style: italic; font-size: 1.1rem; color: #3e2723; text-align: center; opacity: 0.8;">
               विश्वं दर्पणदृश्यमाननगरीतुल्यं निजान्तर्गतं पश्यन्नात्मनि मायया बहिरिवोद्भूतं यथा निद्रया ।<br>
               यः साक्षात्कुरुते प्रबोधसमये स्वात्मानमेवाद्वयं तस्मै श्रीगुरुमूर्तये नम इदं श्रीदक्षिणामूर्तये ॥१॥<br><br>
                <i>The universe is a projection of appearances within the mind </i>
                <br>The mind is the mirror of consciousness </i><br>

            </div>
            <hr style="width: 20%; margin: 20px auto; border-color: #d4af37;">
            """, 
            unsafe_allow_html=True
        )

        # --- B. FETCH TEXT ANALYSIS FIRST (FAST) ---
        with st.spinner("The mirror is observing your essence..."):
            # logic.py now returns 3 values: analysis, titles, justifications
            analysis, titles = parse_recommendations(get_lifestyle_recommendations(interests))

        # --- C. DISPLAY "THE MIRROR'S INSIGHT" IMMEDIATELY ---
        st.markdown(
            f"""
            <div class="insight-container">
                <div class="insight-header">THE MIRROR'S INSIGHT</div>
                <div class="insight-body">"{analysis}"</div>
            </div>
            """, 
            unsafe_allow_html=True
        )

        # --- D. START IMAGE GENERATION IN BACKGROUND ---
        # While the user is reading the beautiful insight above, we trigger the images.
        loader_placeholder = st.empty()
        loader_placeholder.markdown(
            """
            <div class="loader-container">
                <div class="mandala-sun"></div>
                <div style="margin-top: 15px; font-family: 'Playfair Display'; font-style: italic; color: #5d4037;">
                    Manifesting your visions from the deep impressions...
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Fetch images
        rec_imgs, dream_imgs = generate_all_images_fast(titles, interests)

        # Clear the loader
        loader_placeholder.empty()

        # --- E. DISPLAY WAKING VISIONS ---
        st.markdown("<br><p class='sub-label'>Waking Visions</p>", unsafe_allow_html=True)
        cols = st.columns(len(titles))
        for i in range(len(titles)):
            with cols[i]:
                if i < len(rec_imgs) and rec_imgs[i]: 
                    st.image(rec_imgs[i], use_column_width=True)
                st.markdown(f"**{titles[i]}**")


        # --- F. DISPLAY DREAM ECHOES ---
        st.markdown("<br><p class='sub-label'>Dream Echoes</p>", unsafe_allow_html=True)
        d_cols = st.columns(len(dream_imgs))
        for i in range(len(dream_imgs)):
            with d_cols[i]:
                if dream_imgs[i]: 
                    st.image(dream_imgs[i], use_column_width=True)
                st.caption(f"Dream Vision {i+1}")
                
    else:
        st.warning("The glass remains dark. Speak your mind.")