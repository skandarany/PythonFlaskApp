from flask import Flask, render_template, request, redirect, url_for,jsonify
import psycopg2
import pytesseract
from werkzeug.utils import secure_filename
import os
from PIL import Image
from pdf2image import convert_from_path
import pdfplumber
import re
import json




# Supabase connection credentials
#SUPABASE_DB_HOST = "localhost"
#SUPABASE_DB_PORT = "5555"
#SUPABASE_DB_NAME = "postgres"
#SUPABASE_DB_USER = "postgres"
#SUPABASE_DB_PASSWORD = "your-super-secret-and-long-postgres-password"



# Create Flask app
app = Flask(__name__)

# Function to get database connection
#def get_db_connection():
   # connection = psycopg2.connect(
      #  host=SUPABASE_DB_HOST,
       # port=SUPABASE_DB_PORT,
       # database=SUPABASE_DB_NAME,
       # user=SUPABASE_DB_USER,
        #password=SUPABASE_DB_PASSWORD
   # )
   # return connection

#UPLOAD_FOLDER = './uploads'
#ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route to display the search form and results
# @app.route('/', methods=['GET', 'POST'])
# def index():
#     employees = []
#     location = request.form.get('location', '').strip()  # Get location input (default empty string)
#     skills_input = request.form.get('skills', '').strip()  # Get skills input (default empty string)
    
#     # Split multiple skills entered by the user (separated by commas)
#     skills = [skill.strip().lower() for skill in skills_input.split(',')] if skills_input else []

#     # Construct SQL query based on user input
#     query = "SELECT id, name, skills, location, position FROM employees WHERE TRUE"
#     conditions = []
#     params = []

#     if location:
#         conditions.append("LOWER(location) ILIKE %s")  # Case-insensitive location search
#         params.append(f"%{location.lower()}%")  # Add location as a parameter for SQL query

#     if skills:
#         # Case-insensitive check for each skill in the input
#         skill_conditions = []
#         for skill in skills:
#             skill_conditions.append("LOWER(skills::text[]) ILIKE %s")  # Check if the skill exists in the array
#             params.append(f"%{skill}%")

#         conditions.append(f"({' OR '.join(skill_conditions)})")  # Any skill match (OR condition for each skill)

#     # If there are conditions, append them to the query
#     if conditions:
#         query += " AND " + " AND ".join(conditions)

#     try:
#         # Establish database connection
#         connection = get_db_connection()
#         cursor = connection.cursor()

#         # Execute the query with the parameters
#         cursor.execute(query, params)
#         employees = cursor.fetchall()
#         cursor.close()
#         connection.close()
#     except Exception as e:
#         print("Error executing query:", e)
    
#     return render_template('index.html', employees=employees)





# @app.route('/ocr', methods=['GET', 'POST'])
# def ocr():
#     if request.method == 'POST':
#         if 'cv' not in request.files:
#             return "No file uploaded", 400
#         file = request.files['cv']
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             file.save(filepath)

#             # Check if the file is a PDF
#             if filename.lower().endswith('.pdf'):
#                 try:
#                     # Convert PDF to images
#                     images = convert_from_path(filepath, poppler_path='/usr/bin')  # Adjust as per your system
#                     # Extract text from each image page
#                     extracted_text = ""
#                     for image in images:
#                         extracted_text += pytesseract.image_to_string(image)

#                 except Exception as e:
#                     print("Error processing PDF:", str(e))  # Log the exact error
#                     return f"Error processing PDF: {str(e)}", 500

#             else:
#                 # Process as an image (if not PDF)
#                 try:
#                     extracted_text = pytesseract.image_to_string(Image.open(filepath))
#                 except Exception as e:
#                     print("Error processing image:", e)
#                     return "Error processing image", 500

#             # Debugging: Print the extracted text to the console
#             print("Extracted Text:", extracted_text)

#             # Split the extracted text into lines
#             lines = extracted_text.split('\n')

