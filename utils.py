from flask import jsonify
from datetime import datetime
from models import Skill
from lxml import etree
import logging

def xmlToSkill(skills_xml: str, level: str = 'Intermediate'):
    #Parse XML
    try:
        root = etree.fromstring(skills_xml)
    except etree.XMLSyntaxError as e:
        logging.error(f"Error parsing XML: {e}")
        return []
    
    # Create skill list
    skills = []
    for skill_element in root.findall('skill'):
        skill_name = skill_element.text.strip()
        if skill_name:  
            skill = Skill(name=skill_name, level=level) 
            skills.append(skill)
    
    return skills 

def validate_job_data(job_data):
    # Required fields
    required_fields = ['title', 'description', 'company_name', 'country', 'salary', 'posted_at', 'enabled', 'skills']
    missing_fields = [field for field in required_fields if field not in job_data]

    if missing_fields:
        return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

    # Validate title (max 100 characters)
    if not isinstance(job_data['title'], str) or len(job_data['title']) > 100:
        return jsonify({"error": "Title must be a string not exceeding 100 characters"}), 400

    # Validate description (should be text, no specific length given, but let's check if it's not empty)
    if not isinstance(job_data['description'], str) or not job_data['description'].strip():
        return jsonify({"error": "Description must be a non-empty string"}), 400

    # Validate company_name (max 100 characters)
    if not isinstance(job_data['company_name'], str) or len(job_data['company_name']) > 100:
        return jsonify({"error": "Company name must be a string not exceeding 100 characters"}), 400

    # Validate country (max 50 characters)
    if not isinstance(job_data['country'], str) or len(job_data['country']) > 50:
        return jsonify({"error": "Country must be a string not exceeding 50 characters"}), 400

    # Validate salary (must be an integer, no decimals)
    if not isinstance(job_data['salary'], int) or not str(job_data['salary']).isdigit():
        return jsonify({"error": "Salary must be an integer without decimals"}), 400

    # Validate posted_at (must be in format 'YYYY-MM-DD')
    try:
        datetime.strptime(job_data['posted_at'], '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Posted_at must be in format 'YYYY-MM-DD'"}), 400

    # Validate enabled (must be boolean)
    if not isinstance(job_data['enabled'], bool):
        return jsonify({"error": "Enabled must be a boolean"}), 400

    # Skills validation (assuming it's a list of dictionaries, but we'll keep it simple here)
    if not isinstance(job_data['skills'], list):
        return jsonify({"error": "Skills must be a list"}), 400

    return None  # No errors found