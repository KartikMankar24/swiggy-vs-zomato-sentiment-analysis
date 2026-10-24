import os
import json
import secrets
import hashlib
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from fastapi import Header, HTTPException, status, Request
from pydantic import BaseModel, Field

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
KEYS_FILE = os.path.join(DATA_DIR, "api_keys.json")

class ClientRegistrationRequest(BaseModel):
    app_name: str = Field(..., example="Zomato Analytics Dashboard")
    organization: Optional[str] = Field(None, example="Consumer Insights Corp")
    client_code: Optional[str] = Field(None, example="ZMT-CORP-BLR-01", description="Custom client identifier code. Auto-generated if not provided.")
    allowed_user_agents: Optional[List[str]] = Field(default=[], example=["ZomatoJourneyClient/1.0", "PostmanRuntime/*"], description="Optional list of permitted User-Agent patterns.")

class ClientCredentialsResponse(BaseModel):
    message: str
    client_id: str
    client_code: str
    api_key: str
    user_agent_detected: str
    app_name: str
    created_at: str
    permissions: List[str]

class AuthenticatedClient(BaseModel):
    client_id: str
    client_code: str
    user_agent: str
    app_name: str
    is_active: bool
    created_at: str
    permissions: List[str]
    request_count: int

def load_keys_db() -> Dict[str, Dict[str, Any]]:
    if os.path.exists(KEYS_FILE):
        try:
            with open(KEYS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_keys_db(db: Dict[str, Dict[str, Any]]):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(KEYS_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2)

def hash_key(key: str) -> str:
    return hashlib.sha256(key.encode("utf-8")).hexdigest()

# Initialize with a default demo key if file is empty
def init_default_keys():
    db = load_keys_db()
    demo_key = "zmt_live_demo_key_9999"
    demo_id = "zmt_client_demo_001"
    demo_code = "ZMT-BLR-JOURNEY-DEMO"
    
    key_hash = hash_key(demo_key)
    if key_hash not in db:
        db[key_hash] = {
            "client_id": demo_id,
            "client_code": demo_code,
            "app_name": "Demo Consumer Journey Client",
            "organization": "Zomato CJM Open Demo",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "is_active": True,
            "allowed_user_agents": [], # empty means all allowed
            "permissions": ["read:journey", "read:funnel", "read:sentiment", "read:personas", "write:journey"],
            "request_count": 0
        }
        save_keys_db(db)

init_default_keys()

def create_client_credentials(payload: ClientRegistrationRequest, detected_user_agent: str) -> Dict[str, Any]:
    db = load_keys_db()
    
    # Generate unique client_id
    raw_id = secrets.token_hex(6)
    client_id = f"zmt_client_{raw_id}"
    
    # Generate client_code if not supplied
    if payload.client_code and payload.client_code.strip():
        client_code = payload.client_code.strip().upper()
    else:
        client_code = f"ZMT-{secrets.token_hex(3).upper()}-{datetime.now().year}"
        
    # Generate raw secure API Key
    raw_key = secrets.token_urlsafe(32)
    api_key = f"zmt_live_sec_{raw_key}"
    key_hash = hash_key(api_key)
    
    db[key_hash] = {
        "client_id": client_id,
        "client_code": client_code,
        "app_name": payload.app_name,
        "organization": payload.organization or "Personal",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "is_active": True,
        "allowed_user_agents": payload.allowed_user_agents or [],
        "permissions": ["read:journey", "read:funnel", "read:sentiment", "read:personas"],
        "request_count": 0
    }
    save_keys_db(db)
    
    return {
        "message": "API Key and Client Credentials successfully generated.",
        "client_id": client_id,
        "client_code": client_code,
        "api_key": api_key,
        "user_agent_detected": detected_user_agent,
        "app_name": payload.app_name,
        "created_at": db[key_hash]["created_at"],
        "permissions": db[key_hash]["permissions"]
    }

async def verify_api_client(
    request: Request,
    x_api_key: Optional[str] = Header(None, alias="X-API-Key", description="Your Secret API Key (e.g., zmt_live_...)"),
    x_client_id: Optional[str] = Header(None, alias="X-Client-ID", description="Your unique client identifier"),
    x_client_code: Optional[str] = Header(None, alias="X-Client-Code", description="Your assigned client/tenant code"),
    user_agent: Optional[str] = Header(None, alias="User-Agent", description="HTTP Client User-Agent string")
) -> AuthenticatedClient:
    """
    Validates client_id, client_code, api_key, and user_agent headers.
    """
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing required authentication header: 'X-API-Key'."
        )
        
    if not x_client_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing required client identifier header: 'X-Client-ID'."
        )
        
    if not x_client_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing required client code header: 'X-Client-Code'."
        )
        
    if not user_agent or not user_agent.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing required 'User-Agent' header. Every API client must provide a identifiable User-Agent."
        )

    db = load_keys_db()
    k_hash = hash_key(x_api_key)
    
    if k_hash not in db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid 'X-API-Key' provided. Please verify your credentials or register a new key."
        )
        
    client_entry = db[k_hash]
    
    if not client_entry.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This API key has been deactivated."
        )
        
    # Verify client_id matches
    if client_entry["client_id"] != x_client_id.strip():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Mismatch: 'X-Client-ID' does not match the registered client ID for this API Key."
        )
        
    # Verify client_code matches
    if client_entry["client_code"].upper() != x_client_code.strip().upper():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Mismatch: 'X-Client-Code' does not match the registered client code for this API Key."
        )
        
    # Validate User-Agent restriction if defined
    allowed_agents = client_entry.get("allowed_user_agents", [])
    if allowed_agents:
        matched = False
        ua_lower = user_agent.lower()
        for pattern in allowed_agents:
            pat_clean = pattern.lower().replace("*", "")
            if pat_clean in ua_lower:
                matched = True
                break
        if not matched:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User-Agent '{user_agent}' is not permitted for client_id '{x_client_id}'. Allowed patterns: {allowed_agents}"
            )
            
    # Increment request counter
    client_entry["request_count"] = client_entry.get("request_count", 0) + 1
    save_keys_db(db)
    
    return AuthenticatedClient(
        client_id=client_entry["client_id"],
        client_code=client_entry["client_code"],
        user_agent=user_agent,
        app_name=client_entry.get("app_name", "Unknown App"),
        is_active=client_entry.get("is_active", True),
        created_at=client_entry.get("created_at", ""),
        permissions=client_entry.get("permissions", []),
        request_count=client_entry["request_count"]
    )
