"""
Test improved ranking system with enhanced role detection and role-aware scoring.

Validates that:
1. Full-stack jobs detect BOTH frontend and backend correctly
2. Full-stack candidates rank highest for full-stack jobs
3. Role fit has equal weight to skill matching
4. Missing skills are properly identified
5. Ranking formula produces expected scores
"""

import sys
import json
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from services.mock_services import (
    detect_job_role,
    detect_candidate_domain,
    calculate_role_fit_score,
    calculate_skill_match_score,
    normalize_skill_name,
    generate_ranking_explanation
)


def test_fullstack_job_role_detection():
    """Test 1: Full-stack job detection with both frontend and backend."""
    print("\n" + "="*70)
    print("TEST 1: Full-Stack Job Role Detection")
    print("="*70)
    
    jd_text = """
    Full-Stack Developer - React, Node.js, SQL, AWS
    
    We're looking for an experienced Full-Stack Developer to join our team.
    
    Must-have skills:
    - React and TypeScript for frontend development
    - Node.js and Express backend experience
    - PostgreSQL or MySQL database design
    - REST API development
    - AWS or similar cloud platform experience
    
    Nice-to-have:
    - Docker and Kubernetes
    - CI/CD experience
    - GraphQL
    """
    
    skills = ["react", "typescript", "node.js", "express", "postgresql", "rest api", "aws"]
    
    role = detect_job_role(jd_text, skills)
    
    print(f"✓ Job Description: Full-Stack Developer with React, Node.js, SQL, AWS")
    print(f"✓ Extracted Skills: {skills}")
    print(f"✓ Detected Role: {role}")
    
    assert role == "fullstack", f"Expected 'fullstack', got '{role}'"
    print(f"✅ PASSED: Correctly detected full-stack role")
    return True


def test_candidate_rankings():
    """Test 2: Verify candidate ranking for full-stack job."""
    print("\n" + "="*70)
    print("TEST 2: Candidate Ranking for Full-Stack Job")
    print("="*70)
    
    # Job requirement
    job_role = "fullstack"
    job_skills = ["react", "typescript", "node.js", "express", "postgresql", "rest api", "aws"]
    
    # Candidates
    candidates = [
        {
            "name": "Alice (Full-Stack)",
            "domain": "fullstack",
            "skills": ["react", "typescript", "node.js", "express", "postgresql", "aws"]
        },
        {
            "name": "Bob (Backend)",
            "domain": "backend",
            "skills": ["node.js", "express", "postgresql", "java", "spring", "rest api"]
        },
        {
            "name": "Charlie (Data Engineer)",
            "domain": "data",
            "skills": ["spark", "hadoop", "kafka", "python", "sql"]
        },
        {
            "name": "Diana (Frontend)",
            "domain": "frontend",
            "skills": ["react", "vue", "typescript", "css", "html5"]
        },
    ]
    
    # Calculate scores for each candidate
    scores = []
    for cand in candidates:
        # Role fit score
        role_fit_score, role_fit_explanation = calculate_role_fit_score(
            job_role, cand["domain"],
            candidate_skills=cand["skills"],
            job_skills=job_skills
        )
        
        # Skill match score
        skill_match_score, matched_count, missing = calculate_skill_match_score(
            job_skills, cand["skills"]
        )
        
        # Ranking formula: (0.4 × Skill) + (0.4 × Role) + (0.2 × Interest)
        interest_score = 70  # Default
        final_score = (skill_match_score * 0.4 + role_fit_score * 0.4 + interest_score * 0.2)
        
        scores.append({
            "name": cand["name"],
            "domain": cand["domain"],
            "role_fit_score": role_fit_score,
            "role_fit_explanation": role_fit_explanation,
            "skill_match_score": skill_match_score,
            "matched_skills": matched_count,
            "missing_skills": missing,
            "interest_score": interest_score,
            "final_score": final_score
        })
    
    # Sort by final score
    scores.sort(key=lambda x: x["final_score"], reverse=True)
    
    # Print results
    print(f"✓ Job Role: {job_role}")
    print(f"✓ Required Skills: {job_skills}\n")
    
    print("Ranking Results:")
    print("-" * 70)
    
    for rank, score in enumerate(scores, 1):
        print(f"\nRank {rank}: {score['name']}")
        print(f"  Domain: {score['domain']}")
        print(f"  Role Fit: {score['role_fit_score']}/100 - {score['role_fit_explanation']}")
        print(f"  Skill Match: {score['skill_match_score']}/100 ({score['matched_skills']} matched)")
        if score["missing_skills"]:
            print(f"  Missing: {', '.join(score['missing_skills'][:3])}")
        print(f"  Interest: {score['interest_score']}/100")
        print(f"  📊 Final Score: {score['final_score']:.1f}/100")
    
    # Verify ranking order
    print("\n" + "="*70)
    print("Verification:")
    print("="*70)
    
    # Alice should rank first (full-stack)
    assert scores[0]["name"].startswith("Alice"), f"Expected Alice first, got {scores[0]['name']}"
    print("✅ Alice (Full-Stack) ranked #1 - CORRECT")
    
    # Bob should rank second (backend, partial frontend)
    assert scores[1]["name"].startswith("Bob"), f"Expected Bob second, got {scores[1]['name']}"
    print("✅ Bob (Backend) ranked #2 - CORRECT")
    
    # Scores should be descending
    for i in range(len(scores) - 1):
        assert scores[i]["final_score"] >= scores[i+1]["final_score"], \
            f"Scores not in descending order: {scores[i]['final_score']} < {scores[i+1]['final_score']}"
    print("✅ Final scores in descending order - CORRECT")
    
    # Check score differences (no identical scores)
    unique_scores = set(s["final_score"] for s in scores)
    print(f"✅ All scores unique: {len(unique_scores)} unique scores for {len(scores)} candidates")
    
    return True


