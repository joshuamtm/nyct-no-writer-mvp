"""
AI service for proposal analysis and memo generation using OpenAI or Anthropic.
"""
import os
import json
import logging
from typing import Dict, Any, Optional, List
from enum import Enum
import openai
import anthropic
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class LLMProvider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"

class AIService:
    """Handles AI-powered text analysis and generation."""
    
    def __init__(self):
        self.provider = LLMProvider(os.getenv("LLM_PROVIDER", "openai"))
        
        if self.provider == LLMProvider.OPENAI:
            self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            self.model = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
        else:
            self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            self.model = os.getenv("ANTHROPIC_MODEL", "claude-3-opus-20240229")
    
    async def extract_proposal_elements(self, proposal_text: str) -> Dict[str, Any]:
        """
        Extract key elements from a grant proposal using AI.
        
        Args:
            proposal_text: Full text of the proposal
            
        Returns:
            Dictionary containing extracted elements
        """
        extraction_prompt = """
        Analyze this grant proposal and extract the following information in JSON format:
        
        {
            "organizationName": "Name of the organization",
            "organizationMission": "Brief mission statement",
            "foundingYear": "Year founded (if mentioned)",
            "grantAmount": "Amount requested (with $ symbol)",
            "projectDescription": "Brief description of the project/program",
            "targetPopulation": "Who will be served",
            "geographicScope": "Geographic area of service",
            "currentBudget": "Organization's current operating budget (if mentioned)",
            "projectBudget": "Total project budget (if mentioned)",
            "peopleServed": "Number of people to be served",
            "keyDeliverables": ["List", "of", "main", "deliverables"],
            "timeline": "Project timeline or duration",
            "keyPartners": ["List", "of", "partner", "organizations"],
            "evaluationMethods": "How success will be measured"
        }
        
        If a field is not found in the proposal, use null for that field.
        Extract only factual information directly stated in the proposal.
        
        Proposal text:
        {proposal_text}
        """
        
        try:
            if self.provider == LLMProvider.OPENAI:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are an expert grant proposal analyst. Extract information accurately and concisely."},
                        {"role": "user", "content": extraction_prompt.format(proposal_text=proposal_text[:8000])}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.1,
                    max_tokens=1500
                )
                result = json.loads(response.choices[0].message.content)
            else:
                response = self.client.messages.create(
                    model=self.model,
                    messages=[
                        {"role": "user", "content": extraction_prompt.format(proposal_text=proposal_text[:8000])}
                    ],
                    system="You are an expert grant proposal analyst. Extract information accurately and concisely. Always respond with valid JSON.",
                    temperature=0.1,
                    max_tokens=1500
                )
                result = json.loads(response.content[0].text)
            
            return result
            
        except Exception as e:
            logger.error(f"Error extracting proposal elements: {e}")
            # Return a basic extraction as fallback
            return {
                "organizationName": self._extract_org_name_fallback(proposal_text),
                "grantAmount": self._extract_amount_fallback(proposal_text),
                "projectDescription": proposal_text[:500] if len(proposal_text) > 500 else proposal_text
            }
    
    async def generate_nyct_memo(
        self, 
        proposal_summary: Dict[str, Any],
        decline_reason: str,
        specific_context: str
    ) -> str:
        """
        Generate NYCT-formatted internal decline memo.
        
        Args:
            proposal_summary: Extracted proposal elements
            decline_reason: Reason code for decline
            specific_context: Additional context from user
            
        Returns:
            Formatted internal memo (150-200 words)
        """
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
        
        generation_prompt = f"""
        Write a concise internal memo for The New York Community Trust board in EXACTLY this format:
        
        [Organization name], founded in [year], [mission/description]. This [grant amount] request is to support [project description]. [Add 1-2 relevant details about scope, budget, or population served].
        
        I recommend this request be declined for {reason_descriptions.get(decline_reason, 'the specified reason')}. {specific_context}
        
        Rationale: {reason_descriptions.get(decline_reason, 'Decline Reason')}
        
        Requirements:
        - Total length: 150-200 words
        - Factual, objective tone
        - No subjective assessments
        - Include specific grant amount
        - Clear decline reason
        
        Proposal Summary:
        {json.dumps(proposal_summary, indent=2)}
        """
        
        try:
            if self.provider == LLMProvider.OPENAI:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a grant officer writing internal memos for a foundation board. Be concise and factual."},
                        {"role": "user", "content": generation_prompt}
                    ],
                    temperature=0.3,
                    max_tokens=300
                )
                return response.choices[0].message.content.strip()
            else:
                response = self.client.messages.create(
                    model=self.model,
                    messages=[
                        {"role": "user", "content": generation_prompt}
                    ],
                    system="You are a grant officer writing internal memos for a foundation board. Be concise and factual.",
                    temperature=0.3,
                    max_tokens=300
                )
                return response.content[0].text.strip()
                
        except Exception as e:
            logger.error(f"Error generating NYCT memo: {e}")
            # Fallback to template-based generation
            return self._generate_fallback_memo(proposal_summary, decline_reason, specific_context)
    
    async def generate_external_letter(
        self,
        organization_name: str,
        decline_reason: str
    ) -> str:
        """
        Generate a polite external decline letter.
        
        Args:
            organization_name: Name of the organization
            decline_reason: Reason for decline (for tone adjustment)
            
        Returns:
            Professional decline letter
        """
        generation_prompt = f"""
        Write a professional, empathetic decline letter for a grant application from {organization_name}.
        
        Requirements:
        - Professional and respectful tone
        - Thank them for their application
        - Acknowledge their important work
        - Indicate the decision without specific reasons
        - Encourage future applications
        - Keep it concise (150-200 words)
        
        Do not mention specific decline reasons or internal rationale.
        """
        
        try:
            if self.provider == LLMProvider.OPENAI:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are writing on behalf of The New York Community Trust. Be professional and empathetic."},
                        {"role": "user", "content": generation_prompt}
                    ],
                    temperature=0.4,
                    max_tokens=300
                )
                return response.choices[0].message.content.strip()
            else:
                response = self.client.messages.create(
                    model=self.model,
                    messages=[
                        {"role": "user", "content": generation_prompt}
                    ],
                    system="You are writing on behalf of The New York Community Trust. Be professional and empathetic.",
                    temperature=0.4,
                    max_tokens=300
                )
                return response.content[0].text.strip()
                
        except Exception as e:
            logger.error(f"Error generating external letter: {e}")
            return self._generate_fallback_letter(organization_name)
    
    def _extract_org_name_fallback(self, text: str) -> str:
        """Fallback method to extract organization name."""
        lines = text.split('\n')
        for line in lines[:20]:  # Check first 20 lines
            if 'organization' in line.lower() or 'applicant' in line.lower():
                parts = line.split(':')
                if len(parts) > 1:
                    return parts[1].strip()
        return "Organization"
    
    def _extract_amount_fallback(self, text: str) -> Optional[str]:
        """Fallback method to extract grant amount."""
        import re
        amounts = re.findall(r'\$[\d,]+(?:\.\d{2})?', text)
        return amounts[0] if amounts else None
    
    def _generate_fallback_memo(
        self,
        summary: Dict[str, Any],
        reason: str,
        context: str
    ) -> str:
        """Fallback template-based memo generation."""
        org = summary.get('organizationName', 'The organization')
        amount = summary.get('grantAmount', 'requested funding')
        desc = summary.get('projectDescription', 'their proposed project')
        
        return f"""{org} requests {amount} to support {desc}.

I recommend this request be declined. {context}

Rationale: {reason}"""
    
    def _generate_fallback_letter(self, org_name: str) -> str:
        """Fallback template-based letter generation."""
        return f"""Dear {org_name},

Thank you for your proposal submission to The New York Community Trust. We appreciate your organization's dedication to serving the community.

After careful review, we have determined that we will not be able to provide funding for this request at this time. While we recognize your important work, this proposal does not align with our current funding priorities.

We encourage you to review our updated guidelines and consider applying for future opportunities.

Best regards,
NYCT Program Team"""