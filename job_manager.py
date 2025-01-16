from flask import Flask, request, jsonify

app = Flask(__name__)

jobs = []

@app.route('/jobs', methods=['POST'])
def create_job():
    job_data = request.json
    job = {
        'id': len(jobs) + 1,
        'title': job_data['title'],
        'description': job_data['description']
    }
    jobs.append(job)
    return jsonify(job), 201

if __name__ == '__main__':
    app.run(debug=True)