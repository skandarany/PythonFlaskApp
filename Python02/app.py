from flask import Flask, render_template, request, redirect, url_for,jsonify,Response
#import psycopg2
#import pytesseract
from werkzeug.utils import secure_filename
import os
from PIL import Image
from pdf2image import convert_from_path
import pdfplumber
import re
import json
from datetime import datetime
import pandas as pd
import panel as pn
import threading

from bokeh.embed import server_document




pn.extension()

# Create Flask app
#app = Flask(__name__)


app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
#app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
experience_levels = ["senior", "junior", "mid-level", "lead", "entry-level", "intern","confirmed"]

Indus_Dict=["TC Consulting (Siemens Solutions)",
"AWC (Siemens Solutions)",
"RAC (Siemens Solutions)",
"ITK (Siemens Solutions)",
"BMIDE (Siemens Solutions)",
"TC Workflow (Siemens Solutions)",
"TC NX Integration (Siemens Solutions)",
"TC Catia Integration (Siemens Solutions)",
"TC AIG (T4E) (Siemens Solutions)",
"NX (Siemens Solutions)",
"NXOpen (Siemens Solutions)",
"JTOpen (Siemens Solutions)",
"Teamcenter Enterprise (Siemens Solutions Metaphase)",
"Deployment Center (Siemens Solutions)",
"Multisite (Siemens Solutions)",
"Opcenter  (Siemens Solutions Camstar & Simatic-IT)",
"Opcenter Integrations (Siemens Solutions Connect MOM)",
"System Modeling Workbench (Siemens Solutions)",
"Supplier Collaboration (Siemens Solutions)",
"Manufacturing (MPP)+ Easy Plan (Siemens Solutions)",
"MBSE (Siemens Solutions)",
"JT (Siemens Solutions)",
"SOA (Siemens Solutions)",
"BOM (Siemens Solutions)",
"PLMXML (Siemens Solutions)",
"Tecnomatix | Process Designer (Siemens Solutions)",
"Tecnomatix | Process Simulate (Siemens Solutions)",
"Tecnomatix | Plant Simulation (Siemens Solutions)",
"Windchill Consulting (PTC Solutions)",
"Windchill Customization (PTC Solutions)",
"Integrity/RV&S (PTC Solutions)",
"Windchill server side administration  (PTC Solutions)",
"Windchill +  (PTC Solutions)",
"ALM | Codebeamer (PTC Solutions)",
"ALM | PTC Modeler (PTC Solutions)",
"AR | Vuforia Work Instructions (PTC Solutions)",
"AR | Vuforia Studio (PTC Solutions)",
"AR | Vuforia Expert Capture (PTC Solutions)",
"AR | Vuforia Engine (PTC Solutions)",
"AR | Vuforia Chalk (PTC Solutions)",
"CAD | Onshape (PTC Solutions)",
"CAD | Creo Elements/Direct (PTC Solutions)",
"CAD | Creo (PTC Solutions)",
"IIOT | ThingWorx Platform for IIoT-Solutions (PTC Solutions)",
"IIOT | ThingWorx Manufacturing Apps (PTC Solutions)",
"IIOT | ThingWorx Kepware Server (PTC Solutions)",
"IIOT | ThingWorx Digital Performance Management (PTC Solutions)",
"PLM | Windchill (PTC Solutions)",
"PLM | ThingWorx Navigate (PTC Solutions)",
"PLM | FlexPLM (PTC Solutions)",
"PLM | Creo View (PTC Solutions)",
"PLM | Arena (PTC Solutions)",
"CADDS 5 (PTC Solutions)",
"PTC Developer Tools (PTC Solutions)",
"PTC Implementer (PTC Solutions)",
"SLM | ThingWorx Asset Advisor (PTC Solutions)",
"SLM | Servigistics (PTC Solutions)",
"SLM | ServiceMax (PTC Solutions)",
"SLM | Service Knowledge and Diagnostics (PTC Solutions SKD)",
"SLM | PTC Warranty (PTC Solutions)",
"Mathcad | Mathcad Prime (PTC Solutions)",
"Mathcad | Mathcad Express (PTC Solutions)",
"SLM | Creo Illustrate (PTC Solutions)",
"SLM | Arbortext (PTC Solutions)",
"Windchill | DocumentManagement (PTC Solutions)",
"Windchill | BaselineandEffectivityManagement (PTC Solutions)",
"Windchill | CADWorkspaceManagement (PTC Solutions)",
" (PTC Solutions)",
"Knowledgegraph (Interoperability)",
"eQube (Interoperability)",
"SPRQL (Interoperability)",
"ETL (Interoperability)",
" (Interoperability)",
"Opcenter (PLM Complementary)",
"Opcenter RdnL (PLM Complementary)",
"Mendix (PLM Complementary)",
"Migration (PLM Complementary)",
"E-CAD (PLM Complementary Mentor, Graphics, EPLAN)",
"DATA Migration (PLM Complementary CDM Importer)",
"ALM (PLM Complementary)",
"PLM (PLM Complementary)",
"Pro/E (PLM Complementary)",
"Auto Cad (PLM Complementary)",
"ACL (General Technologies)",
"TCL (General Technologies)",
"Project Management (Process & Methods)",
"SAFe (Process & Methods)",
"System Engineering (Process & Methods)",
"ISTQB (Process & Methods)",
"Scrummaster (Process & Methods)",
"UML (Process & Methods)",
"Leadership / Soft Skills (Process & Methods)",
"Project Controlling (Process & Methods)",
"Waterfall (Process & Methods)",
"ISO (Process & Methods)",
"Process Management (Process & Methods)",
"Six Sigma (Process & Methods)",
"RCP (Process & Methods)",
"XML (Process & Methods)",
"Smaragd (Individual Solutions)",
"Connect (Individual Solutions)",
"Globus (Individual Solutions)",
"NWC (Net Work Client) (Individual Solutions)",
"FAPLIS-Navigator (Individual Solutions)",
"FAPLIS-WebClient (Individual Solutions)",
"FAPLIS4Experts (Individual Solutions)",
"MicroStation V8i (Bentley Solutions SS4)",
"MicroStation CONNECT 2023 (Bentley Solutions)",
"3DS | 3DExcite (Dassault Solutions)",
"3DS | 3DVia (Dassault Solutions)",
"3DS | BioVia (Dassault Solutions)",
"3DS | Delmia (Dassault Solutions)",
"3DS | CentricPLM (Dassault Solutions)",
"3DS | Catia (Dassault Solutions)",
"3DS | MediData (Dassault Solutions)",
"3DS | GeoVia (Dassault Solutions)",
"3DS | Enovia (Dassault Solutions)",
"3DS | SolidWorks (Dassault Solutions)",
"3DS | Simulia (Dassault Solutions)",
"3DS | Netvibes (Dassault Solutions)",
"TIBCO (TIBCO Software Inc. SAP-Interface)"]

