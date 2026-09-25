from rapidfuzz import fuzz, process
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
import re

class EmployerMatcher:
    """Auto-match new employers to existing records"""
    
    def __init__(self, db_url='sqlite:///data/raw/job_tracker.db'):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        
    def normalize(self, text):
        """Standardize employer name for comparison"""
        text = text.lower().strip()
        text = re.sub(r'\b(llc|inc|corp|limited|ltd|co|company)$', '', text)
        text = re.sub(r'[^a-z0-9\s]', '', text)
        return re.sub(r'\s+', ' ', text).strip()
    
    def find_similar_employer(self, candidate_name, threshold=85):
        """Find best matching employer from database"""
        with self.Session() as session:
            candidates = [emp.normalized_name for emp in session.execute(
                select(Employer)
            ).scalars()]
            
            if not candidates:
                return None, 0
            
            match, score = process.extractOne(
                self.normalize(candidate_name),
                candidates,
                scorer=fuzz.WRatio
            )
            
            if score >= threshold:
                employer = session.execute(
                    select(Employer).where(
                        Employer.normalized_name == match
                    )
                ).scalar_one()
                return employer, score
            
            return None, score
    
    def auto_tag_employer(self, employer_name):
        """Auto-assign industry/location tags based on known patterns"""
        industry_keywords = {
            'technology': ['soft', 'tech', 'cloud', 'dev', 'saas', 'ai'],
            'insurance': ['insur', 'claim', 'underwrit', 'actuarial'],
            'retail': ['store', 'shop', 'merchant', 'retail'],
            'healthcare': ['hospital', 'clinic', 'med', 'health'],
        }
        
        normalized = self.normalize(employer_name)
        detected = []
        
        for category, keywords in industry_keywords.items():
            if any(kw in normalized for kw in keywords):
                detected.append(category)
        
        return detected

# Usage example
matcher = EmployerMatcher()
employer, confidence = matcher.find_similar_employer("Erie Insurance Group")
if confidence > 85:
    print(f"Matched to existing employer with {confidence}% confidence")