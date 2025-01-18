from flask import Flask
from flask_testing import TestCase
from job_manager import app, db
from copy import deepcopy
import random

class JobManagerTest(TestCase):
    
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
    
 
    job_valid_examples = [
        {"title":"Devops","description":"Responsible for designing, implementing, and maintaining infrastructure automation. ESENCIA","company_name":"Tech Solutions Inc.","country":"Argentina","salary":1000000000,"posted_at":"2025-01-16","enabled":True,"skills":[{"name":"Linux","level":"High"}]},
        {"title":"Python Developer","description":"Develop and maintain Python applications.","company_name":"The Coffee Machine","country":"Brazil","salary":1000,"posted_at":"2025-01-16","enabled":True,"skills":[{"name":"Python","level":"Medium"}]},
        {"title":"Java Developer","description":"Spring Boot developer.","company_name":"Tech Solutions Inc.","country":"Argentina","salary":3000,"posted_at":"2025-02-20","enabled":False,"skills":[{"name":"Java","level":"High"}]}, 
        {"title":"Web Developer","description":"Develop websites and web applications.","company_name":"Web World","country":"USA","salary":2500,"posted_at":"2025-03-01","enabled":True,"skills":[{"name":"HTML","level":"High"},{"name":"CSS","level":"Medium"}]},
        {"title":"Data Scientist","description":"Analyze data to extract insights.","company_name":"Data Inc.","country":"Canada","salary":5000,"posted_at":"2025-04-10","enabled":True,"skills":[{"name":"Python","level":"Advanced"},{"name":"SQL","level":"Medium"}]},
        {"title":"QA Engineer","description":"Test and ensure the quality of software.","company_name":"Tech Solutions Inc.","country":"Argentina","salary":1500,"posted_at":"2025-05-15","enabled":True,"skills":[{"name":"Manual Testing","level":"High"},{"name":"Automation Testing","level":"Medium"}]},
        {"title":"Product Manager","description":"Oversee product development and strategy.","company_name":"Product Co.","country":"UK","salary":4500,"posted_at":"2025-06-20","enabled":False,"skills":[{"name":"Project Management","level":"High"},{"name":"Agile","level":"Medium"}]},
        {"title":"Backend Developer","description":"Develop server-side logic and APIs.","company_name":"Tech Solutions Inc.","country":"Argentina","salary":3500,"posted_at":"2025-07-01","enabled":True,"skills":[{"name":"Node.js","level":"High"},{"name":"MongoDB","level":"Medium"}]},
        {"title":"Frontend Developer","description":"Develop client-side applications.","company_name":"Creative Solutions","country":"USA","salary":2800,"posted_at":"2025-08-10","enabled":True,"skills":[{"name":"React","level":"High"},{"name":"JavaScript","level":"Advanced"}]},
        {"title":"Cloud Engineer","description":"Design and implement cloud solutions.","company_name":"Cloud World","country":"Germany","salary":6000,"posted_at":"2026-09-05","enabled":True,"skills":[{"name":"AWS","level":"High"},{"name":"Terraform","level":"Medium"}]},
        {"title":"Cybersecurity Analyst","description":"Protect systems and data from cyber threats.","company_name":"SecureTech","country":"Australia","salary":4000,"posted_at":"2025-10-01","enabled":False,"skills":[{"name":"Network Security","level":"High"},{"name":"Penetration Testing","level":"Medium"}]}
    ]

    #######################################
    ## 1. Create a job posting service   ##
    #######################################
    
    # Create a normal job
    def test_job_creation(self):
        job_data = self.job_valid_examples[0]
        response = self.client.post('/jobs', json=job_data)
        
        try: 
            self.assertIn('id', f"'id' not found in response body: {response.json}")
            self.assertEqual(response.status_code, 201)
        except AssertionError:
            print(f"Failed test: {response.json}")
            raise
    
    # Create all jobs
    def test_create_all_job(self):
        for job_data in self.job_valid_examples:
            job_data = random.choice(self.job_valid_examples).copy()
            response = self.client.post('/jobs', json=job_data)
            try: 
                self.assertIn('id', f"'id' not found in response body: {response.json}")
                self.assertEqual(response.status_code, 201)
            except AssertionError:
                print(f"Failed test: {response.json}")
                raise
    
    # I create a job without title
    def test_job_bad_creation(self):
        job_data = random.choice(self.job_valid_examples).copy()
        job_data.pop("title", None)  # Remove title to simulate a bad request
        response = self.client.post('/jobs', json=job_data)
        try:
            self.assertEqual(response.status_code, 400)
        except AssertionError:
            print(f"Failed test: {response.json}")
            raise
    
    # I create a job with a bad skill
    def test_job_bad_skill_creation(self):
        job_data = deepcopy(random.choice(self.job_valid_examples))  # Copia profunda
        job_data['skills'][0] = [{"nombre":"debria fallar","nivel":"altamente"}]  # Invalid skill format
        response = self.client.post('/jobs', json=job_data)
        try:
            self.assertEqual(response.status_code, 400)
        except AssertionError:
            print(f"Failed test: {response.json}")
            raise

    # Create new Skill and use in another job
    def test_job_existing_skill(self):
        response1 = self.client.post('/jobs', json=random.choice(self.job_valid_examples))
        try:
            self.assertEqual(response1.status_code, 201)
        except AssertionError:
            print(f"Failed test: {response1.json}")
            raise

        idSkill = response1.json['skills'][0]['id']

        job_data = random.choice(self.job_valid_examples).copy()
        job_data['skills'] = [{ "id": idSkill }]  # Reuse the existing skill
        response2 = self.client.post('/jobs', json=job_data)
        try:
            self.assertEqual(response2.status_code, 201)
        except AssertionError:
            print(f"Failed test: {response2.json}")
            raise
    
    # Create a job with the id of a skill that does not exist
    def test_job_not_existing_skill(self):
        job_data = random.choice(self.job_valid_examples).copy()
        job_data['skills'] = [{ "id": 9999 }]  # ID not exist
        response2 = self.client.post('/jobs', json=job_data)
        try:
            self.assertEqual(response2.status_code, 404)
        except AssertionError:
            print(f"Failed test: {response2.json}")
            raise



    #######################################
    ## 2. Create a job-searching service ##
    #######################################
  
    # Get 0 jobs
    def test_get_jobs(self):
        response = self.client.get('/jobs?external_source=false')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['pagination']['total'], 0,f"Failed test: {response.json}")

            
    # Create a normal job and get
    def test_job_get(self):
        self.client.post('/jobs', json=random.choice(self.job_valid_examples))
        response = self.client.get('/jobs?external_source=false')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['pagination']['total'], 1, f"Failed test: {response.json}")

    
    # Create many jobs and get
    def test_job_get_multiple(self):
        for _ in range(3):
            response = self.client.post('/jobs', json=random.choice(self.job_valid_examples))
            try:
                self.assertEqual(response.status_code, 201)
            except AssertionError:
                print(f"Failed test: {response.json}")
                raise
        response = self.client.get('/jobs?external_source=false')
        try:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['pagination']['total'], 3)
        except AssertionError:
            print(f"Failed test: {response.json}")
            raise
    
    # Create up to 10 jobs and get
    def test_job_get_up_10(self):
        for job in  self.job_valid_examples:
            response = self.client.post('/jobs', json=job)
            try:
                self.assertEqual(response.status_code, 201)
            except AssertionError:
                print(f"Failed test: {response.json}")
                raise
        response = self.client.get('/jobs?external_source=false')
        try:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['pagination']['total'], 11)
        except AssertionError:
            print(f"Failed test: {response.json}")
            raise
    
    # Get pag 2
    def test_job_get_pag2(self):
        for job in  self.job_valid_examples:
            response = self.client.post('/jobs', json=job)
            try:
                self.assertEqual(response.status_code, 201)
            except AssertionError:
                print(f"Failed test: {response.json}")
                raise
        response = self.client.get('/jobs',query_string={'external_source':'false','page': 2})
        try:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['pagination']['total'], 11)
        except AssertionError:
            print(f"Failed test: {response.json}")
            raise

    # Search simple
    def test_job_search(self):
        for job in  self.job_valid_examples:
            response = self.client.post('/jobs', json=job)
            try:
                self.assertEqual(response.status_code, 201)
            except AssertionError:
                print(f"Failed test: {response.json}")
                raise
        # One of the descriptions has the word "ESENCIA" to facilitate unit testing.
        response = self.client.get('/jobs',query_string={'external_source':'false', 'search': 'ESENCIA'})
        
        try:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['pagination']['total'], 1)
        except AssertionError:
            print(f"Failed test: {response.json}")
            raise

    def test_job_filters(self):
        for job in self.job_valid_examples:
            response = self.client.post('/jobs', json=job)
            try:
                self.assertEqual(response.status_code, 201)
            except AssertionError:
                print(f"Failed to create job: {response.json}")
                raise

        # Cases test for each filter
        test_cases = [
            # Test description filter
            {'filter': {'search': 'QA'}, 'expected_total': 1, 'description': 'Search by description keyword'},
            # Test posted_after filter
            {'filter': {'posted_after': '2026-01-01'}, 'expected_total': 1, 'description': 'Search by posted date'},
            # Test salary range filter (minimum salary)
            {'filter': {'salary_min': 4000}, 'expected_total': 5, 'description': 'Search by minimum salary'},
            # Test salary range filter (maximum salary)
            {'filter': {'salary_max': 3000}, 'expected_total': 5, 'description': 'Search by maximum salary'},
            # Test company name filter
            {'filter': {'company_name': 'Tech Solutions Inc.'}, 'expected_total': 4, 'description': 'Search by company name'},
            # Test country filter
            {'filter': {'country': 'Argentina'}, 'expected_total': 4, 'description': 'Search by country'},
            # Test skills filter (single skill)
            {'filter': {'skills': ['Python']}, 'expected_total': 2, 'description': 'Search by single skill'},
            # Test skills filter (multiple skills)
            # I get two jobs, one that requires react and another that requires AWS (according to my list)
            {'filter': {'skills': ['React', 'AWS']}, 'expected_total': 2, 'description': 'Search by multiple skills'},
            # Test skills filter (multiple skills)
            # I get one jobs, one that requires react and Javascript (according to my list)
            {'filter': {'skills': ['React', 'Javascript']}, 'expected_total': 1, 'description': 'Search by multiple skills one job'},
        ]
        
        # Run each test
        for test in test_cases:
            query = {**test['filter'], 'external_source': 'false'}
            response = self.client.get('/jobs', query_string=query)
            try:
                self.assertEqual(response.status_code, 200, f"Failed {test['description']}: Status code mismatch.")
                self.assertEqual(response.json['pagination']['total'], test['expected_total'], f"Failed {test['description']}: Total mismatch.")
            except AssertionError:
                print(f"Failed test: {test['description']}\nResponse: {response.json}")
                raise

        # Test combinado de filtros
        combined_filters = {
            'search': 'Engineer',
            'posted_after': '2026-01-01',
            'salary_min': 5000,
            'salary_max': 1000000000,
            'company_name': 'Cloud World',
            'country': 'Germany',
            'skills': ['AWS', 'Terraform']
        }
        query  = {**combined_filters, 'external_source': 'false'}
        response = self.client.get('/jobs', query_string=query)
        try:
            self.assertEqual(response.status_code, 200, "Failed combined filters: Status code mismatch.")
            self.assertEqual(response.json['pagination']['total'], 1, "Failed combined filters: Total mismatch.")
        except AssertionError:
            print(f"Failed combined filters\nResponse: {response.json}")
            raise


    #######################################
    ## 4. Create additional sources      ##
    #######################################
    
    # Get 42 extra soruce jobs
    def test_get_jobs_extra_source(self):
        response = self.client.get('/jobs')
        try: 
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['pagination']['total'], 42)
        except AssertionError:
            print(f"Failed test: {response.json}")
            raise
    
    # get page 4, creating only 11 elements, if the extra source should be only 3 pages with 11 elements, but now it should be 6 pages with 53 (11+42) elements
    def test_job_get_pag2_extra_source(self):
        # Create 11 jobs
        for job in self.job_valid_examples:
            response = self.client.post('/jobs', json=job)
            try:
                self.assertEqual(response.status_code, 201)
            except AssertionError:
                print(f"Failed test: {response.json}")
                raise
        
        response = self.client.get('/jobs',query_string={'page': 4})
        try:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['pagination']['total'], 53)
            self.assertEqual(response.json['pagination']['pages'], 6)
        except AssertionError:
            print(f"Failed test: {response.json}")
            raise

    # Search simple with external sources
    def test_job_search(self):
        for job in  self.job_valid_examples:
            response = self.client.post('/jobs', json=job)
            try:
                self.assertEqual(response.status_code, 201)
            except AssertionError:
                print(f"Failed test: {response.json}")
                raise

        # Java 4 = 3 external + 1 in db  
        response = self.client.get('/jobs',query_string={'search': 'Java'})
        
        try:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['pagination']['total'], 4)
            
            # Validate  3 external + 1 in db  
            externalJobs=0
            localJobs=0
            for job in response.json['jobs']:
                if job['external'] == 'jobberwocky-extra-source-v2':
                    externalJobs+=1
                elif job['external'] == 'local':
                    localJobs+=1

            self.assertEqual(externalJobs, 3)
            self.assertEqual(localJobs, 1)

        except AssertionError:
            print(f"Failed test: {response.json}")
            raise

    def test_job_filters_external_source(self):
        for job in self.job_valid_examples:
            response = self.client.post('/jobs', json=job)
            try:
                self.assertEqual(response.status_code, 201)
            except AssertionError:
                print(f"Failed to create job: {response.json}")
                raise

        # Cases test for each filter
        test_cases = [
            # Test description filter
            {'filter': {'search': 'QA'}, 'expected_total': 1, 'description': 'Search by description keyword with external source'},
            # Test posted_after filter
            {'filter': {'posted_after': '2026-01-01'}, 'expected_total': 43, 'description': 'Search by posted date with external source'},
            # Test salary range filter (minimum salary)
            {'filter': {'salary_min': 50000}, 'expected_total': 21, 'description': 'Search by minimum salary with external source'},
            # Test salary range filter (maximum salary)
            {'filter': {'salary_max': 3000}, 'expected_total': 5, 'description': 'Search by maximum salary with external source'},
            # Test company name filter
            {'filter': {'company_name': 'Tech Solutions Inc.'}, 'expected_total': 4, 'description': 'Search by company name with external source'},
            # Test country filter
            {'filter': {'country': 'Argentina'}, 'expected_total': 21, 'description': 'Search by country with external source'},
            # Test skills filter (single skill)
            {'filter': {'skills': ['Python']}, 'expected_total': 6, 'description': 'Search by single skill with external source'},
            # Test skills filter (multiple skills)
            # I get two jobs, one that requires react and another that requires AWS 
            {'filter': {'skills': ['React', 'AWS']}, 'expected_total': 5, 'description': 'Search by multiple skills with external source'},
            # Test skills filter (multiple skills)
            # Get jobs with skills react and Javascript is repeated in some places and not in others  
            {'filter': {'skills': ['React', 'Javascript']}, 'expected_total': 3, 'description': 'Search by multiple job with external source'},
        ]
        
        # Run each test
        for test in test_cases:
            response = self.client.get('/jobs', query_string=test['filter'])
            try:
                self.assertEqual(response.status_code, 200, f"Failed {test['description']}: Status code mismatch.")
                self.assertEqual(response.json['pagination']['total'], test['expected_total'], f"Failed {test['description']}: Total mismatch.")
            except AssertionError:
                print(f"Response: {response.json}")
                raise

        # Test combinado de filtros
        combined_filters = {
            'search': 'Engineer',
            'posted_after': '2026-01-01',
            'salary_min': 5000,
            'salary_max': 1000000000,
            'company_name': 'Cloud World',
            'country': 'Germany',
            'skills': ['AWS', 'Terraform']
        }
       
        response = self.client.get('/jobs', query_string=combined_filters)
        try:
            self.assertEqual(response.status_code, 200, "Failed combined filters: Status code mismatch with external source.")
            self.assertEqual(response.json['pagination']['total'], 1, "Failed combined filters with external source: Total mismatch.")
        except AssertionError:
            print(f"Response: {response.json}")
            raise
        