result = {}
for item in Indus_Dict:
    if "(" in item and ")" in item:
        key = item.split("(")[0].strip()
        value = item.split("(")[1].replace(")", "").strip()
        result[key] = value


def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    return text
import spacy
from spacy.matcher import PhraseMatcher
from skillNer.general_params import SKILL_DB
from skillNer.skill_extractor_class import SkillExtractor
nlp = spacy.load("en_core_web_lg")
skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)
def extract_skiller(text):
    
    annotations = skill_extractor.annotate(text)
    unique_skills = set()  # Using a set to store unique skills
    for match in annotations['results']['full_matches']:
        if match['score'] == 1:
            unique_skills.add(match['doc_node_value'])
    print("full matches",unique_skills)
    unique_skills_list = sorted(unique_skills)
    return unique_skills_list
from skillNer.visualizer.phrase_class import Phrase
from skillNer.visualizer.html_elements import DOM, render_phrase
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
        max_year = max(years, key=lambda x: (int(x.rstrip('+')), '+' in x))
        return f"{'Over' if '+' not in max_year else ''} {max_year} years"
    return "No specific experience mentioned"
def extract_emails(text):
    """Extract email addresses from the text."""
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, text)
    return emails if emails else ["No emails found"]
def extract_name_from_email(email):
    """Extract a name from an email address."""
    username = email.split('@')[0]
    name_parts = re.split(r'[._-]', username)
    formatted_name = " ".join(part.capitalize() for part in name_parts if part)
    return formatted_name
