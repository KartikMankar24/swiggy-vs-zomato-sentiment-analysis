import streamlit as st
import pandas as pd
import requests
import json
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Zomato Consumer Journey & ABSA Dashboard",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #E23744;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #555;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F8F9FA;
        border-radius: 8px;
        padding: 16px;
        border-left: 4px solid #E23744;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar: API & Credential Configuration
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/b/bd/Zomato_Logo.svg", width=180)
st.sidebar.markdown("### 🔑 API Key & Client Credentials")

api_base_url = st.sidebar.text_input("API Base URL", "http://127.0.0.1:8000")

# Demo Credential Defaults
DEFAULT_KEY = "zmt_live_demo_key_9999"
DEFAULT_ID = "zmt_client_demo_001"
DEFAULT_CODE = "ZMT-BLR-JOURNEY-DEMO"
DEFAULT_UA = "ZomatoCJMExplorer/2.0 (Streamlit; Windows)"

if "api_key" not in st.session_state:
    st.session_state["api_key"] = DEFAULT_KEY
if "client_id" not in st.session_state:
    st.session_state["client_id"] = DEFAULT_ID
if "client_code" not in st.session_state:
    st.session_state["client_code"] = DEFAULT_CODE
if "user_agent" not in st.session_state:
    st.session_state["user_agent"] = DEFAULT_UA

api_key_input = st.sidebar.text_input("X-API-Key", st.session_state["api_key"], type="password")
client_id_input = st.sidebar.text_input("X-Client-ID", st.session_state["client_id"])
client_code_input = st.sidebar.text_input("X-Client-Code", st.session_state["client_code"])
user_agent_input = st.sidebar.text_input("User-Agent Header", st.session_state["user_agent"])

st.session_state["api_key"] = api_key_input
st.session_state["client_id"] = client_id_input
st.session_state["client_code"] = client_code_input
st.session_state["user_agent"] = user_agent_input

def get_auth_headers():
    return {
        "X-API-Key": st.session_state["api_key"],
        "X-Client-ID": st.session_state["client_id"],
        "X-Client-Code": st.session_state["client_code"],
        "User-Agent": st.session_state["user_agent"]
    }

# Connection Check
auth_status = False
auth_details = {}
try:
    auth_resp = requests.get(f"{api_base_url}/api/v1/auth/me", headers=get_auth_headers(), timeout=3)
    if auth_resp.status_code == 200:
        auth_status = True
        auth_details = auth_resp.json()
        st.sidebar.success(f"🟢 Authenticated: {auth_details.get('client_id')}")
    else:
        st.sidebar.error(f"🔴 Auth Failed ({auth_resp.status_code}): {auth_resp.json().get('detail', 'Unknown')}")
except Exception as e:
    st.sidebar.warning("⚠️ Could not connect to API server. Ensure FastAPI is running on port 8000.")

st.sidebar.markdown("---")
with st.sidebar.expander("➕ Register New Client Credentials"):
    new_app = st.text_input("App Name", "My Analytics Suite")
    new_code = st.text_input("Custom Client Code (optional)", "ZMT-MYAPP-01")
    if st.button("Generate New API Key"):
        try:
            reg_res = requests.post(
                f"{api_base_url}/api/v1/auth/register",
                json={"app_name": new_app, "client_code": new_code},
                headers={"User-Agent": user_agent_input}
            )
            if reg_res.status_code == 200:
                data = reg_res.json()
                st.session_state["api_key"] = data["api_key"]
                st.session_state["client_id"] = data["client_id"]
                st.session_state["client_code"] = data["client_code"]
                st.sidebar.success("New Key Generated & Applied!")
                st.rerun()
            else:
                st.sidebar.error("Registration failed.")
        except Exception as err:
            st.sidebar.error(str(err))

# Header
st.markdown('<div class="main-header">Zomato Consumer Journey & Aspect-Based Sentiment Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Data Intelligence Platform analyzing 51,717 restaurant interactions, conversion funnels, dining personas, and dish-level ABSA.</div>', unsafe_allow_html=True)

# Main Navigation Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Journey Funnel & Conversion",
    "👥 Consumer Personas",
    "🍲 Dish-Level ABSA Intelligence",
    "🧠 Live RoBERTa Review Analyzer",
    "🔐 API Telemetry & Credentials"
])

