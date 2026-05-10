import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def ask_gemini(user_question, df):
    model = genai.GenerativeModel("gemini-3.1-flash-lite")
    
    data_text = df.to_string(index=False)
    
    prompt = f"""
You are a real estate data analyst. You have this Pune customer leads data:

{data_text}

Columns available:
- Name: customer name
- Budget: property budget in rupees
- Property Type: 2BHK or 3BHK
- Location: area in Pune (Kharadi, Aundh, Baner, Wakad,Hadapsar, Hinjewadi, Magarpatta, Kothrud, Pimple Saudagar, Viman Nagar etc)
- Contact: phone number
- Expected: expected purchase date
- Last Call Status: Busy / Switched / Connected / Call Back / Not Answered 
- Last Call Connected Time: date and time of last call

User question: "{user_question}"

RULES:
1. Answer ONLY using the data above. Never guess.
2. Show exact numbers and names from data.
3. Give a clean summary at the end.
4. Format nicely with bullet points if listing customers.

Answer:
"""
    response = model.generate_content(prompt)
    return response.text