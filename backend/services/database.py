import sqlite3
import json
import os
from datetime import datetime
from typing import Optional, List
from contextlib import contextmanager


DB_PATH = os.path.join(os.path.dirname(__file__), "../data/talent_scout.db")


class CandidateDatabase:
    """SQLite database for persistent candidate storage and retrieval."""
    
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_db()
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def _init_db(self):
        """Initialize database schema."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Candidates table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS candidates (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    title TEXT NOT NULL,
                    skills TEXT NOT NULL,
                    experience_years INTEGER,
                    location TEXT,
                    summary TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Job Descriptions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS job_descriptions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    company TEXT NOT NULL,
                    description TEXT NOT NULL,
                    parsed_data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Scoring Results table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS scoring_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    jd_id INTEGER NOT NULL,
                    candidate_id INTEGER NOT NULL,
                    match_score INTEGER,
                    match_breakdown TEXT,
                    interest_score INTEGER,
                    interest_breakdown TEXT,
                    conversation TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (jd_id) REFERENCES job_descriptions(id),
                    FOREIGN KEY (candidate_id) REFERENCES candidates(id)
                )
            """)
            
            # Agent Runs table (for analytics)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS agent_runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    jd_id INTEGER NOT NULL,
                    total_time_seconds FLOAT,
                    candidates_processed INTEGER,
                    errors_count INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (jd_id) REFERENCES job_descriptions(id)
                )
            """)
            
            conn.commit()
    
    def add_candidate(self, name: str, title: str, skills: list, 
                     experience_years: int = None, location: str = None, 
                     summary: str = None) -> int:
        """Add or update a candidate."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO candidates 
                (name, title, skills, experience_years, location, summary, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (name, json.dumps(skills), json.dumps(skills), experience_years, 
                  location, summary, datetime.utcnow().isoformat()))
            conn.commit()
            return cursor.lastrowid
    
    def get_all_candidates(self) -> List[dict]:
        """Retrieve all candidates."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM candidates ORDER BY name")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def get_candidate(self, candidate_id: int) -> Optional[dict]:
        """Get a single candidate by ID."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM candidates WHERE id = ?", (candidate_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def save_jd(self, title: str, company: str, description: str, 
                parsed_data: dict = None) -> int:
        """Save job description."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO job_descriptions 
                (title, company, description, parsed_data)
                VALUES (?, ?, ?, ?)
            """, (title, company, description, json.dumps(parsed_data) if parsed_data else None))
            conn.commit()
            return cursor.lastrowid
    
    def save_scoring_result(self, jd_id: int, candidate_id: int, 
                           match_score: int, match_breakdown: dict,
                           interest_score: int, interest_breakdown: dict,
                           conversation: list) -> int:
        """Save scoring result for a candidate against a JD."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO scoring_results
                (jd_id, candidate_id, match_score, match_breakdown, 
                 interest_score, interest_breakdown, conversation)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (jd_id, candidate_id, match_score, json.dumps(match_breakdown),
                  interest_score, json.dumps(interest_breakdown), json.dumps(conversation)))
            conn.commit()
            return cursor.lastrowid
    
    def get_jd_results(self, jd_id: int) -> List[dict]:
        """Get all scoring results for a JD."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT sr.*, c.name, c.title 
                FROM scoring_results sr
                JOIN candidates c ON sr.candidate_id = c.id
                WHERE sr.jd_id = ?
                ORDER BY sr.match_score DESC
            """, (jd_id,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def save_agent_run(self, jd_id: int, total_time: float, 
                      candidates_count: int, errors_count: int) -> int:
        """Record agent execution metrics."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO agent_runs
                (jd_id, total_time_seconds, candidates_processed, errors_count)
                VALUES (?, ?, ?, ?)
            """, (jd_id, total_time, candidates_count, errors_count))
            conn.commit()
            return cursor.lastrowid
    
    def get_stats(self) -> dict:
        """Get database statistics."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as count FROM candidates")
            total_candidates = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM job_descriptions")
            total_jds = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM agent_runs")
            total_runs = cursor.fetchone()['count']
            
            return {
                "total_candidates": total_candidates,
                "total_job_descriptions": total_jds,
                "total_agent_runs": total_runs
            }


# Global instance
db = CandidateDatabase()
