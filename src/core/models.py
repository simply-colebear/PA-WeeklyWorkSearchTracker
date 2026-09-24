
from sqlalchemy import (
    Column, Integer, String, DateTime, Text, ForeignKey,
    Numeric, Date, Boolean, Table, event
)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

# Association table for many-to-many between jobs and employers
job_employer_tags = Table(
    'job_employer_tags', Base.metadata,
    Column('job_id', ForeignKey('jobs.id'), primary_key=True),
    Column('tag_id', ForeignKey('tags.id'), primary_key=True)
)

class Job(Base):
    """Primary application record"""
    __tablename__ = 'jobs'
    
    id = Column(Integer, primary_key=True)
    employer_id = Column(Integer, ForeignKey('employers.id'), nullable=False)
    
    # Application metadata
    application_date = Column(Date, nullable=False, index=True)
    position_title = Column(String(200))
    job_url = Column(String(500))
    source_platform = Column(String(100))  # LinkedIn, Indeed, etc.
    
    # Status tracking
    status = Column(String(50), default='applied')  # applied, interview, rejected, hired
    contact_name = Column(String(100))
    contact_email = Column(String(200))
    contact_phone = Column(String(20))
    
    # Results tracking for UC form
    how_applied = Column(String(100))  # online, email, in-person
    results = Column(Text)  # outcome notes
    
    # Week association for UC reports
    week_start = Column(Date, nullable=False, index=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    employer = relationship('Employer', back_populates='jobs')
    tags = relationship('Tag', secondary=job_employer_tags, backref='jobs')
    
    def to_uc_form_dict(self):
        """Format as PA UC form expects"""
        return {
            'date': self.application_date.isoformat(),
            'employer': self.employer.name,
            'contact_name': self.contact_name or '',
            'contact_phone': self.contact_phone or '',
            'how_applied': self.how_applied or 'online',
            'results': self.results or ''
        }

class Employer(Base):
    """Employer master record with smart matching"""
    __tablename__ = 'employers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), unique=True, nullable=False, index=True)
    normalized_name = Column(String(200), index=True)  # lowercase, no punctuation
    website = Column(String(500))
    industry = Column(String(100))
    location = Column(String(200))
    is_verified = Column(Boolean, default=False)
    
    jobs = relationship('Job', back_populates='employer')
    tags = relationship('Tag', secondary='employer_tags')
    
    @staticmethod
    def normalize(text):
        """Standardize for fuzzy matching"""
        import re
        text = text.lower().strip()
        text = re.sub(r'[^a-z0-9\s]', '', text)
        text = re.sub(r'\s+', ' ', text)
        return text

class Tag(Base):
    """Industry/company categorization"""
    __tablename__ = 'tags'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    category = Column(String(50))  # industry, size, location_type
    
class UserConfig(Base):
    """Store user preferences for mapping automation"""
    __tablename__ = 'user_config'
    
    id = Column(Integer, primary_key=True)
    key = Column(String(100), unique=True)
    value = Column(Text)
    updated_at = Column(DateTime, default=datetime.utcnow)
