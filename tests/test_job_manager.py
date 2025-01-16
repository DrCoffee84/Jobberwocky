from flask import Flask
from flask_testing import TestCase
from job_manager import app 

class MyTest(TestCase):
    
    
    def create_app(self):
        return app

    # I create a normal job
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
                    "id": 101
                },
                { 
                    "name": "Linux",
                    "level": "High"
                }
            ]})
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)
    
    # I create a job without title
    def test_job_bad_creation(self):
        response = self.client.post('/jobs', json={
            # title: "no esta :("
            "description": "Responsible for designing, implementing, and maintaining infrastructure automation.",
            "company_name": "Tech Solutions Inc.",
            "country": "Argentina",
            "salary": 1000000000,  # Mi salario (?)
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
            "salary": 1000000000,  # Mi salario (?)
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

