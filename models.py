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
    external = None

    # Relationship to JobSkill 
    job_skills = db.relationship('JobSkill', backref='job', lazy='joined')

    def to_dict(self):
        job_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}

        # Include skills in the dictionary with full structure
        job_dict['skills'] = [
            {
                'id': skill.skill.id,
                'name': skill.skill.name,
                'level': skill.skill.level
            } for skill in self.job_skills
        ]
    
        # Set a default value for 'external' if not set
        job_dict['external'] = self.external if self.external else "local"  # Default to 'local' if not set
    
        return job_dict

class Skill(db.Model):
    __tablename__ = 'skills'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    level = db.Column(db.String(20), nullable=False)

    # Relationship to JobSkill
    job_skills = db.relationship('JobSkill', backref='skill', lazy='joined')  

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    

class JobSkill(db.Model):
    __tablename__ = 'job_skill'
    id = db.Column(db.Integer, primary_key=True)  
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'), nullable=False)