#             # Try to extract the name (looking for "Name:" or similar)
#             name = ""
#             for line in lines:
#                 if "name" in line.lower():  # Look for a line with the word 'name'
#                     name = line.strip().replace("Name:", "").strip()  # Clean up the line if needed
#                     break  # Stop once the name is found

#             # If no name was found, try the first non-empty line as the name
#             if not name:
#                 for line in lines:
#                     if line.strip():  # Skip empty lines
#                         name = line.strip()
#                         break

#             # Try to extract skills by checking for relevant lines
#             skills = []
#             for line in lines:
#                 if "skills" in line.lower():  # Look for lines containing 'skills'
#                     skills.extend([skill.strip() for skill in line.split(',')])  # Split by commas for multiple skills
#                 # If you want to look for specific skills, you can also check for those here
#                 # Example:
#                 # elif any(skill in line.lower() for skill in ['html', 'css', 'javascript']):
#                 #     skills.append(line.strip())

#             # Ensure skills is always a list (even if it's empty)
#             skills = skills if skills else []

#             # Log what we extracted to check if it's correct
#             print("Extracted Name:", name)
#             print("Extracted Skills:", skills)

#             # Save to database
#             try:
#                 connection = get_db_connection()
#                 cursor = connection.cursor()
#                 cursor.execute(
#                     "INSERT INTO employees (name, skills, location, position) VALUES (%s, %s, %s, %s)",
#                     (name, skills, 'Unknown', 'Unknown')  # Adjust as needed
#                 )
#                 connection.commit()
#                 cursor.close()
#                 connection.close()
#             except Exception as e:
#                 print("Error saving to database:", e)
#                 return "Database error", 500

#             return redirect(url_for('index'))

#     return render_template('ocr.html')

#skill_keywords = ["python", "java", "c++", "html", "css", "javascript", "sql", "machine learning", "deep learning", "data science", "php"]
experience_levels = ["senior", "junior", "mid-level", "lead", "entry-level", "intern","confirmed"]
##skill_categories = {
    ##"Web Development": ["html", "css", "javascript", "php"],
   ## "Data Analysis": ["power bi", "sql", "tableau"],
  ##  "Programming": ["python", "java", "c++"],
  ##  "Machine Learning": ["machine learning", "deep learning", "data science"],
##}

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    return text

import spacy
from spacy.matcher import PhraseMatcher

# load default skills data base
from skillNer.general_params import SKILL_DB
# import skill extractor
from skillNer.skill_extractor_class import SkillExtractor

# init params of skill extractor
nlp = spacy.load("en_core_web_lg")
#skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)
#annotations = skill_extractor.annotate(text)
def extract_skiller(text):
    skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)
    annotations = skill_extractor.annotate(text)
    unique_skills = set()  # Using a set to store unique skills

# Extract skills from 'full_matches'
    for match in annotations['results']['full_matches']:
        if match['score'] == 1:
            unique_skills.add(match['doc_node_value'])
    print("full matches",unique_skills)

# Extract skills from 'ngram_scored'
    #for match in annotations['results']['ngram_scored']:
        #if match['score'] == 1:
           # unique_skills.add(match['doc_node_value'])
   # print("ngram scored",unique_skills)

# Convert the set to a sorted list for display
    unique_skills_list = sorted(unique_skills)
    return unique_skills_list

#import spacy
#from spacy.matcher import PhraseMatcher

# load default skills data base
#from skillNer.general_params import SKILL_DB
# import skill extractor
#from skillNer.skill_extractor_class import SkillExtractor

from skillNer.visualizer.phrase_class import Phrase
from skillNer.visualizer.html_elements import DOM, render_phrase


#def extract_skills(text):
    #skills = [skill for skill in skill_keywords if re.search(r"\b" + re.escape(skill) + r"\b", text, re.IGNORECASE)]
   # return skills

#def extract_names_with_regex(text):
 #   match = re.findall(r'\b[A-Z][A-Z]+\s[A-Z][A-Z]+\b', text)
  #  return match

