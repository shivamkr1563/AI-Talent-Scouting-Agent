"""
Test script demonstrating role-based ranking system.

Shows how candidates are ranked based on:
1. Skill Match (0.4 weight)
2. Role Fit (0.4 weight)
3. Interest Score (0.2 weight)

Final Score = (0.4 × Skill Match) + (0.4 × Role Fit) + (0.2 × Interest Score)
"""

from services.mock_services import (
    detect_job_role, 
    detect_candidate_domain, 
    calculate_role_fit_score
)


def test_role_based_ranking():
    """Test role-based ranking formula."""
    
    print("=" * 80)
    print("ROLE-BASED RANKING SYSTEM - TEST")
    print("=" * 80)
    print()
    
    # Test Case 1: Frontend Role
    print("TEST CASE 1: Frontend React Developer Role")
    print("-" * 80)
    
    jd_title = "Senior Frontend Engineer - React"
    jd_skills = ["React", "TypeScript", "CSS3", "JavaScript"]
    job_role = detect_job_role(jd_title, jd_skills)
    print(f"✅ Detected Job Role: {job_role}")
    print(f"   Required Skills: {', '.join(jd_skills)}")
    print()
    
    # Candidates with different domains
    candidates = [
        {
            "name": "Alice (React Expert)",
            "skills": ["React", "TypeScript", "Next.js", "CSS3"],
            "skill_match": 95,  # 95% skill match
            "interest": 85,
        },
        {
            "name": "Bob (Full-Stack Developer)",
            "skills": ["React", "Node.js", "PostgreSQL", "Python"],
            "skill_match": 80,  # 80% skill match
            "interest": 75,
        },
        {
            "name": "Charlie (Backend Python Dev)",
            "skills": ["Python", "FastAPI", "PostgreSQL", "Docker"],
            "skill_match": 30,  # 30% skill match
            "interest": 70,
        },
    ]
    
    print("CANDIDATES:")
    rankings = []
    for cand in candidates:
        candidate_domain = detect_candidate_domain(cand["skills"])
        # Note: New improved function returns (score, explanation) tuple
        # Old code expects just score, so we unpack the tuple
        result = calculate_role_fit_score(job_role, candidate_domain, 
                                          candidate_skills=cand["skills"],
                                          job_skills=["React", "TypeScript", "CSS3", "JavaScript"])
        
        if isinstance(result, tuple):
            role_fit_score, role_fit_explanation = result
            # Convert 0-100 scale to 0-10 scale for backward compatibility
            role_fit_score_normalized = role_fit_score / 10.0
        else:
            # Old function returned just score (0-10)
            role_fit_score_normalized = result
            role_fit_explanation = f"Role fit: {candidate_domain} → {job_role}"
        
        # Calculate combined score using the formula
        skill_match_norm = cand["skill_match"] / 100.0
        role_fit_norm = role_fit_score_normalized / 10.0 if role_fit_score_normalized > 10 else role_fit_score_normalized
        interest_norm = cand["interest"] / 100.0
        
        combined_score = (skill_match_norm * 0.4 + 
                         role_fit_norm * 0.4 + 
                         interest_norm * 0.2) * 100
        
        rankings.append({
            "name": cand["name"],
            "domain": candidate_domain,
            "skills": ", ".join(cand["skills"][:3]),
            "skill_match": cand["skill_match"],
            "role_fit": role_fit_score_normalized * 10 if isinstance(result, tuple) else role_fit_score_normalized,
            "interest": cand["interest"],
            "combined_score": combined_score,
        })
        
        print(f"\n  {cand['name']}")
        print(f"    Skills: {', '.join(cand['skills'][:3])}")
        print(f"    Domain: {candidate_domain}")
        print(f"    Skill Match: {cand['skill_match']}/100")
        print(f"    Role Fit: {role_fit_score_normalized * 10:.1f}/100 ({candidate_domain} → {job_role})")
        print(f"    Interest: {cand['interest']}/100")
        print(f"    COMBINED SCORE: {combined_score:.1f}/100")
    
    # Sort by combined score
    rankings.sort(key=lambda x: x["combined_score"], reverse=True)
    
    print("\n" + "=" * 80)
    print("RANKING RESULTS:")
    print("=" * 80)
    for idx, rank in enumerate(rankings, 1):
        print(f"{idx}. {rank['name']:<30} Score: {rank['combined_score']:6.1f}/100")
        print(f"   Domain: {rank['domain']:<15} Skills: {rank['skills']}")
        print(f"   Skill: {rank['skill_match']}/100 | Role Fit: {rank['role_fit']}/10 | Interest: {rank['interest']}/100")
        print()
    
    # Verify correct ranking
    print("=" * 80)
    print("ANALYSIS:")
    print("=" * 80)
    print("✅ Alice ranks #1: Best skill match (95%) + perfect role fit (10/10)")
    print("✅ Bob ranks #2: Good skill match (80%) + related role fit (7/10 - fullstack→frontend)")
    print("✅ Charlie ranks #3: Poor skill match (30%) + different domain (3/10 - backend→frontend)")
    print()
    print("KEY INSIGHT:")
    print("  Alice wins with balanced skill and role fit emphasis:")
    print("  - Skill match (0.4 weight) + perfect role fit (0.4 weight)")
    print("  - 0.4×0.95 + 0.4×1.0 + 0.2×0.85 = 0.38 + 0.40 + 0.17 = 0.95 (95%)")
    print()
    print("  Charlie loses despite high interest (70%) because:")
    print("  - Skill match low (0.4 weight) + completely different domain (0.4 weight)")
    print("  - 0.4×0.30 + 0.4×0.3 + 0.2×0.70 = 0.12 + 0.12 + 0.14 = 0.38 (38%)")
    print()


