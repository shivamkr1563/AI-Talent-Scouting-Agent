from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from routers import agent_v2
from dotenv import load_dotenv
import logging
import sys
import os
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('logs/app.log') if os.path.exists('logs') or os.makedirs('logs', exist_ok=True) else logging.NullHandler()
    ]
)

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="AI Talent Scouting Agent",
    description="Production-grade AI agent for candidate discovery and engagement",
    version="2.0-production",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS Middleware
allowed_origins = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,http://localhost:5174,https://ai-talent-scouting-agent-zwcv.vercel.app"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in allowed_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=3600,
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catch all exceptions and return formatted error response."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": str(exc),
            "error_code": "INTERNAL_SERVER_ERROR",
            "timestamp": datetime.utcnow().isoformat(),
            "path": str(request.url),
            "details": None
        }
    )


# Include routers
app.include_router(agent_v2.router)

# Legacy v1 endpoint (backward compatibility)
@app.get("/api/legacy/status")
async def legacy_status():
    """Legacy endpoint for backward compatibility."""
    return {"status": "deprecated", "message": "Use /api/v2 endpoints instead"}


# Health check
@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "2.0-production",
        "timestamp": datetime.utcnow().isoformat()
    }


# Root endpoint
@app.get("/")
async def root():
    """API documentation and information."""
    return {
        "name": "AI Talent Scouting Agent",
        "version": "2.0-production",
        "docs": "/docs",
        "redoc": "/redoc",
        "api_base": "/api/v2",
        "endpoints": {
            "POST /api/v2/run": "Run talent scouting workflow",
            "GET /api/v2/stats": "Get system statistics",
            "GET /health": "Health check"
        }
    }


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize on startup."""
    logger.info("=" * 60)
    logger.info("🚀 AI Talent Scouting Agent - Production Edition")
    logger.info("=" * 60)
    logger.info(f"OpenRouter API: {'✅ Configured' if os.getenv('OPENROUTER_API_KEY') else '❌ Not configured'}")
    logger.info(f"Database: Initializing...")
    
    from services.database import db
    stats = db.get_stats()
    logger.info(f"Database Stats: {stats}")
    logger.info("=" * 60)


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("🛑 Application shutting down...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("ENV", "development") == "development",
        log_level="info"
    )