def extract_experience_level(text):
    for level in experience_levels:
        if re.search(r"\b" + re.escape(level) + r"\b", text, re.IGNORECASE):
            return level
    return None

def extract_years_experience(text):
    experience_pattern = r"(?:(?:over\s+)?(\d+)(?:\s*[-+]\s*\d*)?)\s+years?"
    matches = re.finditer(experience_pattern, text, re.IGNORECASE)
    
    years = []
    for match in matches:
        # Get the base number
        base_number = int(match.group(1))
        full_match = match.group(0).lower()
        
        # Add to years list, keeping the "+" notation in mind
        if '+' in full_match or 'over' in full_match:
            years.append(f"{base_number}+")
        else:
            years.append(str(base_number))
    
    if years:
        # Get the highest value, treating "X+" as higher than X
        max_year = max(years, key=lambda x: (int(x.rstrip('+')), '+' in x))
        return f"{'Over' if '+' not in max_year else ''} {max_year} years"
    
    return "No specific experience mentioned"

def extract_emails(text):
    """Extract email addresses from the text."""
    # Regular expression for emails
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, text)
    return emails if emails else ["No emails found"]


def extract_name_from_email(email):
    """Extract a name from an email address."""
    # Split the email into the part before '@'
    username = email.split('@')[0]

    # Replace common separators with spaces (e.g., '.', '_', '-')
    name_parts = re.split(r'[._-]', username)

    # Capitalize each part to format it as a proper name
    formatted_name = " ".join(part.capitalize() for part in name_parts if part)

    return formatted_name


###
#from skillNer.visualizer.phrase_class import Phrase
#from skillNer.visualizer.html_elements import DOM, render_phrase
def extract_hard_soft(text,hard_skills,soft_skills,certifications):
    skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)
    annotations = skill_extractor.annotate(text)
    arr_phrases = Phrase.split_text_to_phare(annotations,SKILL_DB)
    for a in arr_phrases:
        if a.skill_type=="Hard Skill" and a.skill_name not in hard_skills:
            hard_skills.append(a.skill_name)
        if a.skill_type=="Soft Skill" and a.skill_name not in soft_skills:
            soft_skills.append(a.skill_name)
        if a.skill_type=="Certification" and a.skill_name not in certifications:
            certifications.append(a.skill_name)
        

###




def process_cv(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    #skills = extract_skiller(text)
    #extract_hard_soft_certif()
    ##
    hard_skills=[]
    soft_skills=[]
    certifications=[]
    extract_hard_soft(text,hard_skills,soft_skills,certifications)
    uni_certifications=set(certifications)
   # annotations = skill_extractor.annotate(text)
   # arr_phrases = Phrase.split_text_to_phare(annotations,SKILL_DB)




   # extract_hard_soft_certif()
    # Extract experience level
    experience = extract_experience_level(text)
    #names = extract_names_with_regex(text)
    years=extract_years_experience(text)
    contact=extract_emails(text)
    print("contact ",contact)
    print("years years",years)
    username=extract_name_from_email(contact[0])
    print("username",username)

   ## category = [
      ##  category_name
      ##  for category_name, category_skills in skill_categories.items()
       ## if len([skill for skill in skills if skill in category_skills]) >= 2
    ##]

    return {
       ## "skills_category":category,
        #"skills": skills,
        "years_experience":years,
        "experience_level": experience,
        "name":username,
        "contact":contact,
        "hard_skills":hard_skills,
        "soft_skills":soft_skills
       # "certifications":certifications
       
    }


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        # Redirect to the upload page when accessed via GET
        return render_template('json.html')
    
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Process the uploaded file
        extracted_data = process_cv(filepath)

        # Save to JSON file
        output_json_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output4.json')
        with open(output_json_path, 'w') as json_file:
            json.dump(extracted_data, json_file, indent=4)

        return jsonify({"message": "File processed successfully", "data": extracted_data})


    


# Run the app
if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)








