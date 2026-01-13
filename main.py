from google import genai
from google.genai import types
from dotenv import load_dotenv
import pathlib
from docx import Document
from docx.shared import Inches, Pt

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

notes = response.text

# notes = """
# February 2 []
# Opening [Daiwik, Anish, Rohan]: (15)
# Skill [Aneesh, AT]: (20)
# Game [Tavish, Tejas]: (20)
# Intrapatrol [Daiwik, Anish]: (20)
# Closing [Rohan, Aneesh, AT]: (15)

# February 9 []
# Opening [Anish, Rohan, Aneesh]: (15)
# Skill [AT, Tavish]: (20)
# Game [Tejas, Daiwik]: (20)
# Intrapatrol [Anish, Rohan]: (20)
# Closing [Aneesh, AT, Tavish]: (15)

# February 23 []
# Opening [Rohan, Aneesh, AT]: (15)
# Skill [Tavish, Tejas]: (20)
# Game [Daiwik, Anish]: (20)
# Intrapatrol [Rohan, Aneesh]: (20)
# Closing [AT, Tavish, Tejas]: (15)
# """

doc = Document()

style = doc.styles['Normal']
style.font.name = 'Arial'
style.paragraph_format.space_after = Pt(0)
style.paragraph_format.space_before = Pt(0)
style.paragraph_format.line_spacing = 1

# Split the input into individual lines
lines = notes.strip().split('\n')

for line in lines:
    line = line.strip()
    
    # Skip empty lines
    if not line:
        continue
    
    paragraph = doc.add_paragraph()
    if line.split()[0] in ("Opening", "Skill", "Game", "Intrapatrol", "Closing"):
        # bullet point
        doc.add_paragraph(line, style='List Bullet')
    else:
        doc.add_paragraph(line)

doc.save("plc_notes.docx")
print("Outputted to plc_notes.docx")