# ----------------- TAB 1: FUNNEL & CJM -----------------
with tab1:
    st.subheader("Lifecycle Conversion Funnel (Bangalore Market)")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Market Listings", "51,717", "8,792 Brands")
    with col2:
        st.metric("Online Delivery Adoption", "58.9%", "+12% YoY")
    with col3:
        st.metric("Table Booking Enabled", "12.5%", "High-end & Nightlife")
    with col4:
        st.metric("Overall Market Rating", "3.70 / 5.0", "Median 41 Votes")
        
    st.markdown("---")
    
    funnel_stages = [
        "Stage 1: Discovery & Trigger",
        "Stage 2: Exploration & Filter",
        "Stage 3: Trust & Evaluation",
        "Stage 4: Purchase & Conversion"
    ]
    funnel_values = [51717, 42407, 29995, 19652]
    
    col_chart, col_desc = st.columns([3, 2])
    with col_chart:
        fig_funnel = go.Figure(go.Funnel(
            y=funnel_stages,
            x=funnel_values,
            textinfo="value+percent initial",
            marker={"color": ["#E23744", "#F05A65", "#FA7D87", "#FFA6AD"]},
            connector={"line": {"color": "#CCC", "width": 1.5}}
        ))
        fig_funnel.update_layout(
            title_text="Consumer Journey Conversion Drop-off Funnel",
            margin=dict(l=20, r=20, t=40, b=20),
            height=380
        )
        st.plotly_chart(fig_funnel, use_container_width=True)
        
    with col_desc:
        st.markdown("#### 🔍 Stage Transition Dynamics")
        selected_stage = st.selectbox(
            "Select Journey Stage to Inspect",
            [
                "Stage 1: Discovery (Locality & Craving)",
                "Stage 2: Exploration (Filters & Cost)",
                "Stage 3: Evaluation (Ratings & Reviews)",
                "Stage 4: Conversion (Checkout & Booking)",
                "Stage 5: Fulfillment (Delivery & Service)",
                "Stage 6: Advocacy (Retention & Reviews)"
            ]
        )
        if "Stage 1" in selected_stage:
            st.info("""
            **Customer Intent**: *"Hungry or planning a meal out. What's good near me?"*  
            • **Top Neighborhood Hubs**: BTM (5,124), HSR (2,523), Koramangala 5th Block (2,800+).  
            • **Top Searched Cuisines**: North Indian (21,085), Chinese (15,547), South Indian (8,644).  
            • **Drop-off Trigger**: Sparse listings in outer suburbs or poor cuisine options.
            """)
        elif "Stage 2" in selected_stage:
            st.info("""
            **Customer Intent**: *"Does it fit my budget? Can I get delivery or book a table?"*  
            • **Budget Split**: < ₹400 (35%), ₹400-800 (45%), > ₹800 (20%).  
            • **Avg Cost for Two**: ₹555 (~₹278/individual meal).  
            • **Drop-off Trigger**: Restaurant lacks online ordering or price exceeds budget.
            """)
        elif "Stage 3" in selected_stage:
            st.info("""
            **Customer Intent**: *"Is the food actually good? What are previous diners saying?"*  
            • **Ratings Threshold**: 30.5% rated > 4.0; median 41 votes required for high trust.  
            • **Dishes Liked Signal**: 45.6% listings feature verified customer favorite dishes.  
            • **Drop-off Trigger**: Low rating (<3.5) or lack of peer review validation.
            """)
        elif "Stage 4" in selected_stage:
            st.info("""
            **Customer Intent**: *"Adding to cart and completing payment."*  
            • **Delivery Share**: ~85% of transactions; avg basket size ₹278/person.  
            • **Dine-out Booking**: ~15% share; avg ticket size ₹555/couple.  
            • **Drop-off Trigger**: Surge pricing, high delivery fees, unavailable reservation slots.
            """)
        elif "Stage 5" in selected_stage:
            st.info("""
            **Customer Intent**: *"Receiving food delivery or dining at venue."*  
            • **Critical Fulfillment Touchpoints**: Delivery speed, food temperature, packaging integrity, restaurant hygiene.  
            • **Drop-off Trigger**: Spilled sauce/gravy, cold soggy food, delivery delay > 45 mins.
            """)
        else:
            st.info("""
            **Customer Intent**: *"Submitting star rating, leaving review, and re-ordering."*  
            • **Net Sentiment Score**: +68.35% (84.18% Positive, 15.82% Negative).  
            • **Advocacy Boosters**: Delicious flavor, quick delivery, generous portions.  
            • **Churn Drivers**: Late delivery, cold food, small portion sizes.
            """)