def extract_hard_soft(text,hard_skills,soft_skills,certifications):
    #skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)
    annotations = skill_extractor.annotate(text)
    arr_phrases = Phrase.split_text_to_phare(annotations,SKILL_DB)
    for a in arr_phrases:
        if a.skill_type=="Hard Skill" and a.skill_name not in hard_skills:
            hard_skills.append(a.skill_name)
        if a.skill_type=="Soft Skill" and a.skill_name not in soft_skills:
            soft_skills.append(a.skill_name)
        if a.skill_type=="Certification" and a.skill_name not in certifications:
            certifications.append(a.skill_name)
    for key,value in result.items():
        if re.search(r"\b" + re.escape(key) + r"\b", text, re.IGNORECASE) and key not in hard_skills:
            hard_skills.append(key+" ("+value+")")
###
def extract_categ_skills(skill_list):
    """Extract unique values from parentheses in a list of strings."""
    values = []
    for skill in skill_list:
        match = re.search(r'\((.*?)\)', skill)
        if match:
            values.append(match.group(1))
    return list(set(values))


def process_cv(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    hard_skills=[]
    soft_skills=[]
    certifications=[]
    extract_hard_soft(text,hard_skills,soft_skills,certifications)
    uni_certifications=set(certifications)
    categ_skills=extract_categ_skills(hard_skills)
    experience = extract_experience_level(text)
    years=extract_years_experience(text)
    contact=extract_emails(text)
    print("contact ",contact)
    print("years years",years)
    username=extract_name_from_email(contact[0])
    print("username",username)
    return {
        "skills_category":categ_skills,
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
        return render_template('json.html')
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        extracted_data = process_cv(filepath)
        current_time = datetime.now()
        formatted_time = current_time.strftime("%d-%m-%Y-%H-%M-%S") + ".json"
        print(formatted_time)
        output_json_path = os.path.join(app.config['UPLOAD_FOLDER'],formatted_time)
        with open(output_json_path, 'w') as json_file:
            json.dump(extracted_data, json_file, indent=4)
        return jsonify({"message": "File processed successfully", "data": extracted_data})



def load_employee_data(folder):
    employee_data = []
    for file_name in os.listdir(folder):
        if file_name.endswith(".json"):
            with open(os.path.join(folder, file_name), "r") as f:
                data = json.load(f)
                employee_data.append({
                    "Name": data.get("name"),
                    "Experience": data.get("years_experience"),
                    "Experience Level": data.get("experience_level"),
                    "Contact": ", ".join(data.get("contact", [])),
                    "Hard Skills": data.get("hard_skills", []),
                    "Soft Skills": data.get("soft_skills", []),
                })
    return pd.DataFrame(employee_data)

# Load the data
employee_df = load_employee_data(UPLOAD_FOLDER)

# Widgets and Tables
employee_table = pn.widgets.Tabulator(
    employee_df[["Name", "Experience", "Experience Level", "Contact"]], 
    selection=[0],  # Default selection
    height=300
)
skills_table = pn.widgets.Tabulator(
    pd.DataFrame(columns=["Skill Type", "Skill"]), 
    height=300
)

# Function to update skills_table based on selected employee
def update_skills_table(event):
    selected_indices = employee_table.selection
    if selected_indices:
        selected_index = selected_indices[0]
        employee = employee_df.iloc[selected_index]
        hard_skills = [{"Skill Type": "Hard Skill", "Skill": skill} for skill in employee["Hard Skills"]]
        soft_skills = [{"Skill Type": "Soft Skill", "Skill": skill} for skill in employee["Soft Skills"]]
        combined_skills = hard_skills + soft_skills
        skills_table.value = pd.DataFrame(combined_skills)
    else:
        skills_table.value = pd.DataFrame(columns=["Skill Type", "Skill"])

# Attach the callback to employee_table.selection
employee_table.param.watch(update_skills_table, "selection")

# Trigger the callback initially to populate the right table for the default selection
update_skills_table(None)

# Panel app layout
def panel_app():
    return pn.Column(
        "## Employee Skills Viewer",
        pn.Row(
            pn.Column("### Employees", employee_table), 
            pn.Column("### Skills", skills_table)
        )
    )

# Function to serve the Panel app in a separate thread
def run_panel():
    pn.serve(panel_app, port=5006, show=False,allow_websocket_origin=["localhost:5000", "localhost:5006"])

# Flask routes


@app.route("/panel")
def panel_page():
    # Render the page that embeds the Panel app
    return render_template("panel.html")
    #return redirect("http://localhost:5006")




# Run the app





if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    threading.Thread(target=run_panel, daemon=True).start()
    app.run(debug=True, port=5000)
   # pn.serve(panel_app, port=5006, show=False)  # Start the Panel server
    #app.run(debug=True)


