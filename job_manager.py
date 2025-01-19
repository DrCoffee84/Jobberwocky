from flask import Flask, request, jsonify,render_template
from models import db, Job, Skill, JobSkill
from math import ceil
from sqlalchemy.orm import joinedload
from services import fetch_jobs_from_external_service
from utils import validate_job_data

import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

logging.basicConfig(level=logging.INFO)


@app.route('/')
def Frontend():
    return render_template('index.html')

@app.route('/jobs', methods=['POST'])
def create_job():
    job_data = request.json
    validation_result = validate_job_data(job_data)

    if validation_result:
        return validation_result
    
    new_job = Job(
        title=job_data['title'],
        description=job_data['description'],
        company_name=job_data['company_name'],
        country=job_data['country'],
        salary=job_data['salary'],
        posted_at=job_data['posted_at'],
        enabled=job_data['enabled']
    )

    db.session.add(new_job)
    db.session.flush() # Force to get ID

    skills_list = []
    for skill in job_data['skills']:
        if 'id' in skill:
            skill_instance = db.session.get(Skill, skill['id'])
            if not skill_instance:
                return jsonify({"error": "Skill not found"}), 404
        else:
            # Validate the fields are correct
            if 'name' in skill and 'level' in skill:
                skill_instance = Skill(name=skill['name'], level=skill['level'])
                db.session.add(skill_instance)
                db.session.flush() # Force to get ID
            else:
                return jsonify({"error": "Each skill must have an 'id' or both 'name' and 'level'."}), 400


        # N to N relationship
        new_job_skill = JobSkill(job_id=new_job.id, skill_id=skill_instance.id)
        db.session.add(new_job_skill)
        skills_list.append(skill_instance.to_dict()) 

    # If everything went well, I commit the changes to the database.
    try:
        db.session.commit()
        response_data = new_job.to_dict()
        response_data['skills'] = skills_list
        return jsonify(response_data), 201
    except Exception as e:
        db.session.rollback()  # Rollback en caso de error
        return jsonify({"error": str(e)}), 500


@app.route('/jobs', methods=['GET'])
def get_jobs():
    # Pagination parameters: page (current page) and per_page (items per page)
    page = request.args.get('page', 1, type=int)  # Default page is 1
    per_page = request.args.get('per_page', 10, type=int)  # Default is 10 items per page
    
    # Search pattern for the job description
    search = request.args.get('search', '', type=str)  # Default is an empty string (no filtering)
    date_filter = request.args.get('posted_after', None, type=str)  # Filter by date (YYYY-MM-DD)
    salary_min = request.args.get('salary_min', None, type=int)  # Minimum salary
    salary_max = request.args.get('salary_max', None, type=int)  # Maximum salary
    company_name = request.args.get('company_name', '', type=str)  # Filter by company name
    country = request.args.get('country', '', type=str)  # Filter by country
    skills_filter = request.args.getlist('skills')  # Filter by skills (list of skills)
    external_source = request.args.get('external_source') # Get jobs from external source 

    # Base query for jobs
    query = Job.query.options(joinedload(Job.job_skills).joinedload(JobSkill.skill))

    # Apply the search filter if provided
    if search:
        query = query.filter((Job.description.ilike(f"%{search}%")) | (Job.title.ilike(f"%{search}%")))
    if date_filter:
        query = query.filter(Job.posted_at >= date_filter)  # Jobs posted after a specific date
    if salary_min is not None:
        query = query.filter(Job.salary >= salary_min)  # Jobs with salary >= salary_min
    if salary_max is not None:
        query = query.filter(Job.salary <= salary_max)  # Jobs with salary <= salary_max
    if company_name:
        query = query.filter(Job.company_name.ilike(f"%{company_name}%"))  # Search by company name
    if country:
        query = query.filter(Job.country.ilike(f"%{country}%"))  # Search by country name
    if skills_filter:
        query = query.join(JobSkill).join(Skill).filter(Skill.name.in_(skills_filter)).distinct()  # Filter by skills
    else:
        query = query.join(JobSkill).join(Skill).distinct()
    
    # Fetch jobs with pagination
    jobs_query = query.paginate(page=page, per_page=per_page, error_out=False)
    # To Dict
    db_jobs = [job.to_dict() for job in jobs_query.items]
    
    # Get external Jobs
    external_jobs = []  # A redis could be used
    if external_source != 'false':
        external_jobs = fetch_jobs_from_external_service(search,salary_min,salary_max,country,date_filter,company_name,skills_filter)
    
    # Combine both lists of jobs
    all_jobs = db_jobs + external_jobs
    
    # Manually paginate the combined list
    total_jobs = len(external_jobs) + jobs_query.total  # Total number of jobs
    total_pages = ceil(total_jobs / per_page)  # Total number of pages
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    paginated_jobs = all_jobs[start_index:end_index]
   
    # Prepare the pagination data
    pagination_data = {
        'total': total_jobs,  # Total number of jobs
        'pages': total_pages,  # Total number of pages
        'current_page': page,  # Current page number
        'next_page': page + 1 if page < total_pages else None,  # Next page number (None if on last page)
        'prev_page': page - 1 if page > 1 else None,  # Previous page number (None if on first page)
    }

    # Return jobs and pagination data
    return jsonify({
        'jobs': paginated_jobs,  # List of jobs
        'pagination': pagination_data  # Pagination info
    })

if __name__ == '__main__':
    app.run(debug=True)