import os
import time
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from groq import Groq


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
GROQ_KEY = os.getenv("GROQ_API_KEY")
if not api_key:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except:
        api_key = "AIzaSyA4Yemxk0OYleVIQEUMxkpM9wWwyRdBDTU"

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-flash-latest")
groq_client = Groq(api_key=GROQ_KEY) if GROQ_KEY else None

@st.cache_data(show_spinner=False)
def get_ai_response(vital_stats, task_type):
    prompts = {
        "summary": f"Summarize these business stats in 3 short bullets: {vital_stats['financials']}.",
        "anomalies": f"Identify one major risk from these data points: {vital_stats['risks']}.",
        "actions": f"Suggest 3 profit-boosting actions for a company with a {vital_stats['financials']['margin']} margin."
    }

    # Attempt twice to handle random API failures
# Use 3 attempts and a longer wait to stop the 'Connection Busy' error
    for attempt in range(3):
        try:
            response = model.generate_content(
                prompts[task_type],
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=500, 
                    temperature=0.1
                )
            )
            
            # Check for valid text response
            if response and response.candidates and len(response.candidates[0].content.parts) > 0:
                return response.text.strip()
            
            # If empty, wait longer before retrying (1.5 seconds is the sweet spot)
            time.sleep(1.5)
            continue 

        except Exception:
            # On the final attempt, show a helpful message instead of crashing
            if attempt == 2:
                return "The system is currently busy. Please wait 2 seconds and click the button again."
            time.sleep(1.5)
            
    return "AI Service Notice: Please try clicking the button once more."
def get_chat_response(vital_stats, user_query):

    if not groq_client:
        return "Groq API key not configured."

    context = f"""
    Dataset Scope: {vital_stats.get('scope')}
    Financials: {vital_stats.get('financials')}
    Categories: {vital_stats.get('champions', {}).get('category')}

    If a question asks for missing data, clearly say it is not available.
    """

    try:
        completion = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful business analyst."},
                {"role": "user", "content": f"{context}\n\nQuestion: {user_query}"}
            ],
            temperature=0.2,
            max_tokens=300
        )

        return completion.choices[0].message.content

    except Exception as e:
        return f"Chat Error: {str(e)}"
