"""
Project Dwight - Lead Capture Service
Handles lead storage and notifications.
"""

from typing import Optional
from datetime import datetime
from pathlib import Path
import json
import structlog

from config import settings

logger = structlog.get_logger()

# Leads backup file path
LEADS_BACKUP_FILE = Path(__file__).parent.parent / "leads_backup.json"

# Google Sheets client (lazy initialized)
_sheets_client = None
_worksheet = None


def _get_sheets_client():
    """Get or create Google Sheets client."""
    global _sheets_client
    
    if not settings.google_sheets_enabled:
        return None
    
    if _sheets_client is not None:
        return _sheets_client
    
    try:
        # Lazy import - only when actually needed
        import gspread
        from google.oauth2.service_account import Credentials
        
        if not settings.google_credentials_file:
            logger.warning("Google credentials file not configured")
            return None
            
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        credentials = Credentials.from_service_account_file(
            settings.google_credentials_file,
            scopes=scopes
        )
        _sheets_client = gspread.authorize(credentials)
        logger.info("Google Sheets client initialized")
        return _sheets_client
        
    except Exception as e:
        logger.error("Failed to initialize Google Sheets client", error=str(e))
        return None


def _get_worksheet():
    """Get or create the leads worksheet."""
    global _worksheet
    
    if _worksheet is not None:
        return _worksheet
    
    client = _get_sheets_client()
    if client is None or not settings.google_sheets_id:
        return None
    
    try:
        import gspread
        
        spreadsheet = client.open_by_key(settings.google_sheets_id)
        
        # Try to get existing worksheet or create new one
        try:
            _worksheet = spreadsheet.worksheet("Leads")
        except gspread.WorksheetNotFound:
            _worksheet = spreadsheet.add_worksheet("Leads", rows=1000, cols=10)
            # Add headers
            _worksheet.update('A1:G1', [[
                "Timestamp", "Name", "Email", "Phone", 
                "Query Context", "Session ID", "Status"
            ]])
            logger.info("Created new Leads worksheet")
        
        return _worksheet
        
    except Exception as e:
        logger.error("Failed to get worksheet", error=str(e))
        return None


async def capture_lead(
    email: str,
    phone: str,
    name: Optional[str] = None,
    query_context: Optional[str] = None,
    session_id: Optional[str] = None
) -> bool:
    """
    Capture and store a lead.
    
    Args:
        email: User's email address
        phone: User's phone number
        name: User's name (optional)
        query_context: The query that triggered lead capture
        session_id: Session identifier
        
    Returns:
        True if lead was captured successfully
    """
    timestamp = datetime.utcnow().isoformat()
    
    # Log the lead regardless of storage success
    logger.info(
        "Lead captured",
        email=email[:3] + "***",  # Partial for privacy in logs
        has_phone=bool(phone),
        has_name=bool(name),
        session_id=session_id
    )
    
    # Store in Google Sheets if enabled
    sheets_success = await _store_lead_in_sheets(
        timestamp=timestamp,
        name=name or "",
        email=email,
        phone=phone,
        query_context=query_context or "",
        session_id=session_id or ""
    )
    
    # Send email notification if enabled
    email_success = await _send_lead_notification(
        timestamp=timestamp,
        name=name,
        email=email,
        phone=phone,
        query_context=query_context
    )
    
    # If neither external storage method is configured, use local file backup
    if not sheets_success and not email_success:
        local_success = await _store_lead_locally(
            timestamp=timestamp,
            name=name or "",
            email=email,
            phone=phone,
            query_context=query_context or "",
            session_id=session_id or ""
        )
        return local_success
    
    # Return True if at least one storage method succeeded
    return sheets_success or email_success


async def _store_lead_locally(
    timestamp: str,
    name: str,
    email: str,
    phone: str,
    query_context: str,
    session_id: str
) -> bool:
    """Store lead locally in a JSON file as fallback."""
    try:
        lead_data = {
            "timestamp": timestamp,
            "name": name,
            "email": email,
            "phone": phone,
            "query_context": query_context,
            "session_id": session_id,
            "status": "New"
        }
        
        # Load existing leads or create new list
        existing_leads = []
        if LEADS_BACKUP_FILE.exists():
            try:
                with open(LEADS_BACKUP_FILE, 'r') as f:
                    existing_leads = json.load(f)
            except (json.JSONDecodeError, IOError):
                existing_leads = []
        
        # Append new lead
        existing_leads.append(lead_data)
        
        # Save to file
        with open(LEADS_BACKUP_FILE, 'w') as f:
            json.dump(existing_leads, f, indent=2)
        
        logger.info("Lead stored locally in backup file", file=str(LEADS_BACKUP_FILE))
        return True
        
    except Exception as e:
        logger.error("Failed to store lead locally", error=str(e))
        return False


async def _store_lead_in_sheets(
    timestamp: str,
    name: str,
    email: str,
    phone: str,
    query_context: str,
    session_id: str
) -> bool:
    """Store lead in Google Sheets."""
    if not settings.google_sheets_enabled:
        logger.debug("Google Sheets not enabled, skipping")
        return False
    
    try:
        worksheet = _get_worksheet()
        if worksheet is None:
            return False
        
        # Append row
        worksheet.append_row([
            timestamp,
            name,
            email,
            phone,
            query_context[:500] if query_context else "",  # Limit length
            session_id,
            "New"
        ])
        
        logger.info("Lead stored in Google Sheets")
        return True
        
    except Exception as e:
        logger.error("Failed to store lead in Sheets", error=str(e))
        return False


async def _send_lead_notification(
    timestamp: str,
    name: Optional[str],
    email: str,
    phone: str,
    query_context: Optional[str]
) -> bool:
    """Send email notification for new lead."""
    if not settings.smtp_enabled:
        logger.debug("SMTP not enabled, skipping notification")
        return False
    
    try:
        import aiosmtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        # Create email
        msg = MIMEMultipart()
        msg['From'] = settings.smtp_username
        msg['To'] = settings.notification_email
        msg['Subject'] = f"New Lead from Dwight Chatbot - {email}"
        
        body = f"""
New Lead Captured from Tiger Logistics Chatbot

Timestamp: {timestamp}
Name: {name or 'Not provided'}
Email: {email}
Phone: {phone}

Query Context:
{query_context or 'No context available'}

---
This is an automated notification from Project Dwight.
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        await aiosmtplib.send(
            msg,
            hostname=settings.smtp_host,
            port=settings.smtp_port,
            username=settings.smtp_username,
            password=settings.smtp_password,
            start_tls=True
        )
        
        logger.info("Lead notification email sent")
        return True
        
    except Exception as e:
        logger.error("Failed to send lead notification", error=str(e))
        return False
