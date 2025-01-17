from flask import Flask
from flask_testing import TestCase
from job_manager import app, db

class MyTest(TestCase):
    
    
    def create_app(self):
        app.config['TESTING'] = True
        return app
    
    # Clean the database before each test
    def setUp(self):
        db.create_all()

    # Clean after each test
    def tearDown(self): 
        db.session.remove()
        db.drop_all()

    # Create a normal job
    def test_job_creation(self):
        response = self.client.post('/jobs', json={
            "title": "Devops", 
            "description": "Responsible for designing, implementing, and maintaining infrastructure automation.",
            "company_name": "Tech Solutions Inc.",
            "country": "Argentina",
            "salary": 1_000_000_000,  # Mi salario (?)
            "posted_at": "2025-01-16",
            "enabled": True,
            "skills": [
                { 
                    "name": "Linux",
                    "level": "High"
                }
            ]})

        self.assertIn('id', response.json, f"'id' not found in response body: {response.json}")
        self.assertEqual(response.status_code, 201)
    
    # I create a job without title
    def test_job_bad_creation(self):
        response = self.client.post('/jobs', json={
            # title: "no esta :("
            "description": "Responsible for designing, implementing, and maintaining infrastructure automation.",
            "company_name": "Tech Solutions Inc.",
            "country": "Argentina",
            "salary": 1000000000, 
            "posted_at": "2025-01-16",
            "enabled": True,
            "skills": [
                {
                    "id": 101
                },
                { 
                    "name": "Linux",
                    "level": "High"
                }
            ]})
        
        # BAD_REQUEST is expected
        self.assertEqual(response.status_code, 400)
    
    # I create a job without title
    def test_job_bad_skill_creation(self):
        response = self.client.post('/jobs', json={
            "title": "Devops", 
            "description": "Responsible for designing, implementing, and maintaining infrastructure automation.",
            "company_name": "Tech Solutions Inc.",
            "country": "Argentina",
            "salary": 1000000000, 
            "posted_at": "2025-01-16",
            "enabled": True,
            "skills": [
                { 
                    "mensaje": "Que fiaca" 
                }
            ]})
        
        # BAD_REQUEST is expected
        # I would expect it to fail since the skill model should be "id" or create a new one that with "name" and "level"
        self.assertEqual(response.status_code, 400)

    # Create new Skill and use in another job
    def test_job_existing_skill(self):
        response1 = self.client.post('/jobs', json={
            "title": "Devops", 
            "description": "Responsible for designing, implementing, and maintaining infrastructure automation.",
            "company_name": "Tech Solutions Inc.",
            "country": "Argentina",
            "salary": 1000000000,  # Mi salario (?)
            "posted_at": "2025-01-16",
            "enabled": True,
            "skills": [
                { 
                    "name": "Linux",
                    "level": "High"
                }
            ]})
        
        self.assertEqual(response1.status_code, 201)
        idSkill = response1.json['skills'][0]['id']


        response2 = self.client.post('/jobs', json={
            "title": "Devops", 
            "description": "Responsible for designing, implementing, and maintaining infrastructure automation.",
            "company_name": "Tech Solutions Inc.",
            "country": "Argentina",
            "salary": 1000000000, 
            "posted_at": "2025-01-16",
            "enabled": True,
            "skills": [
                { 
                   "id": idSkill
                }
            ]})      
        
        self.assertEqual(response2.status_code, 201)

    
