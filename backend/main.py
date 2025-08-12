from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import hashlib
import os
from datetime import datetime
import logging
from enum import Enum
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="NYCT No-Writer MVP", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Reason codes as defined in requirements
class ReasonCode(str, Enum):
    GENERAL_OPERATING_SUPPORT = "General Operating Support"
    ENDOWMENT = "Endowment"
    CAPITAL = "Capital"
    DEFICIT_FINANCING = "Deficit Financing"
    UNAPPROVED_PROGRAM_CATEGORY = "Unapproved Program Category"
    OUTSIDE_APPROVED_GUIDELINES = "Outside Approved Guidelines"
    OTHER_PROJECTS_HIGHER_MERIT = "Other Projects Higher Merit"
    OTHER_QUALITATIVE = "Other Qualitative (Replace Govt. Funds, Poor Design, Capability Problems, Duplicative Effort, Budget Exhausted)"

# Pydantic models
class AnalyzeRequest(BaseModel):
    proposal_hash: str
    text_content: str
    filename: str

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

class AnalyzeResponse(BaseModel):
    summary: ProposalSummary
    analysis_time_ms: int

class GenerateRequest(BaseModel):
    reason_code: str
    specific_reasons: str
    proposal_summary: ProposalSummary

class GeneratedOutput(BaseModel):
    internal_rationale: str
    external_reply: str
    generation_time_ms: int

class AuditLog(BaseModel):
    timestamp: datetime
    user_id: str
    proposal_hash: str
    reason_code: str
    internal_rationale: str

# Mock user for demo purposes - no authentication required
def get_current_user():
    return {"user_id": "demo_user", "role": "Program Director"}

@app.get("/")
async def root():
    return {"message": "NYCT No-Writer MVP API", "version": "1.0.0"}

@app.get("/reason-codes")
async def get_reason_codes():
    """Get all available reason codes"""
    return [{"value": code.value, "label": code.value} for code in ReasonCode]

@app.post("/upload", response_model=dict)
async def upload_proposal(file: UploadFile = File(...)):
    """Upload and process proposal document"""
    
    # Validate file size (10MB max)
    if file.size and file.size > 10 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File too large. Maximum size is 10MB.")
    
    # Validate file type
    allowed_types = ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Only PDF and Word documents are allowed.")
    
    try:
        # Read file content
        content = await file.read()
        
        # Create hash for proposal identification
        proposal_hash = hashlib.sha256(content).hexdigest()
        
        # Extract text based on file type
        if file.content_type == "application/pdf":
            text_content = extract_pdf_text(content)
        else:  # Word document
            text_content = extract_docx_text(content)
        
        # Create vector embedding for semantic compression (mock implementation)
        # In production, use pgvector with actual embeddings
        compressed_text = text_content[:2000] if len(text_content) > 2000 else text_content
        
        return {
            "proposal_hash": proposal_hash,
            "text_content": compressed_text,
            "filename": file.filename,
            "size": len(content)
        }
        
    except Exception as e:
        logger.error(f"Error processing upload: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing file")

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_proposal(request: AnalyzeRequest):
    """Analyze proposal and extract key information for Stage 1"""
    
    start_time = datetime.now()
    
    try:
        # Extract key information from proposal text
        summary = await extract_proposal_summary(request.text_content)
        
        end_time = datetime.now()
        analysis_time_ms = int((end_time - start_time).total_seconds() * 1000)
        
        return AnalyzeResponse(
            summary=summary,
            analysis_time_ms=analysis_time_ms
        )
        
    except Exception as e:
        logger.error(f"Error analyzing proposal: {str(e)}")
        raise HTTPException(status_code=500, detail="Error analyzing proposal")

@app.post("/generate", response_model=GeneratedOutput)
async def generate_rationale(request: GenerateRequest):
    """Generate internal rationale and external reply for Stage 2"""
    
    start_time = datetime.now()
    
    try:
        # Generate NYCT-formatted internal memo and generic external letter
        internal_rationale, external_reply = await generate_nyct_outputs(
            request.proposal_summary,
            request.reason_code,
            request.specific_reasons
        )
        
        end_time = datetime.now()
        generation_time_ms = int((end_time - start_time).total_seconds() * 1000)
        
        # Create audit log entry
        current_user = get_current_user()
        audit_entry = AuditLog(
            timestamp=datetime.now(),
            user_id=current_user["user_id"],
            proposal_hash=hashlib.sha256(str(request.proposal_summary).encode()).hexdigest()[:16],
            reason_code=request.reason_code,
            internal_rationale=internal_rationale
        )
        
        # In production, save to database
        logger.info(f"Audit log: {audit_entry}")
        
        return GeneratedOutput(
            internal_rationale=internal_rationale,
            external_reply=external_reply,
            generation_time_ms=generation_time_ms
        )
        
    except Exception as e:
        logger.error(f"Error generating rationale: {str(e)}")
        raise HTTPException(status_code=500, detail="Error generating rationale")

