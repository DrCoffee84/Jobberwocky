from flask import Flask, request, jsonify
from models import db, Job, Skill, JobSkill

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/jobs', methods=['POST'])
def create_job():
    job_data = request.json
    
    # Required fields
    required_fields = ['title', 'description', 'company_name', 'country', 'salary', 'posted_at', 'enabled', 'skills']
    if not all(field in job_data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400 # bad request

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

    # Fetch jobs with pagination
    jobs_query = Job.query.paginate(page=page, per_page=per_page, error_out=False)
    
    # Prepare the response data
    jobs = [job.to_dict() for job in jobs_query.items]
    for job in jobs:
        job['skills'] = [skill.to_dict() for skill in job.skills]
    
    # Pagination data
    pagination_data = {
        'total': jobs_query.total,  # Total number of jobs
        'pages': jobs_query.pages,  # Total number of pages
        'current_page': jobs_query.page,  # Current page number
        'next_page': jobs_query.next_num,  # Next page number (None if on last page)
        'prev_page': jobs_query.prev_num,  # Previous page number (None if on first page)
    }
    
    # Return jobs and pagination data
    return jsonify({
        'jobs': jobs,  # List of jobs
        'pagination': pagination_data  # Pagination info
    })




if __name__ == '__main__':
    app.run(debug=True)