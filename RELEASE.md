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

# Docker

Build
```bash
docker build -t jobberwocky .
```

Run
```bash
docker run --name jobberwocky-container -p 8080:3000 jobberwocky
```

Run from registry 
```bash
docker run --name jobberwocky-container -p 8080:3000 avature/jobberwocky:latest
```

# Dev 
Kustomize was chosen to manage Kubernetes resources in a clean and organized manner. Ideally, these resources would be automatically created with the necessary configurations for the project. Currently, the configurations are located in the gitops folder, but in an ideal setup, these would be in a separate repository to avoid confusing end users. This would ensure that only advanced teams with knowledge of the project's setup would have access to configure these resources.

Additionally, the pipeline is set up in the .github/workflows directory, with a CI pipeline defined in ci-pipeline.yml to automate the deployment process.

A script for post-deployment testing should also be created, but since this goes beyond the scope of the current exercise, it has not been implemented yet.