# ----------------- TAB 2: PERSONAS -----------------
with tab2:
    st.subheader("Consumer Personas Derived from Demographics")
    
    personas_data = [
        {
            "name": "The Budget Delivery Explorer",
            "icon": "🎓",
            "budget": "₹250",
            "channel": "Delivery",
            "cuisines": "Fast Food, Biryani, North Indian",
            "touchpoints": "Discount promo codes, low delivery fee, quick bites",
            "friction": "Surge delivery fees or high minimum order threshold"
        },
        {
            "name": "The Weekend Social Diner",
            "icon": "🍸",
            "budget": "₹1,200",
            "channel": "Dine-out / Nightlife / Buffet",
            "cuisines": "Continental, Finger Food, Italian",
            "touchpoints": "Table reservation, ambiance gallery, valet parking info",
            "friction": "Table booking cancellation or crowded seating without reservations"
        },
        {
            "name": "The Everyday Working Professional",
            "icon": "💼",
            "budget": "₹350",
            "channel": "Delivery (Lunch)",
            "cuisines": "South Indian, Thali, Healthy Food",
            "touchpoints": "Fast delivery (<30 min), tamper-proof packaging, repeat button",
            "friction": "Late delivery eating into lunch break, spilled gravy"
        },
        {
            "name": "The Aesthetic Cafe Hopper",
            "icon": "☕",
            "budget": "₹600",
            "channel": "Cafes / Desserts",
            "cuisines": "Specialty Coffee, Desserts, Bakery",
            "touchpoints": "Wi-Fi in reviews, cozy decor photos, artisanal coffee menu",
            "friction": "No seating availability, poor internet, or lack of power outlets"
        }
    ]
    
    p_cols = st.columns(2)
    for idx, p in enumerate(personas_data):
        with p_cols[idx % 2]:
            st.markdown(f"""
            <div class="metric-card">
                <h4>{p['icon']} {p['name']}</h4>
                <p><strong>Avg Budget:</strong> {p['budget']} | <strong>Preferred Channel:</strong> {p['channel']}</p>
                <p><strong>Favorite Cuisines:</strong> {p['cuisines']}</p>
                <p><strong>Key Touchpoints:</strong> {p['touchpoints']}</p>
                <p style="color:#C0392B;"><strong>Critical Friction:</strong> {p['friction']}</p>
            </div>
            <br>
            """, unsafe_allow_html=True)

# ----------------- TAB 3: DISH-LEVEL ABSA -----------------
with tab3:
    st.subheader("Aspect-Based Sentiment Analysis (ABSA) for Top Dishes")
    st.markdown("Granular breakdown of customer sentiment across 4 key dimensions: **Taste, Portion, Value, and Freshness**.")
    
    try:
        dish_res = requests.get(f"{api_base_url}/api/v1/sentiment/dishes", headers=get_auth_headers(), timeout=4)
        if dish_res.status_code == 200:
            dishes_dict = dish_res.json()["data"]["dishes"]
        else:
            dishes_dict = {}
    except Exception:
        dishes_dict = {}

    if not dishes_dict:
        st.warning("Could not fetch dish ABSA data from API. Using local cache.")
        dishes_dict = {
            "Biryani": {
                "dish_name": "Biryani (Chicken & Mutton)",
                "total_mentions_analyzed": 5422,
                "overall_sentiment_positive_pct": 86.4,
                "aspect_scores": {"taste_and_flavor": 0.84, "portion_quantity": 0.62, "value_for_money": 0.71, "freshness_and_packaging": 0.78},
                "top_positive_drivers": ["Fragrant dum spices", "Tender succulent meat", "Generous meat pieces"],
                "top_negative_drivers": ["Oily bottom layer", "Cold rice delivery", "Portion too small for price"],
                "top_recommended_places": [{"name": "Meghana Foods", "rating": 4.4, "locality": "Jayanagar"}, {"name": "Nagarjuna", "rating": 4.3, "locality": "Residency Road"}]
            }
        }
        
    selected_dish = st.selectbox("Select Dish Entity", list(dishes_dict.keys()))
    dish_info = dishes_dict[selected_dish]
    
    col_d1, col_d2 = st.columns([3, 2])
    with col_d1:
        aspects = ["Taste & Flavor", "Portion Quantity", "Value for Money", "Freshness & Prep"]
        scores = [
            dish_info["aspect_scores"]["taste_and_flavor"],
            dish_info["aspect_scores"]["portion_quantity"],
            dish_info["aspect_scores"]["value_for_money"],
            dish_info["aspect_scores"]["freshness_and_packaging"]
        ]
        
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=scores,
            theta=aspects,
            fill='toself',
            name=selected_dish,
            line=dict(color='#E23744', width=2)
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1.0])),
            showlegend=False,
            title=f"Aspect Polarity Radar: {selected_dish}",
            height=340
        )
        st.plotly_chart(fig_radar, use_container_width=True)
        
    with col_d2:
        st.markdown(f"#### 🍽️ {dish_info['dish_name']}")
        st.metric("Total Mentions Analyzed", f"{dish_info['total_mentions_analyzed']:,}")
        st.progress(dish_info["overall_sentiment_positive_pct"] / 100.0, text=f"Positive Sentiment: {dish_info['overall_sentiment_positive_pct']}%")
        
        st.markdown("**🟢 Top Praise Drivers:**")
        for drv in dish_info["top_positive_drivers"]:
            st.markdown(f"- *{drv}*")
            
        st.markdown("**🔴 Top Churn Complaints:**")
        for cmp in dish_info["top_negative_drivers"]:
            st.markdown(f"- *{cmp}*")
            
    st.markdown("##### 🏆 Top Recommended Restaurants for this Dish")
    top_p_cols = st.columns(len(dish_info.get("top_recommended_places", [])))
    for i, p in enumerate(dish_info.get("top_recommended_places", [])):
        with top_p_cols[i]:
            st.success(f"**{p['name']}**\n\n⭐ {p['rating']} / 5.0 | 📍 {p['locality']}")