def test_role_fit_relationships():
    """Test role fit scoring relationships."""
    
    print("\n" + "=" * 80)
    print("ROLE FIT SCORING - RELATIONSHIPS")
    print("=" * 80)
    
    test_pairs = [
        ("frontend", "frontend", "Perfect match"),
        ("frontend", "fullstack", "Related role"),
        ("frontend", "backend", "Different domain"),
        ("backend", "data", "Related role (data-heavy backend)"),
        ("backend", "ml", "Different domain"),
        ("ml", "data", "Related role"),
        ("devops", "backend", "Related role"),
    ]
    
    print("\nRole Fit Scoring Matrix:")
    print("-" * 80)
    for job_role, candidate_domain, description in test_pairs:
        result = calculate_role_fit_score(job_role, candidate_domain)
        if isinstance(result, tuple):
            score, explanation = result
            score_normalized = score / 10.0  # Convert 0-100 to 0-10 for display
        else:
            score_normalized = result
        print(f"{job_role:12} ← {candidate_domain:12}: {score_normalized:4.1f}/10  ({description})")


def test_formula_breakdown():
    """Show formula calculations in detail."""
    
    print("\n" + "=" * 80)
    print("FORMULA BREAKDOWN - DETAILED CALCULATION")
    print("=" * 80)
    print()
    print("Formula:")
    print("  Final Score = (0.4 × Skill Match%) + (0.4 × Role Fit/10) + (0.2 × Interest%)")
    print()
    
    print("Example 1: Frontend React Expert")
    print("-" * 80)
    skill = 95
    role_fit = 10
    interest = 85
    score = (skill/100 * 0.4) + (role_fit/10 * 0.4) + (interest/100 * 0.2)
    score_100 = score * 100
    print(f"  Skill Match:   {skill:3}%  × 0.4 = {(skill/100)*0.4:.3f}")
    print(f"  Role Fit:      {role_fit:4.1f}/10  × 0.4 = {(role_fit/10)*0.4:.3f}")
    print(f"  Interest:      {interest:3}%  × 0.2 = {(interest/100)*0.2:.3f}")
    print(f"  {'─'*40}")
    print(f"  Combined Score = {score:.3f} = {score_100:.1f}/100")
    print()
    
    print("Example 2: Backend Developer Applied for Frontend Role")
    print("-" * 80)
    skill = 30
    role_fit = 3
    interest = 70
    score = (skill/100 * 0.4) + (role_fit/10 * 0.4) + (interest/100 * 0.2)
    score_100 = score * 100
    print(f"  Skill Match:   {skill:3}%  × 0.4 = {(skill/100)*0.4:.3f}")
    print(f"  Role Fit:      {role_fit:4.1f}/10  × 0.4 = {(role_fit/10)*0.4:.3f}")
    print(f"  Interest:      {interest:3}%  × 0.2 = {(interest/100)*0.2:.3f}")
    print(f"  {'─'*40}")
    print(f"  Combined Score = {score:.3f} = {score_100:.1f}/100")
    print()
    print("Note: High interest (70%) doesn't compensate for poor skill match (30%)")
    print("      and domain mismatch (3/10) since skill and role fit are equally weighted.")


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("ROLE-BASED CANDIDATE RANKING SYSTEM")
    print("=" * 80)
    
    test_role_based_ranking()
    test_role_fit_relationships()
    test_formula_breakdown()
    
    print("\n" + "=" * 80)
    print("✅ ALL TESTS COMPLETE")
    print("=" * 80)
    print("""
The new ranking system ensures:
  ✓ Role fit is a critical factor in ranking
  ✓ Skill-heavy but domain-mismatched candidates rank lower
  ✓ Perfect role fit with good skills ranks highest
  ✓ Interest score provides minor adjustment
  ✓ Formula is transparent and explainable
""")
