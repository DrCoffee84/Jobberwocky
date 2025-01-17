# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    posted_at = db.Column(db.String(10), nullable=False)
    enabled = db.Column(db.Boolean, nullable=False)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Skill(db.Model):
    __tablename__ = 'skills'
    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(50),  nullable=False)
    level = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class JobSkill(db.Model):
    __tablename__ = 'job_skill'
    id = db.Column(db.Integer, primary_key=True)  
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'), nullable=False)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}