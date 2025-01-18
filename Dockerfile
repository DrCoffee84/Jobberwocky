# Use the official Python image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the application code
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Set the FLASK_APP environment variable
ENV FLASK_APP=job_manager.py

# Set URL to avatureexternaljobs
ENV URL_EXTERNAL_SOURCE='avatureexternaljobs:8080'

# Expose the port the app runs on
EXPOSE 3000

# Run the Flask server
CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]