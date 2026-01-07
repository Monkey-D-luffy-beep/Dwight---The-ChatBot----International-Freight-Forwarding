"""
Project Dwight - Chat Router
Main chat endpoint for the AI assistant.
"""

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import structlog

from config import settings
from core.intent_classifier import classify_intent, IntentType
from core.rag_engine import retrieve_context
from core.llm_client import generate_response
from core.guardrails import validate_response, check_lead_trigger
from services.lead_capture import capture_lead
from services.logger import log_chat_interaction

router = APIRouter()
logger = structlog.get_logger()


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str = Field(..., min_length=1, max_length=2000, description="User message")
    session_id: Optional[str] = Field(None, description="Optional session identifier")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "What services does Tiger Logistics offer?",
                "session_id": "user-123"
            }
        }


class LeadInfo(BaseModel):
    """Lead information model."""
    email: Optional[str] = None
    phone: Optional[str] = None
    name: Optional[str] = None


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    response: str = Field(..., description="AI assistant response")
    intent: str = Field(..., description="Detected intent type")
    lead_prompt: bool = Field(False, description="Whether to prompt for lead info")
    timestamp: str = Field(..., description="Response timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "response": "Tiger Logistics offers FCL shipping, LCL shipping, air freight, cold chain logistics, project cargo, and customs clearance services.",
                "intent": "support",
                "lead_prompt": False,
                "timestamp": "2025-01-01T00:00:00Z"
            }
        }


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, req: Request):
    """
    Main chat endpoint for the AI assistant.
    
    Handles user queries by:
    1. Classifying intent (support/sales/internal)
    2. Retrieving relevant context via RAG
    3. Generating response using LLM
    4. Applying guardrails
    5. Checking for lead capture triggers
    """
    start_time = datetime.utcnow()
    
    try:
        user_message = request.message.strip()
        session_id = request.session_id or "anonymous"
        
        logger.info(
            "Chat request received",
            session_id=session_id,
            message_length=len(user_message)
        )
        
        # Step 1: Classify intent
        intent = await classify_intent(user_message)
        logger.info("Intent classified", intent=intent.value)
        
        # Step 2: Retrieve relevant context
        context = await retrieve_context(user_message, intent)
        logger.info("Context retrieved", context_length=len(context))
        
        # Step 3: Generate response
        response = await generate_response(
            query=user_message,
            context=context,
            intent=intent
        )
        
        # Step 4: Apply guardrails
        validated_response = await validate_response(response, context)
        
        # Step 5: Check for lead capture trigger
        lead_prompt = await check_lead_trigger(user_message, intent)
        
        # Log interaction
        await log_chat_interaction(
            session_id=session_id,
            message=user_message,
            response=validated_response,
            intent=intent.value,
            duration_ms=(datetime.utcnow() - start_time).total_seconds() * 1000
        )
        
        return ChatResponse(
            response=validated_response,
            intent=intent.value,
            lead_prompt=lead_prompt,
            timestamp=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        logger.error("Chat error", error=str(e), session_id=request.session_id)
        raise HTTPException(
            status_code=500,
            detail="I'm having trouble processing your request. Please try again."
        )


class LeadCaptureRequest(BaseModel):
    """Request model for lead capture."""
    email: str = Field(..., description="User email address")
    phone: str = Field(..., description="User phone number")
    name: Optional[str] = Field(None, description="User name")
    query_context: Optional[str] = Field(None, description="Original query context")
    session_id: Optional[str] = Field(None, description="Session identifier")


class LeadCaptureResponse(BaseModel):
    """Response model for lead capture."""
    success: bool
    message: str


@router.post("/lead", response_model=LeadCaptureResponse)
async def submit_lead(request: LeadCaptureRequest):
    """
    Lead capture endpoint.
    Stores lead information in Google Sheets and sends email notification.
    """
    try:
        logger.info(
            "Lead capture request",
            email=request.email[:3] + "***",  # Partial for privacy
            session_id=request.session_id
        )
        
        success = await capture_lead(
            email=request.email,
            phone=request.phone,
            name=request.name,
            query_context=request.query_context,
            session_id=request.session_id
        )
        
        if success:
            return LeadCaptureResponse(
                success=True,
                message="Thank you! Our team will reach out to you shortly."
            )
        else:
            return LeadCaptureResponse(
                success=False,
                message="There was an issue submitting your information. Please try again or contact us directly."
            )
            
    except Exception as e:
        logger.error("Lead capture error", error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Unable to process your request. Please contact us directly at info@tigerlogistics.in"
        )
