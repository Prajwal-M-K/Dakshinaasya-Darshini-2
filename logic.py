from google import genai
from google.genai import types
import base64
import re # For parsing the output
import random
import concurrent.futures
import streamlit as st


# 1. Initialize the client using Streamlit secrets
client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
client_img = genai.Client(api_key=st.secrets["GOOGLE_API_KEY_IMG"])

def get_lifestyle_recommendations(interests):
    interest_str = ", ".join(interests)
    
    # Updated Prompt with the "Mirror's Insight" Instruction
    prompt = f"""
    The user is in Bengaluru and likes: {interest_str}.
    Act as a world-class Psychographic Analyst. 

    TASK:
    1. '### THE MIRROR'S INSIGHT': Write a 2-sentence poetic analysis of the user's aura.
    2. '### THE RECOMMENDATIONS': List 3 NEW things they would like as bold titles only.

    Format:
    ### THE MIRROR'S INSIGHT
    [Analysis]

    ### THE RECOMMENDATIONS
    1. **Title 1**
    2. **Title 2**
    3. **Title 3**
    """

    print("🔍 Seeking the mirror's insight...")
    
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    return response.text


def parse_recommendations(text):
    # 1. Extract the Analysis section
    analysis_match = re.search(r"### THE MIRROR'S INSIGHT\n(.*?)\n\n###", text, re.DOTALL)
    analysis = analysis_match.group(1).strip() if analysis_match else "The glass reflects a unique essence."

    # 2. Extract Titles only (everything inside **)
    titles = re.findall(r'\*\*(.*?)\*\*', text)
    
    # If the AI accidentally bolds the header, remove it from the list
    titles = [t for t in titles if "RECOMMENDATIONS" not in t and "INSIGHT" not in t]

    return analysis, titles



# List of surreal objects to swap in
SURREAL_OBJECTS = [
    "melting clocks", "floating lavender clouds", "a staircase leading into the moon", 
    "liquid marble statues", "translucent jellyfish in a desert", "crystal butterflies","Krishna",
    "neon geometric rain", "a glowing golden portal", "shattered mirror mountains","meditating god","lamp","blue moon"
]


# ... (keep your existing imports and clients)

def generate_single_image(prompt):
    """Helper to fetch a single image for parallel execution"""
    try:
        response = client_img.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"]
            )
        )
        for part in response.candidates[0].content.parts:
            if part.inline_data:
                return part.inline_data.data
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def generate_all_images_fast(rec_titles, interests):
    """Generates all 10 images (Recs + Dreams) simultaneously"""
    
    # Create all prompts first
    prompts = []
    
    # 5 Recommendation Prompts (Simplified for speed)
    for title in rec_titles:
        prompts.append(f"Clean minimalistic style photo of {title}, in an Indian setting with soft lighting.")
    
    # 5 Dream Prompts
    base_interests = interests[:3]
    for i in range(3):
        num_original = 3 - i
        combined = base_interests[:num_original] + random.sample(SURREAL_OBJECTS, i)
        prompts.append(f"Surreal dream art: {', '.join(combined)}, ethereal lighting, soft focus.")

    # Execute in Parallel
    print(f"🚀 Launching {len(prompts)} parallel generation tasks...")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(generate_single_image, prompts))
    
    # Split results back into Recs and Dreams
    return results[:3], results[3:]