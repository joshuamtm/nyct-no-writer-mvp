"""
Enhanced NYCT No-Writer Backend with Real AI Integration
"""
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import hashlib
import os
import time
import uuid
from datetime import datetime
import logging
from enum import Enum
import asyncio
from dotenv import load_dotenv

# Import our service modules
from services.document_processor import DocumentProcessor
from services.ai_service import AIService
from services.metrics_service import MetricsService

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="NYCT No-Writer MVP", version="2.0.0")

# CORS middleware
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
ai_service = AIService()
metrics_service = MetricsService()
document_processor = DocumentProcessor()

# Reason codes
class ReasonCode(str, Enum):
    PROJECT_CAPABILITY = "project_capability"
    GENERAL_OPERATING = "general_operating"
    HIGHER_MERIT = "higher_merit"
    OUTSIDE_GUIDELINES = "outside_guidelines"
    INCOMPLETE_PROPOSAL = "incomplete_proposal"
    GEOGRAPHIC_SCOPE = "geographic_scope"
    STRATEGIC_MISMATCH = "strategic_mismatch"
    SUSTAINABILITY = "sustainability"

# Pydantic models
class ProposalSummary(BaseModel):
    organizationName: Optional[str]
    organizationMission: Optional[str]
    foundingYear: Optional[str]
    grantAmount: Optional[str]
    projectDescription: Optional[str]
    targetPopulation: Optional[str]
    geographicScope: Optional[str]
    currentBudget: Optional[str]
    projectBudget: Optional[str]
    peopleServed: Optional[str]
    keyDeliverables: Optional[List[str]]
    timeline: Optional[str]
    keyPartners: Optional[List[str]]
    evaluationMethods: Optional[str]

class AnalyzeRequest(BaseModel):
    proposal_hash: str
    text_content: str
    filename: str

class AnalyzeResponse(BaseModel):
    summary: ProposalSummary
    analysis_time_ms: int
    extracted_text_preview: Optional[str]

class GenerateRequest(BaseModel):
    reason_code: str
    specific_reasons: str
    proposal_summary: ProposalSummary
    session_id: Optional[str]

class GeneratedOutput(BaseModel):
    internal_rationale: str
    external_reply: str
    generation_time_ms: int

class UploadResponse(BaseModel):
    proposal_hash: str
    text_content: str
    filename: str
    size: int
    word_count: int
    extraction_time_ms: int

# Session management
def get_session_id(session_id: Optional[str] = None) -> str:
    """Get or create session ID"""
    return session_id or str(uuid.uuid4())

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "NYCT No-Writer MVP API",
        "version": "2.0.0",
        "ai_enabled": bool(os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")),
        "metrics_enabled": os.getenv("ENABLE_METRICS", "True") == "True"
    }

@app.get("/reason-codes")
async def get_reason_codes():
    """Get all available reason codes"""
    reason_descriptions = {
        ReasonCode.PROJECT_CAPABILITY: "Project Capability Problems",
        ReasonCode.GENERAL_OPERATING: "General Operating Support",
        ReasonCode.HIGHER_MERIT: "Other Projects Higher Merit",
        ReasonCode.OUTSIDE_GUIDELINES: "Outside Approved Guidelines",
        ReasonCode.INCOMPLETE_PROPOSAL: "Incomplete Proposal",
        ReasonCode.GEOGRAPHIC_SCOPE: "Geographic Scope Limitation",
        ReasonCode.STRATEGIC_MISMATCH: "Strategic Priority Mismatch",
        ReasonCode.SUSTAINABILITY: "Sustainability Concerns"
    }
    
    return [
        {"value": code.value, "label": reason_descriptions[code]}
        for code in ReasonCode
    ]

