"""
Test script to debug the /run endpoint with full-stack JD
"""
import sys
import asyncio
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from routers.agent_v2 import AgentOrchestrator
from models.schemas_v2 import RunAgentRequest


async def test_fullstack_jd():
    """Test the agent with full-stack job description"""
    
    job_description = """
Full-Stack Developer - WebStartup

Needed:
- 4+ years full-stack development
- Frontend: React, Vue, or Angular
- Backend: Node.js, Python, or Java
- Databases: SQL and NoSQL
- Cloud: AWS/GCP/Azure
- Agile/Scrum experience

Location: Remote
    """
    
    print("="*70)
    print("Testing Full-Stack Developer Job Description")
    print("="*70)
    print(f"\nJob Description:\n{job_description}\n")
    
    try:
        # Create request
        request = RunAgentRequest(job_description=job_description)
        print("✅ Request created successfully")
        
        # Run orchestrator
        orchestrator = AgentOrchestrator()
        print("✅ Orchestrator created successfully")
        
        result = await orchestrator.run_agent(request)
        print("✅ Agent ran successfully!")
        
        print("\n" + "="*70)
        print("RESULTS")
        print("="*70)
        
        if result.get("parsed_jd"):
            jd = result["parsed_jd"]
            print(f"\n📋 Parsed JD:")
            print(f"   Title: {jd.get('title')}")
            print(f"   Domain: {jd.get('domain')}")
            print(f"   Skills: {jd.get('top_skills', [])}")
        
        if result.get("candidates"):
            print(f"\n👥 Candidates Found: {len(result['candidates'])}")
            for i, cand in enumerate(result['candidates'][:3], 1):
                print(f"\n   {i}. {cand.name} - Score: {cand.combined_score:.1f}/100")
                print(f"      Domain: {cand.match_breakdown.candidate_domain}")
                print(f"      Role Fit: {cand.match_breakdown.role_fit_score:.1f}/10")
                print(f"      Skill Match: {cand.match_breakdown.skill_match_score}/100")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(test_fullstack_jd())
    sys.exit(0 if success else 1)
