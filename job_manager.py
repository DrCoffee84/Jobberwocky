from flask import Flask, request, jsonify

app = Flask(__name__)

# First will save jobs in memory 
jobs = []

@app.route('/jobs', methods=['POST'])
def create_job():
    job_data = request.json
    required_fields = ['title', 'description', 'company_name', 'country', 'salary', 'posted_at', 'enabled', 'skills']
    if not all(field in job_data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400 # bad request

    # Preparar el job con un id único basado en el número de jobs existentes
    new_job = {
        'id': len(jobs) + 1,
        'title': job_data['title'],
        'description': job_data['description'],
        'company_name': job_data['company_name'],
        'country': job_data['country'],
        'salary': job_data['salary'],
        'posted_at': job_data['posted_at'],
        'enabled': job_data['enabled'],
        'skills': job_data['skills']  # 'skills' is still to be validated. 
    }

    jobs.append(new_job)
    return jsonify(new_job), 201 #  create

if __name__ == '__main__':
    app.run(debug=True)