@app.post("/upload", response_model=UploadResponse)
async def upload_proposal(
    file: UploadFile = File(...),
    session_id: Optional[str] = Form(None)
):
    """Upload and extract text from proposal document"""
    
    start_time = time.time()
    session_id = get_session_id(session_id)
    
    # Validate file size (10MB max)
    content = await file.read()
    file_size = len(content)
    
    if file_size > 10 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File too large. Maximum size is 10MB.")
    
    # Validate file type
    allowed_types = [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/msword"
    ]
    
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file.content_type}. Only PDF and Word documents are allowed."
        )
    
    try:
        # Extract text from document
        extracted_text = await document_processor.extract_text(content, file.content_type)
        cleaned_text = document_processor.clean_text(extracted_text)
        
        # Generate hash for proposal
        proposal_hash = hashlib.sha256(content).hexdigest()[:12]
        
        # Calculate word count
        word_count = len(cleaned_text.split())
        
        # Calculate processing time
        extraction_time_ms = int((time.time() - start_time) * 1000)
        
        # Track metrics
        if os.getenv("ENABLE_METRICS", "True") == "True":
            metrics_service.track_upload(
                organization_name="Unknown",  # Will be extracted in analysis
                file_size=file_size,
                word_count=word_count,
                processing_time_ms=extraction_time_ms,
                session_id=session_id
            )
        
        logger.info(f"Successfully extracted {word_count} words from {file.filename}")
        
        return UploadResponse(
            proposal_hash=proposal_hash,
            text_content=cleaned_text,
            filename=file.filename,
            size=file_size,
            word_count=word_count,
            extraction_time_ms=extraction_time_ms
        )
        
    except Exception as e:
        logger.error(f"Error processing upload: {e}")
        
        # Track error
        if os.getenv("ENABLE_METRICS", "True") == "True":
            metrics_service.track_error("upload", str(e), session_id)
        
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_proposal(request: AnalyzeRequest):
    """Analyze proposal and extract key elements using AI"""
    
    start_time = time.time()
    session_id = get_session_id()
    
    try:
        # Use AI to extract proposal elements
        if os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY"):
            # Real AI extraction
            extracted_elements = await ai_service.extract_proposal_elements(request.text_content)
            
            # Convert to ProposalSummary format
            summary = ProposalSummary(**extracted_elements)
        else:
            # Fallback to basic extraction if no API keys
            logger.warning("No AI API keys configured, using basic extraction")
            summary = ProposalSummary(
                organizationName="Sample Organization",
                grantAmount="$100,000",
                projectDescription=request.text_content[:500],
                targetPopulation="Community members",
                geographicScope="New York City"
            )
        
        # Calculate processing time
        analysis_time_ms = int((time.time() - start_time) * 1000)
        
        # Track metrics
        if os.getenv("ENABLE_METRICS", "True") == "True":
            metrics_service.track_analysis(
                organization_name=summary.organizationName or "Unknown",
                processing_time_ms=analysis_time_ms,
                session_id=session_id,
                llm_provider=os.getenv("LLM_PROVIDER", "openai")
            )
        
        logger.info(f"Successfully analyzed proposal for {summary.organizationName}")
        
        return AnalyzeResponse(
            summary=summary,
            analysis_time_ms=analysis_time_ms,
            extracted_text_preview=request.text_content[:200] + "..."
        )
        
    except Exception as e:
        logger.error(f"Error analyzing proposal: {e}")
        
        # Track error
        if os.getenv("ENABLE_METRICS", "True") == "True":
            metrics_service.track_error("analysis", str(e), session_id)
        
        # Return basic extraction as fallback
        return AnalyzeResponse(
            summary=ProposalSummary(
                organizationName="Organization",
                projectDescription="Unable to fully analyze proposal",
                grantAmount="Unknown"
            ),
            analysis_time_ms=int((time.time() - start_time) * 1000)
        )

