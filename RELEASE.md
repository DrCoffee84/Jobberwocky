# Local

First set the Flask app name:

In linux:
```bash
export FLASK_APP=job_manager.py
```

In Windows:
```powershell
set FLASK_APP=job_manager.py
$env:FLASK_APP = "job_manager.py"
```


For local execution, run:
```bash 
flask run
```

For unit test:
```bash
python -m unittest discover tests
```

If you want to put an external service to get more jobs you must perform the build and run
```bash
git clone https://github.com/avatureta/jobberwocky-extra-source-v2.git
cd jobberwocky-extra-source-v2
docker build . -t avatureexternaljobs
docker run -p 8081:8080 avatureexternaljobs
```

# Docker

Build
```bash
docker build -t jobberwocky .
```

Run local
```bash
docker run --name jobberwocky-container --rm -p 8080:3000 jobberwocky
```

Run local with external soruce
```bash
docker network create job_network
docker run --name avatureexternaljobs --rm --network job_network -p 8081:8080 avatureexternaljobs
docker run --name jobberwocky-container --rm  --network job_network -p 8080:3000 jobberwocky
```

Run from registry 
```bash
docker run --name jobberwocky-container --rm -p 8080:3000 avature/jobberwocky:latest
```

# To test 
```bash
 curl -X POST http://localhost:8080/jobs -H "Content-Type: application/json" -d '{"title":"Devops","description":"Responsible for designing, implementing, and maintaining infrastructure automation. ESENCIA","company_name":"Tech Solutions Inc.","country":"Argentina","salary":1000000000,"posted_at":"2025-01-16","enabled":true,"skills":[{"name":"Linux","level":"High"}]}'
```
```bash
 curl -X POST http://localhost:8080/jobs -H "Content-Type: application/json" -d '{"title":"QA Engineer","description":"Test and ensure the quality of software.","company_name":"Tech Solutions Inc.","country":"Argentina","salary":1500,"posted_at":"2025-05-15","enabled":true,"skills":[{"id":1,"level":"High"},{"name":"Automation Testing","level":"Medium"}]}'
```

# Dev 
Kustomize was chosen to manage Kubernetes resources in a clean and organized manner. Ideally, these resources would be automatically created with the necessary configurations for the project. Currently, the configurations are located in the gitops folder, but in an ideal setup, these would be in a separate repository to avoid confusing end users. This would ensure that only advanced teams with knowledge of the project's setup would have access to configure these resources.

Additionally, the pipeline is set up in the .github/workflows directory, with a CI pipeline defined in `ci-pipeline.yml` to automate the deployment process.

A script for post-deployment testing should also be created, but since this goes beyond the scope of the current exercise, it has not been implemented yet.

# Prod 
For production environments, a Continuous Deployment (CD) pipeline would be used (`cd-pipeline.yml`), incorporating the Kustomize overlay for production. This pipeline would be manually triggered. Using the last successful tag to perform the deployment, this piepline can be made as complex as you want.
A script for post-deployment testing should also be created, but since this goes beyond the scope of the current exercise, it has not been implemented yet.