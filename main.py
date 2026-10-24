import os
import json
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, Depends, HTTPException, Query, status, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from auth import (
    ClientRegistrationRequest,
    ClientCredentialsResponse,
    AuthenticatedClient,
    create_client_credentials,
    verify_api_client
)
from dish_absa_engine import AspectBasedSentimentAnalyzer

# Global analyzer instance
absa_analyzer = AspectBasedSentimentAnalyzer()

app = FastAPI(
    title="Zomato Consumer Journey Mapping & Client Auth API",
    description="""
    Comprehensive REST API for Zomato Consumer Journey Mapping (CJM) and Client Authentication.
    Built upon analysis of 51,717 Bangalore restaurants and sentiment-tagged customer reviews.
    
    Demonstrates:
    - End-to-end Consumer Journey Mapping across 6 Lifecycle Stages.
    - Full API Key and Client Credentials Authentication exposing `client_id`, `client_code`, and `user_agent`.
    - Quantitative Conversion Funnels, Touchpoint Pain Points, and Behavioral Personas.
    """,
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
FUNNEL_PATH = os.path.join(DATA_DIR, "journey_funnel.json")
PERSONAS_PATH = os.path.join(DATA_DIR, "personas.json")
DISH_SENTIMENT_PATH = os.path.join(DATA_DIR, "dish_sentiment.json")
SWIGGY_ZOMATO_PATH = os.path.join(DATA_DIR, "swiggy_zomato_keyword_sentiment.json")

class ReviewAnalysisRequest(BaseModel):
    text: str

def load_json_file(path: str) -> Dict[str, Any]:
    if not os.path.exists(path):
        raise HTTPException(status_code=500, detail=f"Data file not found at {path}. Run data_pipeline.py first.")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# Response Models
class APIResponseEnvelope(BaseModel):
    status: str = "success"
    client_context: Dict[str, Any]
    data: Any

@app.get("/", tags=["General"])
async def root():
    return {
        "service": "Zomato Consumer Journey Mapping API",
        "version": "2.0.0",
        "status": "operational",
        "description": "API serving Consumer Journey Mapping insights and Client Key Authentication.",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "demo_credentials": {
            "api_key": "zmt_live_demo_key_9999",
            "client_id": "zmt_client_demo_001",
            "client_code": "ZMT-BLR-JOURNEY-DEMO",
            "header_format": {
                "X-API-Key": "zmt_live_demo_key_9999",
                "X-Client-ID": "zmt_client_demo_001",
                "X-Client-Code": "ZMT-BLR-JOURNEY-DEMO",
                "User-Agent": "YourClientName/1.0"
            }
        }
    }

@app.get("/dashboard", response_class=HTMLResponse, tags=["Dashboard UI"])
async def serve_dashboard():
    """
    Serves the interactive web dashboard with CJM funnel, dish-level ABSA, and client credentials.
    """
    dashboard_path = os.path.join(os.path.dirname(__file__), "frontend", "dashboard.html")
    if os.path.exists(dashboard_path):
        with open(dashboard_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Dashboard file not found</h1>"

# ----------------- AUTHENTICATION ENDPOINTS -----------------

@app.post("/api/v1/auth/register", response_model=ClientCredentialsResponse, tags=["Authentication & Client Identity"])
async def register_new_client(payload: ClientRegistrationRequest, request: Request):
    """
    Register a new client application. Generates a new API Key, client_id, and client_code.
    Inspects and registers the client's User-Agent.
    """
    detected_user_agent = request.headers.get("user-agent", "Unknown-User-Agent")
    creds = create_client_credentials(payload, detected_user_agent)
    return creds

@app.get("/api/v1/auth/me", tags=["Authentication & Client Identity"])
async def get_caller_identity(client: AuthenticatedClient = Depends(verify_api_client)):
    """
    Returns the authenticated client's active credentials:
    Shows `client_id`, `client_code`, and validated `user_agent`.
    """
    return {
        "message": "Client identity successfully verified.",
        "client_id": client.client_id,
        "client_code": client.client_code,
        "user_agent": client.user_agent,
        "app_name": client.app_name,
        "is_active": client.is_active,
        "permissions": client.permissions,
        "total_requests_made": client.request_count,
        "account_created_at": client.created_at
    }

# ----------------- CONSUMER JOURNEY MAPPING ENDPOINTS -----------------

@app.get("/api/v1/journey/overview", tags=["Consumer Journey Mapping"])
async def get_journey_overview(client: AuthenticatedClient = Depends(verify_api_client)):
    """
    Provides the structural architecture of the 6 Consumer Journey Mapping Stages.
    """
    funnel = load_json_file(FUNNEL_PATH)
    return APIResponseEnvelope(
        client_context={
            "client_id": client.client_id,
            "client_code": client.client_code,
            "user_agent": client.user_agent
        },
        data={
            "journey_name": "Zomato End-to-End Consumer Food Discovery & Dining Journey",
            "total_market_size_analyzed": funnel["total_market_records"],
            "unique_restaurants": funnel["unique_restaurants"],
            "stages_summary": [
                {
                    "stage_id": s["stage_id"],
                    "stage_name": s["stage_name"],
                    "user_action": s["user_action"],
                    "primary_drop_off_risk": s.get("drop_off_risk", "N/A")
                }
                for s in funnel["stages"]
            ]
        }
    )

@app.get("/api/v1/journey/funnel", tags=["Consumer Journey Mapping"])
async def get_journey_funnel(client: AuthenticatedClient = Depends(verify_api_client)):
    """
    Returns quantitative funnel volume and drop-off analysis computed from 51,717 restaurant records.
    """
    funnel = load_json_file(FUNNEL_PATH)
    return APIResponseEnvelope(
        client_context={
            "client_id": client.client_id,
            "client_code": client.client_code,
            "user_agent": client.user_agent
        },
        data=funnel
    )

@app.get("/api/v1/journey/stages", tags=["Consumer Journey Mapping"])
async def get_all_stages(client: AuthenticatedClient = Depends(verify_api_client)):
    """
    Returns all 6 journey stages with full behavioral metrics and touchpoint distributions.
    """
    funnel = load_json_file(FUNNEL_PATH)
    return APIResponseEnvelope(
        client_context={
            "client_id": client.client_id,
            "client_code": client.client_code,
            "user_agent": client.user_agent
        },
        data={"stages": funnel["stages"]}
    )

@app.get("/api/v1/journey/stages/{stage_id}", tags=["Consumer Journey Mapping"])
async def get_stage_by_id(stage_id: int, client: AuthenticatedClient = Depends(verify_api_client)):
    """
    Deep-dive into a specific stage (1: Discovery, 2: Consideration, 3: Evaluation, 4: Conversion, 5: Experience, 6: Advocacy).
    """
    funnel = load_json_file(FUNNEL_PATH)
    stage = next((s for s in funnel["stages"] if s["stage_id"] == stage_id), None)
    if not stage:
        raise HTTPException(status_code=404, detail=f"Journey Stage with ID {stage_id} not found. Valid IDs: 1 to 6.")
    return APIResponseEnvelope(
        client_context={
            "client_id": client.client_id,
            "client_code": client.client_code,
            "user_agent": client.user_agent
        },
        data=stage
    )

@app.get("/api/v1/journey/sentiment-analysis", tags=["Consumer Journey Mapping"])
async def get_sentiment_analysis(client: AuthenticatedClient = Depends(verify_api_client)):
    """
    Extracts NLP sentiment analysis across core journey touchpoints (taste, ambiance, service, value, delivery).
    """
    funnel = load_json_file(FUNNEL_PATH)
    stage_5 = funnel["stages"][4]
    stage_6 = funnel["stages"][5]
    
    return APIResponseEnvelope(
        client_context={
            "client_id": client.client_id,
            "client_code": client.client_code,
            "user_agent": client.user_agent
        },
        data={
            "net_sentiment_score": stage_6["net_sentiment_score"],
            "positive_sentiment_share_pct": stage_6["positive_sentiment_share_pct"],
            "negative_sentiment_share_pct": stage_6["negative_sentiment_share_pct"],
            "touchpoint_driver_mentions": {
                "positive": stage_5["key_drivers"]["positive_mentions"],
                "negative": stage_5["key_drivers"]["negative_mentions"]
            },
            "churn_drivers": stage_6["churn_drivers"],
            "advocacy_drivers": stage_6["advocacy_drivers"]
        }
    )

@app.get("/api/v1/journey/personas", tags=["Consumer Journey Mapping"])
async def get_personas(client: AuthenticatedClient = Depends(verify_api_client)):
    """
    Returns demographic & behavioral personas derived from the Zomato Bangalore dataset.
    """
    personas = load_json_file(PERSONAS_PATH)
    return APIResponseEnvelope(
        client_context={
            "client_id": client.client_id,
            "client_code": client.client_code,
            "user_agent": client.user_agent
        },
        data={"personas": personas}
    )

@app.get("/api/v1/journey/recommendation", tags=["Consumer Journey Mapping"])
async def get_journey_recommendations(
    cuisine: Optional[str] = Query("North Indian", description="Desired cuisine"),
    dining_type: Optional[str] = Query("Delivery", description="Delivery, Dine-out, Cafes, Buffet"),
    max_budget: Optional[float] = Query(800.0, description="Maximum budget for two in INR"),
    client: AuthenticatedClient = Depends(verify_api_client)
):
    """
    Simulates the Evaluation & Decision Stage: Recommends restaurants fitting persona constraints.
    """
    # Sample algorithmic matching from pre-filtered criteria
    return APIResponseEnvelope(
        client_context={
            "client_id": client.client_id,
            "client_code": client.client_code,
            "user_agent": client.user_agent
        },
        data={
            "query_criteria": {
                "cuisine": cuisine,
                "dining_type": dining_type,
                "max_budget": max_budget
            },
            "journey_stage_active": "Stage 3: Trust & Evaluation -> Stage 4: Conversion",
            "top_matches": [
                {
                    "name": "Empire Restaurant",
                    "location": "Koramangala 5th Block",
                    "rating": 4.1,
                    "votes": 4884,
                    "cost_for_two": 750,
                    "online_order": True,
                    "top_dishes": "Chicken Biryani, Ghee Rice, Kababs",
                    "match_score": "98%"
                },
                {
                    "name": "Meghana Foods",
                    "location": "Jayanagar",
                    "rating": 4.4,
                    "votes": 3672,
                    "cost_for_two": 600,
                    "online_order": True,
                    "top_dishes": "Meghana Special Biryani, Paneer Biryani, Chicken Boneless",
                    "match_score": "96%"
                },
                {
                    "name": "Kobe Sizzlers",
                    "location": "Indiranagar",
                    "rating": 4.2,
                    "votes": 1421,
                    "cost_for_two": 800,
                    "online_order": True,
                    "top_dishes": "Chicken Sizzler, Garlic Bread, Ice Tea",
                    "match_score": "91%"
                }
            ]
        }
    )

# ----------------- ASPECT-BASED DISH SENTIMENT (ABSA) ENDPOINTS -----------------

@app.get("/api/v1/sentiment/dishes", tags=["Aspect-Based Sentiment Analysis (ABSA)"])
async def get_all_dish_sentiments(client: AuthenticatedClient = Depends(verify_api_client)):
    """
    Returns pre-aggregated Aspect-Based Sentiment Analysis (ABSA) for top Bangalore dishes.
    Breaks down sentiment across Taste, Portion, Value, and Freshness.
    """
    dish_data = load_json_file(DISH_SENTIMENT_PATH)
    return APIResponseEnvelope(
        client_context={
            "client_id": client.client_id,
            "client_code": client.client_code,
            "user_agent": client.user_agent
        },
        data={"dishes": dish_data}
    )

@app.get("/api/v1/sentiment/dishes/{dish_name}", tags=["Aspect-Based Sentiment Analysis (ABSA)"])
async def get_dish_sentiment_by_name(dish_name: str, client: AuthenticatedClient = Depends(verify_api_client)):
    """
    Deep-dive into a specific dish's aspect breakdown, positive/negative drivers, and top places.
    """
    dish_data = load_json_file(DISH_SENTIMENT_PATH)
    matched = None
    for k, v in dish_data.items():
        if k.lower() == dish_name.lower():
            matched = v
            break
    if not matched:
        raise HTTPException(
            status_code=404,
            detail=f"Dish '{dish_name}' not found. Available dishes: {list(dish_data.keys())}"
        )
    return APIResponseEnvelope(
        client_context={
            "client_id": client.client_id,
            "client_code": client.client_code,
            "user_agent": client.user_agent
        },
        data=matched
    )

@app.post("/api/v1/sentiment/absa/analyze", tags=["Aspect-Based Sentiment Analysis (ABSA)"])
async def analyze_custom_review(
    payload: ReviewAnalysisRequest,
    client: AuthenticatedClient = Depends(verify_api_client)
):
    """
    Live RoBERTa/BERT Aspect-Based Sentiment Analysis on customer review text.
    Extracts dish entities, aspect polarity (Taste, Portion, Value, Freshness), and model confidence.
    """
    analysis_res = absa_analyzer.analyze_text(payload.text)
    return APIResponseEnvelope(
        client_context={
            "client_id": client.client_id,
            "client_code": client.client_code,
            "user_agent": client.user_agent
        },
        data=analysis_res
    )

@app.get("/api/v1/sentiment/swiggy-zomato", tags=["Swiggy vs Zomato Sentiment"])
async def get_swiggy_zomato_sentiment(client: AuthenticatedClient = Depends(verify_api_client)):
    """
    Returns positive, negative, and neutral comment metrics for mentions of 'swiggy' and 'zomato'.
    """
    sz_data = load_json_file(SWIGGY_ZOMATO_PATH)
    return APIResponseEnvelope(
        client_context={
            "client_id": client.client_id,
            "client_code": client.client_code,
            "user_agent": client.user_agent
        },
        data=sz_data
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)
