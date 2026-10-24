import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(
    page_title="Swiggy vs Zomato: Keyword & NLP Analysis Dashboard",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_PATH = r"C:\Users\manka\Downloads\Swiggy_vs_Zomato_Sentiment_Report.xlsx"
JSON_PATH = r"C:\Users\manka\.gemini\antigravity\scratch\zomato-consumer-journey-api\data\swiggy_zomato_keyword_sentiment.json"
NLP_JSON_PATH = r"C:\Users\manka\.gemini\antigravity\scratch\zomato-consumer-journey-api\data\tfidf_bert_keyword_extraction.json"

st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #FC8019, #E23744);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .metric-box-swiggy {
        background-color: #FFF6EE;
        border-radius: 8px;
        padding: 14px;
        border-left: 4px solid #FC8019;
    }
    .metric-box-zomato {
        background-color: #FDF2F2;
        border-radius: 8px;
        padding: 14px;
        border-left: 4px solid #E23744;
    }
    .metric-box-both {
        background-color: #F4F6F9;
        border-radius: 8px;
        padding: 14px;
        border-left: 4px solid #2B579A;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    xl = pd.ExcelFile(DATA_PATH)
    df_swiggy = xl.parse("Comments Mentioning Swiggy")
    df_zomato = xl.parse("Comments Mentioning Zomato")
    df_both = xl.parse("Mentioning Both Brands")
    
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        summary = json.load(f)
        
    nlp_data = {}
    if os.path.exists(NLP_JSON_PATH):
        with open(NLP_JSON_PATH, "r", encoding="utf-8") as f:
            nlp_data = json.load(f)
            
    return df_swiggy, df_zomato, df_both, summary, nlp_data

df_swiggy, df_zomato, df_both, summary, nlp_data = load_data()

st.markdown('<div class="main-title">Swiggy vs Zomato: Keyword & NLP Expression Intelligence</div>', unsafe_allow_html=True)
st.markdown("Analyzing positive, negative, and neutral feedback mentioning **'swiggy'** and **'zomato'** using **TF-IDF & BERT Contextual Embeddings**.")
st.markdown("---")

tab1, tab2, tab3 = st.tabs([
    "📊 Sentiment Distribution & KPIs",
    "🧠 TF-IDF & BERT Keyphrases",
    "🔍 Filterable Comments Explorer"
])

# ----------------- TAB 1: KPI & SENTIMENT -----------------
with tab1:
    s_stats = summary["comments_mentioning_swiggy"]
    z_stats = summary["comments_mentioning_zomato"]
    b_stats = summary["comments_mentioning_both"]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="metric-box-swiggy">
            <h4 style="color:#FC8019; margin:0;">🟠 Mentioning "Swiggy"</h4>
            <h2 style="margin:4px 0;">Total: {}</h2>
            <p style="margin:0;"><strong>Negative:</strong> <span style="color:#C0392B;">{} ({}%)</span><br>
            <strong>Positive:</strong> <span style="color:#27AE60;">{} ({}%)</span><br>
            <strong>Neutral:</strong> {} ({}%)</p>
        </div>
        """.format(
            s_stats["total"],
            s_stats["negative"], s_stats["negative_pct"],
            s_stats["positive"], s_stats["positive_pct"],
            s_stats["neutral"], s_stats["neutral_pct"]
        ), unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-box-zomato">
            <h4 style="color:#E23744; margin:0;">🔴 Mentioning "Zomato"</h4>
            <h2 style="margin:4px 0;">Total: {}</h2>
            <p style="margin:0;"><strong>Negative:</strong> <span style="color:#C0392B;">{} ({}%)</span><br>
            <strong>Positive:</strong> <span style="color:#27AE60;">{} ({}%)</span><br>
            <strong>Neutral:</strong> {} ({}%)</p>
        </div>
        """.format(
            z_stats["total"],
            z_stats["negative"], z_stats["negative_pct"],
            z_stats["positive"], z_stats["positive_pct"],
            z_stats["neutral"], z_stats["neutral_pct"]
        ), unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-box-both">
            <h4 style="color:#2B579A; margin:0;">⚖️ Mentioning BOTH Brands</h4>
            <h2 style="margin:4px 0;">Total: {}</h2>
            <p style="margin:0;"><strong>Negative:</strong> <span style="color:#C0392B;">{} ({}%)</span><br>
            <strong>Positive:</strong> <span style="color:#27AE60;">{} ({}%)</span><br>
            <strong>Neutral:</strong> {} ({}%)</p>
        </div>
        """.format(
            b_stats["total"],
            b_stats["negative"], b_stats["negative_pct"],
            b_stats["positive"], b_stats["positive_pct"],
            b_stats["neutral"], b_stats["neutral_pct"]
        ), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.subheader("Absolute Number of Comments")
        chart_df = pd.DataFrame({
            "Keyword Mentioned": ["Mentioning 'Swiggy'", "Mentioning 'Swiggy'", "Mentioning 'Swiggy'",
                                  "Mentioning 'Zomato'", "Mentioning 'Zomato'", "Mentioning 'Zomato'",
                                  "Mentioning Both", "Mentioning Both", "Mentioning Both"],
            "Sentiment": ["Negative", "Positive", "Neutral", "Negative", "Positive", "Neutral", "Negative", "Positive", "Neutral"],
            "Count": [
                s_stats["negative"], s_stats["positive"], s_stats["neutral"],
                z_stats["negative"], z_stats["positive"], z_stats["neutral"],
                b_stats["negative"], b_stats["positive"], b_stats["neutral"]
            ]
        })
        fig_bar = px.bar(
            chart_df,
            x="Keyword Mentioned",
            y="Count",
            color="Sentiment",
            barmode="group",
            color_discrete_map={"Negative": "#E23744", "Positive": "#27AE60", "Neutral": "#95A5A6"},
            text="Count",
            height=360
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_chart2:
        st.subheader("Sentiment Percentage (%)")
        pct_df = pd.DataFrame({
            "Keyword": ["Mentioning 'Swiggy'", "Mentioning 'Swiggy'", "Mentioning 'Swiggy'",
                        "Mentioning 'Zomato'", "Mentioning 'Zomato'", "Mentioning 'Zomato'"],
            "Sentiment": ["Negative %", "Positive %", "Neutral %", "Negative %", "Positive %", "Neutral %"],
            "Percentage": [
                s_stats["negative_pct"], s_stats["positive_pct"], s_stats["neutral_pct"],
                z_stats["negative_pct"], z_stats["positive_pct"], z_stats["neutral_pct"]
            ]
        })
        fig_pct = px.bar(
            pct_df,
            x="Keyword",
            y="Percentage",
            color="Sentiment",
            color_discrete_map={"Negative %": "#E23744", "Positive %": "#27AE60", "Neutral %": "#BDC3C7"},
            text="Percentage",
            height=360
        )
        st.plotly_chart(fig_pct, use_container_width=True)

# ----------------- TAB 2: TF-IDF & BERT NLP -----------------
with tab2:
    st.subheader("TF-IDF Keywords & BERT Semantic Expressions")
    st.markdown("Extracted terms demonstrating what drives **Positive**, **Negative**, and **Neutral** commentary.")
    
    seg_choice = st.selectbox(
        "Select Brand & Sentiment Segment",
        [
            "Swiggy - Negative (Friction & Complaints)",
            "Swiggy - Positive (Delight & Value)",
            "Swiggy - Neutral (Inquiries & General)",
            "Zomato - Negative (Friction & Complaints)",
            "Zomato - Positive (Delight & Value)",
            "Zomato - Neutral (Inquiries & General)"
        ]
    )
    
    key_mapping = {
        "Swiggy - Negative (Friction & Complaints)": "Swiggy_Negative",
        "Swiggy - Positive (Delight & Value)": "Swiggy_Positive",
        "Swiggy - Neutral (Inquiries & General)": "Swiggy_Neutral",
        "Zomato - Negative (Friction & Complaints)": "Zomato_Negative",
        "Zomato - Positive (Delight & Value)": "Zomato_Positive",
        "Zomato - Neutral (Inquiries & General)": "Zomato_Neutral",
    }
    
    selected_key = key_mapping[seg_choice]
    seg_data = nlp_data.get(selected_key, {})
    
    if seg_data:
        st.info(f"**Sample Size:** `{seg_data['comment_count']} comments` analyzed in this segment.")
        
        c_k1, c_k2, c_k3 = st.columns(3)
        with c_k1:
            st.markdown("##### 🔤 Top TF-IDF Unigrams")
            df_u = pd.DataFrame(seg_data["top_keywords_unigrams"])
            if not df_u.empty:
                df_u.columns = ["Keyword", "TF-IDF Weight"]
                st.dataframe(df_u, use_container_width=True, hide_index=True)
                
        with c_k2:
            st.markdown("##### 🔗 Top Multi-Word Expressions (TF-IDF)")
            df_ng = pd.DataFrame(seg_data["top_expressions_tfidf"])
            if not df_ng.empty:
                df_ng.columns = ["Expression (N-gram)", "TF-IDF Weight"]
                st.dataframe(df_ng, use_container_width=True, hide_index=True)
                
        with c_k3:
            st.markdown("##### 🤖 Top BERT Contextual Expressions")
            df_b = pd.DataFrame(seg_data["top_contextual_bert_expressions"])
            if not df_b.empty:
                df_b.columns = ["Semantic Expression", "BERT Similarity"]
                st.dataframe(df_b, use_container_width=True, hide_index=True)

# ----------------- TAB 3: EXPLORER -----------------
with tab3:
    st.subheader("Filter & Read Comments")
    
    c_f1, c_f2, c_f3 = st.columns([2, 2, 3])
    with c_f1:
        pool_choice = st.selectbox("Select Brand Filter", ["Mentioning 'Swiggy' (224)", "Mentioning 'Zomato' (191)", "Mentioning Both (60)"])
    with c_f2:
        filter_sent = st.selectbox("Sentiment Filter", ["All Sentiments", "Negative Only", "Positive Only", "Neutral Only"])
    with c_f3:
        search_kw = st.text_input("Search Text", "", placeholder="e.g. cancellation, fee, refund, photo, bot")

    if "Swiggy" in pool_choice and "Both" not in pool_choice:
        active_df = df_swiggy.copy()
    elif "Zomato" in pool_choice:
        active_df = df_zomato.copy()
    else:
        active_df = df_both.copy()

    if filter_sent == "Negative Only":
        active_df = active_df[active_df["Sentiment"] == "Negative"]
    elif filter_sent == "Positive Only":
        active_df = active_df[active_df["Sentiment"] == "Positive"]
    elif filter_sent == "Neutral Only":
        active_df = active_df[active_df["Sentiment"] == "Neutral"]

    if search_kw.strip():
        active_df = active_df[active_df["Comment Text"].str.contains(search_kw.strip(), case=False, na=False)]

    st.markdown(f"**Showing {len(active_df)} comments:**")
    st.dataframe(active_df[["#", "Sentiment", "Polarity Score", "Comment Text"]], use_container_width=True, height=420)
