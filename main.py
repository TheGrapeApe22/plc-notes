from google import genai
from google.genai import types
from dotenv import load_dotenv
import pathlib

load_dotenv()
client = genai.Client()

filepath = pathlib.Path('newsletter.png')

with open('prompt.txt', 'r') as file:
    prompt = file.read()

response = client.models.generate_content(
  model="gemini-2.5-flash",
  contents=[
      types.Part.from_bytes(
        data=filepath.read_bytes(),
        mime_type='image/png',
      ),
      prompt])
print(response.text)