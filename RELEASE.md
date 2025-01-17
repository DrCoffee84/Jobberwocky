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