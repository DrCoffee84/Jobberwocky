from models import db, Job
from datetime import datetime
from utils import xmlToSkill
import requests, os, logging

url_external_source = os.getenv('URL_EXTERNAL_SOURCE', 'localhost:8081')


def fetch_jobs_from_external_service(name=None, salary_min=None, salary_max=None, country=None,date_filter=None,company_name=None,skills_filter=None):
    # Build params
    params = {}
    if name:
        params['name'] = name
    if salary_min:
        params['salary_min'] = salary_min
    if salary_max:
        params['salary_max'] = salary_max
    if country:
        params['country'] = country
    if  company_name != '':
        if company_name != "Unknow Company":
            return []       
    
    today = datetime.now().strftime('%Y-%m-%d')
    if date_filter:
        # Convert to datetime to comprare
        today_date = datetime.strptime(today, '%Y-%m-%d') 
        date_filter_date = datetime.strptime(date_filter, '%Y-%m-%d')
        if date_filter_date >= today_date: 
            logging.debug("Warning: Assuming the job post date from external sources is today.")
            return []

    # Call extra source service 
    try:
        
        response = requests.get(f"http://{url_external_source}/jobs", params=params)
        response.raise_for_status()  
        
        # Get json
        jobs_data = response.json()
        
        # Convertir la respuesta en un formato más conveniente
        formatted_jobs = []
        for country, jobs in jobs_data.items():
            for job in jobs:
                job_instance = Job(
                    title=job[0],
                    description="This job is from jobberwocky-extra-source-v2", 
                    company_name="Unknow Company",
                    country=country,
                    salary=job[1],
                    posted_at=today,
                    enabled=True,
                    external="jobberwocky-extra-source-v2"
                )
                skills=xmlToSkill(job[2])
                job_data = job_instance.to_dict()
                job_data['skills'] = []

                for skill in skills:
                    job_data['skills'].append(skill.to_dict())
                    
                
                '''
                In case the answer always includes a large number of jobs and filtering by skills is not possible, 
                it could be more efficient to store the jobs in Redis and use it to query by skills.
                Update the redis every time to be defined, in case there are new jobs and others that were cancelled.
                redis.sinter('jobs:skills', *skills_filter) 
                '''
                # Check if any skill is in the skill filter
                if skills_filter:
                    # Check if any skills in the list are in skills_filter when skills filter isn't None
                    if [skill.name for skill in skills if skill.name in skills_filter]:
                        formatted_jobs.append(job_data)
                else:
                    formatted_jobs.append(job_data)          

        # Return a dictionary
        return formatted_jobs

    except requests.exceptions.RequestException as e:
        logging.warning("Warning: Failed to connect to external source.")
        return []