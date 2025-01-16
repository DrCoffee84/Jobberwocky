from flask import Flask
from flask_testing import TestCase

class MyTest(TestCase):
    
    
    def create_app(self):
        app = Flask(__name__)
        return app

    # Creo un job 
    def test_job_creation(self):
        response = self.client.post('/jobs', json={
            'title': 'Devops', 
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
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)