# ----------------- TAB 4: LIVE REVIEW ANALYZER -----------------
with tab4:
    st.subheader("Live RoBERTa / BERT Aspect-Based Sentiment Analysis")
    st.markdown("Paste any customer review below to extract **dish entities, aspect polarity, and transformer confidence** in real time.")
    
    review_input = st.text_area(
        "Customer Review Text",
        "The chicken biryani had incredible aroma and succulent meat, but 420 rs was too overpriced and the portion was tiny!",
        height=100
    )
    
    if st.button("🚀 Analyze Review with ABSA Model"):
        with st.spinner("Extracting aspects and running transformer classification..."):
            try:
                res = requests.post(
                    f"{api_base_url}/api/v1/sentiment/absa/analyze",
                    json={"text": review_input},
                    headers=get_auth_headers(),
                    timeout=5
                )
                if res.status_code == 200:
                    analysis = res.json()["data"]
                    
                    st.success("✅ Analysis Complete!")
                    st.markdown(f"**Identified Dish Entities:** `{'`, `'.join(analysis['detected_dishes'])}`")
                    st.markdown(f"**Overall Classification:** **{analysis['overall_sentiment']}** (Confidence: `{analysis['model_confidence'] * 100:.1f}%`)")
                    
                    st.markdown("#### Aspect Breakdown")
                    asp_cols = st.columns(4)
                    aspect_names = ["taste", "portion", "value", "freshness_prep"]
                    aspect_labels = ["Taste & Flavor", "Portion Size", "Value / Price", "Freshness / Prep"]
                    
                    for i, asp_key in enumerate(aspect_names):
                        asp_data = analysis["aspect_breakdown"][asp_key]
                        with asp_cols[i]:
                            pol = asp_data["aspect_polarity_score"]
                            color = "green" if pol > 0 else ("red" if pol < 0 else "gray")
                            st.markdown(f"""
                            <div style="border:1px solid #ddd; border-radius:8px; padding:12px; text-align:center;">
                                <h6>{aspect_labels[i]}</h6>
                                <h3 style="color:{color};">{asp_data['sentiment']}</h3>
                                <p style="font-size:0.85rem;">Polarity Score: <strong>{pol:+.2f}</strong></p>
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    st.error(f"Error {res.status_code}: {res.text}")
            except Exception as e:
                st.error(f"Request failed: {str(e)}")

# ----------------- TAB 5: TELEMETRY -----------------
with tab5:
    st.subheader("Client Credentials & Security Telemetry")
    st.markdown("View live connection audit parameters currently passed in HTTP headers:")
    
    if auth_status:
        st.json(auth_details)
    else:
        st.warning("Client is not currently authenticated with the API.")
        
    st.markdown("#### Sample Python Integration Code")
    st.code(f"""
import requests

headers = {{
    "X-API-Key": "{st.session_state['api_key']}",
    "X-Client-ID": "{st.session_state['client_id']}",
    "X-Client-Code": "{st.session_state['client_code']}",
    "User-Agent": "{st.session_state['user_agent']}"
}}

response = requests.get("{api_base_url}/api/v1/journey/funnel", headers=headers)
print(response.json())
""", language="python")
