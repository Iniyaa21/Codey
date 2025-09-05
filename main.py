import os 
from dotenv import load_dotenv 
from google import genai 

load_dotenv() 
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents='Suggest some fall activities with a dark academia twist. Limit to one paragraph only'
)
print(response.text)
