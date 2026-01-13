from google import genai
from google.genai import types
from dotenv import load_dotenv
import pathlib
from docx import Document
from docx.shared import Inches, Pt

load_dotenv()
client = genai.Client()

meetings_image = pathlib.Path('meetings.png')

with open('meetings_prompt.txt', 'r') as file:
    prompt = file.read()

meetings = client.models.generate_content(
  model="gemini-2.5-flash",
  contents=[
      types.Part.from_bytes(
        data=meetings_image.read_bytes(),
        mime_type='image/png',
      ),
      prompt])

# build docx
doc = Document()

style = doc.styles['Normal']
style.font.name = 'Arial'
style.paragraph_format.space_after = Pt(0)
style.paragraph_format.space_before = Pt(0)
style.paragraph_format.line_spacing = 1

# meetings
lines = meetings.text.strip().split('\n')
for line in lines:
    # strip
    line = line.strip()
    if not line:
        continue
    
    # bullet point
    if line.split()[0] in ("Opening", "Skill", "Game", "Intrapatrol", "Closing"):
        doc.add_paragraph(line, style='List Bullet')
    else:
        doc.add_paragraph(line)

doc.save("plc_notes.docx")
print("Outputted to plc_notes.docx")