@app.post("/generate", response_model=GeneratedOutput)
async def generate_decline(request: GenerateRequest):
    """Generate decline memo and external letter using AI"""
    
    start_time = time.time()
    session_id = get_session_id(request.session_id)
    
    try:
        # Generate using AI if available
        if os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY"):
            # Generate internal memo
            internal_memo = await ai_service.generate_nyct_memo(
                proposal_summary=request.proposal_summary.dict(),
                decline_reason=request.reason_code,
                specific_context=request.specific_reasons
            )
            
            # Generate external letter
            external_letter = await ai_service.generate_external_letter(
                organization_name=request.proposal_summary.organizationName or "Applicant",
                decline_reason=request.reason_code
            )
        else:
            # Fallback to template-based generation
            logger.warning("No AI API keys configured, using template generation")
            internal_memo = generate_template_memo(
                request.proposal_summary,
                request.reason_code,
                request.specific_reasons
            )
            external_letter = generate_template_letter(
                request.proposal_summary.organizationName or "Applicant"
            )
        
        # Calculate processing time
        generation_time_ms = int((time.time() - start_time) * 1000)
        
        # Track metrics
        if os.getenv("ENABLE_METRICS", "True") == "True":
            metrics_service.track_generation(
                organization_name=request.proposal_summary.organizationName or "Unknown",
                decline_reason=request.reason_code,
                processing_time_ms=generation_time_ms,
                session_id=session_id,
                llm_provider=os.getenv("LLM_PROVIDER", "openai")
            )
        
        logger.info(f"Successfully generated decline for {request.proposal_summary.organizationName}")
        
        return GeneratedOutput(
            internal_rationale=internal_memo,
            external_reply=external_letter,
            generation_time_ms=generation_time_ms
        )
        
    except Exception as e:
        logger.error(f"Error generating decline: {e}")
        
        # Track error
        if os.getenv("ENABLE_METRICS", "True") == "True":
            metrics_service.track_error("generation", str(e), session_id)
        
        raise HTTPException(status_code=500, detail=f"Error generating decline: {str(e)}")

@app.get("/metrics")
async def get_metrics(days: int = 30):
    """Get usage metrics for dashboard"""
    
    if os.getenv("ENABLE_METRICS", "True") != "True":
        return {"message": "Metrics disabled"}
    
    try:
        summary = metrics_service.get_summary_metrics(days)
        daily = metrics_service.get_daily_metrics(min(days, 7))
        
        return {
            "summary": summary,
            "daily": daily,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error retrieving metrics: {e}")
        return {
            "error": "Failed to retrieve metrics",
            "timestamp": datetime.utcnow().isoformat()
        }

# Template-based generation functions (fallback)
def generate_template_memo(
    summary: ProposalSummary,
    reason_code: str,
    specific_reasons: str
) -> str:
    """Generate memo using template (fallback when AI not available)"""
    
    reason_descriptions = {
        "project_capability": "Project Capability Problems",
        "general_operating": "General Operating Support",
        "higher_merit": "Other Projects Higher Merit",
        "outside_guidelines": "Outside Approved Guidelines",
        "incomplete_proposal": "Incomplete Proposal",
        "geographic_scope": "Geographic Scope Limitation",
        "strategic_mismatch": "Strategic Priority Mismatch",
        "sustainability": "Sustainability Concerns"
    }
    
    org = summary.organizationName or "The organization"
    amount = summary.grantAmount or "requested funding"
    desc = summary.projectDescription or "their proposed project"
    
    memo = f"{org}"
    if summary.foundingYear:
        memo += f", founded in {summary.foundingYear},"
    
    if summary.organizationMission:
        memo += f" {summary.organizationMission}."
    else:
        memo += " serves the community."
    
    memo += f" This {amount} request is to support {desc}."
    
    if summary.projectBudget:
        memo += f" The project budget is {summary.projectBudget}."
    
    if summary.currentBudget:
        memo += f" The organization's current operating budget is {summary.currentBudget}."
    
    memo += f"\n\nI recommend this request be declined for {reason_descriptions.get(reason_code, 'the specified reason').lower()}. {specific_reasons}"
    memo += f"\n\nRationale: {reason_descriptions.get(reason_code, 'Decline Reason')}"
    
    return memo

def generate_template_letter(org_name: str) -> str:
    """Generate external letter using template (fallback when AI not available)"""
    
    return f"""Dear {org_name},

Thank you for your proposal submission to The New York Community Trust. We genuinely appreciate your organization's dedication to serving the community and the considerable time you invested in preparing your application.

After careful review by our program team and board, we have determined that we will not be able to provide funding for this request at this time. While we recognize the important work your organization does, this proposal does not align with our current funding priorities.

We encourage you to review our updated funding guidelines on our website and invite you to consider applying for future opportunities that may better align with your organization's mission and our strategic priorities.

Thank you again for considering The New York Community Trust as a potential partner in your work.

Best regards,
NYCT Program Team"""

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)