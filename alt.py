from google import genai
from google.genai import types
from dotenv import load_dotenv
import pathlib
from docx import Document
from docx.shared import Inches, Pt

load_dotenv()
client = genai.Client()

meetings_image = pathlib.Path('meetings.png')

with open('outings_prompt.txt', 'r') as file:
    prompt = file.read()

outings = client.models.generate_content(
  model="gemini-2.5-flash",
  contents=[
      types.Part.from_bytes(
        data=meetings_image.read_bytes(),
        mime_type='image/png',
      ),
      prompt])

print(outings.text)