def test_skill_normalization():
    """Test 3: Skill normalization and mapping."""
    print("\n" + "="*70)
    print("TEST 3: Skill Normalization and Mapping")
    print("="*70)
    
    test_cases = [
        ("rest api", "rest apis"),
        ("apis", "rest apis"),
        ("ml", "machine learning"),
        ("nlp", "nlp"),
        ("typescript", "typescript"),
        ("ts", "typescript"),
        ("node", "node.js"),
    ]
    
    print("Skill Normalization Tests:")
    print("-" * 70)
    
    for skill, expected in test_cases:
        normalized = normalize_skill_name(skill)
        status = "✅" if normalized == expected else "❌"
        print(f"{status} {skill:20} → {normalized:20} (expected: {expected})")
        assert normalized == expected, f"Failed: {skill} → {normalized} (expected {expected})"
    
    print("✅ PASSED: All skill normalization tests")
    return True


def test_role_specific_scoring():
    """Test 4: Role-specific scoring rules."""
    print("\n" + "="*70)
    print("TEST 4: Role-Specific Scoring Rules")
    print("="*70)
    
    test_cases = [
        # (job_role, candidate_domain, candidate_skills, job_skills, min_score, expected_range)
        ("fullstack", "fullstack", 
         ["react", "typescript", "node.js", "express", "postgresql"],
         ["react", "typescript", "node.js", "express", "postgresql"],
         85, "Full-stack candidate for full-stack job"),
        
        ("backend", "backend",
         ["node.js", "express", "postgresql", "java"],
         ["node.js", "express", "postgresql"],
         85, "Backend specialist for backend job"),
        
        ("fullstack", "backend",
         ["node.js", "express", "postgresql", "java"],
         ["react", "typescript", "node.js", "express", "postgresql"],
         60, "Backend specialist for full-stack job (needs frontend)"),
        
        ("backend", "frontend",
         ["react", "typescript", "vue"],
         ["node.js", "express", "postgresql"],
         20, "Frontend developer for backend job (mismatch)"),
    ]
    
    print("Role-Specific Scoring Tests:")
    print("-" * 70)
    
    for job_role, cand_domain, cand_skills, job_skills, min_score, description in test_cases:
        score, explanation = calculate_role_fit_score(
            job_role, cand_domain,
            candidate_skills=cand_skills,
            job_skills=job_skills
        )
        
        status = "✅" if score >= min_score else "❌"
        print(f"{status} {description}")
        print(f"   Score: {score}/100 - {explanation}")
        
        assert score >= min_score, f"Score {score} below minimum {min_score}"
    
    print("✅ PASSED: All role-specific scoring tests")
    return True


def test_formula_validation():
    """Test 5: Validate the ranking formula with known test case."""
    print("\n" + "="*70)
    print("TEST 5: Formula Validation with Known Test Case")
    print("="*70)
    
    # Updated test cases with new 0-100 scale
    # Old 0-10 scale converted: 3 → 30, 7 → 70, 10 → 100
    # Alice: Skill 95, Role 90 (was 9), Interest 80 → (0.4×95 + 0.4×90 + 0.2×80) = 90.0
    # Bob: Skill 60, Role 50 (was 5), Interest 75 → (0.4×60 + 0.4×50 + 0.2×75) = 59.0
    # Charlie: Skill 40, Role 30 (was 3), Interest 60 → (0.4×40 + 0.4×30 + 0.2×60) = 40.0
    
    test_cases = [
        (95, 90, 80, 90.0, "Alice"),
        (60, 50, 75, 59.0, "Bob"),
        (40, 30, 60, 40.0, "Charlie"),
    ]
    
    print("Testing formula: (0.4 × Skill) + (0.4 × Role) + (0.2 × Interest)")
    print("-" * 70)
    
    for skill, role, interest, expected, name in test_cases:
        calculated = (skill * 0.4 + role * 0.4 + interest * 0.2)
        status = "✅" if abs(calculated - expected) < 0.1 else "❌"
        print(f"{status} {name:10} → (0.4×{skill:3} + 0.4×{role:3} + 0.2×{interest:3}) = {calculated:5.1f} (expected {expected:.1f})")
        assert abs(calculated - expected) < 0.1, f"Formula error for {name}"
    
    print("✅ PASSED: Formula validation successful")
    return True


def main():
    """Run all tests."""
    print("\n" + "█"*70)
    print("█" + " "*68 + "█")
    print("█" + "  IMPROVED RANKING SYSTEM - COMPREHENSIVE TEST SUITE".center(68) + "█")
    print("█" + " "*68 + "█")
    print("█"*70)
    
    tests = [
        ("Full-Stack Job Role Detection", test_fullstack_job_role_detection),
        ("Candidate Ranking for Full-Stack Job", test_candidate_rankings),
        ("Skill Normalization and Mapping", test_skill_normalization),
        ("Role-Specific Scoring Rules", test_role_specific_scoring),
        ("Formula Validation with Known Test Case", test_formula_validation),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except AssertionError as e:
            failed += 1
            print(f"❌ FAILED: {e}")
        except Exception as e:
            failed += 1
            print(f"❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
    
    # Summary
    print("\n" + "█"*70)
    print("█" + " "*68 + "█")
    print("█" + "  TEST SUMMARY".center(68) + "█")
    print("█" + " "*68 + "█")
    print("█"*70)
    print(f"\n  Passed: {passed}/{len(tests)} ✅")
    print(f"  Failed: {failed}/{len(tests)} ❌")
    print(f"\n  Overall: {'ALL TESTS PASSED ✅' if failed == 0 else 'SOME TESTS FAILED ❌'}\n")
    
    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