@app.get("/metrics")
async def get_metrics():
    """Get usage metrics for dashboard"""
    # Mock metrics - replace with real database queries
    return {
        "avg_generation_time_ms": 3500,
        "declines_cleared_this_week": 47,
        "total_processed": 234,
        "manual_edits_ratio": 0.23
    }

# Helper functions
def extract_pdf_text(content: bytes) -> str:
    """Extract text from PDF - mock implementation"""
    # In production, use PyPDF2 or similar
    return "Mock PDF text content extracted..."

def extract_docx_text(content: bytes) -> str:
    """Extract text from Word document - mock implementation"""
    # In production, use python-docx
    return "Mock Word document text content extracted..."

async def extract_proposal_summary(text_content: str) -> ProposalSummary:
    """Extract key information from proposal text"""
    
    # Simulate API call delay
    await asyncio.sleep(1.5)
    
    # Mock extraction - in production, use actual NLP/LLM
    # This would parse the proposal text and extract structured information
    import re
    
    # Try to extract organization name
    org_name = "Sample Organization"
    if "Astoria Cat Rescue" in text_content:
        org_name = "Astoria Cat Rescue"
    elif "Community Food Advocates" in text_content:
        org_name = "Community Food Advocates"
    elif "MediSys" in text_content or "Jamaica Hospital" in text_content:
        org_name = "MediSys Health Network"
    
    # Try to extract grant amount
    amount_match = re.search(r'\$[\d,]+(?:\.\d{2})?', text_content)
    grant_amount = amount_match.group(0) if amount_match else "$100,000"
    
    # Try to extract founding year
    year_match = re.search(r'founded in (\d{4})|established (\d{4})|since (\d{4})', text_content, re.I)
    founding_year = (year_match.group(1) or year_match.group(2) or year_match.group(3)) if year_match else None
    
    return ProposalSummary(
        organizationName=org_name,
        organizationMission="To serve and support the community through essential programs and services",
        foundingYear=founding_year,
        grantAmount=grant_amount,
        projectDescription="Community support and development program focused on addressing critical needs",
        targetPopulation="Underserved communities in New York City",
        geographicScope="Queens, NY",
        currentBudget="$125,000",
        projectBudget="$285,000",
        peopleServed="500-1,000 individuals",
        keyDeliverables=[
            "Expand service capacity",
            "Implement new programs",
            "Increase community outreach",
            "Improve operational efficiency"
        ],
        timeline="12 months"
    )

async def generate_nyct_outputs(summary: ProposalSummary, reason_code: str, specific_reasons: str) -> tuple[str, str]:
    """Generate NYCT-formatted internal memo and generic external letter"""
    
    # Simulate API call delay
    await asyncio.sleep(2)
    
    # Map reason codes to labels
    reason_labels = {
        'project_capability': 'Project Capability Problems',
        'general_operating': 'General Operating Support',
        'higher_merit': 'Other Projects Higher Merit',
        'outside_guidelines': 'Outside Approved Guidelines',
        'incomplete_proposal': 'Incomplete Proposal',
        'geographic_scope': 'Geographic Scope Limitation',
        'strategic_mismatch': 'Strategic Priority Mismatch',
        'sustainability': 'Sustainability Concerns'
    }
    
    reason_label = reason_labels.get(reason_code, 'Decline Reason')
    
    # Generate NYCT-formatted internal memo
    internal_rationale = f"""{summary.organizationName}{f', founded in {summary.foundingYear},' if summary.foundingYear else ''} {summary.organizationMission}. This {summary.grantAmount} request is to support {summary.projectDescription}. {f'The project budget is {summary.projectBudget}' if summary.projectBudget else ''}{f' and the organization\'s current operating budget is {summary.currentBudget}.' if summary.currentBudget else '.'}

I recommend this request be declined for {reason_label.lower()}. {specific_reasons}

Rationale: {reason_label}"""
    
    # Generate generic external letter
    external_reply = """Dear Applicant,

Thank you for your proposal submission to The New York Community Trust. We genuinely appreciate your organization's dedication to serving the community and the considerable time you invested in preparing your application.

After careful review by our program team and board, we have determined that we will not be able to provide funding for this request at this time. While we recognize the important work your organization does, this proposal does not align with our current funding priorities.

We encourage you to review our updated funding guidelines on our website and invite you to consider applying for future opportunities that may better align with your organization's mission and our strategic priorities.

Thank you again for considering The New York Community Trust as a potential partner in your work.

Best regards,
NYCT Program Team"""
    
    return internal_rationale, external_reply

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)