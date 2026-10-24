# 🍽️ Swiggy vs Zomato: Consumer Journey Mapping & Sentiment Analysis Engine

[![Live Demo](https://img.shields.io/badge/Live_Dashboard-Vercel-black?style=for-the-badge&logo=vercel)](https://swiggy-zomato-sentiment-cjm-dashboa.vercel.app)
[![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)](https://python.org)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebooks-orange?style=for-the-badge&logo=jupyter)](https://jupyter.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-REST_API-009688?style=for-the-badge&logo=fastapi)](http://127.0.0.1:8000/docs)
[![Streamlit](https://img.shields.io/badge/Streamlit-Interactive_UI-FF4B4B?style=for-the-badge&logo=streamlit)](http://localhost:8502)

> **Live Interactive Web Dashboard**: [https://swiggy-zomato-sentiment-cjm-dashboa.vercel.app](https://swiggy-zomato-sentiment-cjm-dashboa.vercel.app)

An end-to-end data science and natural language processing (NLP) project that maps food delivery consumer experiences into a **6-Stage Consumer Journey Map (CJM)**, performs **Aspect-Based Sentiment Analysis (ABSA)**, and extracts distinctive multi-word expressions using **TF-IDF N-Grams** and **BERT KeyBERT Contextual Embeddings** across 358 consumer comments from Swiggy and Zomato.

---

## 🚀 Live Dashboard Preview

Access the live interactive dashboard deployed on Vercel:
👉 **[Open Live Dashboard](https://swiggy-zomato-sentiment-cjm-dashboa.vercel.app)**

Features of the Live Dashboard:
* **Interactive Sentiment Scorecards**: Real-time filtering for Swiggy, Zomato, and Co-mentions.
* **Journey Lifecycle Visualizer**: Stage-by-stage distribution, negative friction hotspots, and positive retention drivers.
* **Top Linguistic Markers**: Ranked TF-IDF and BERT keyphrases across all 6 sentiment segments.
* **Live Comment Explorer**: Searchable, filterable table of consumer commentary with polarity tags.

---

## 📊 Executive Summary & Keyword Scorecard

Empirical evaluation of 358 consumer comments (`Swiggy vs Zomato.xlsx`):

| Keyword Category | Total Comments | Negative Count (%) | Positive Count (%) | Neutral Count (%) |
| :--- | :---: | :---: | :---: | :---: |
| **Mentioning 'Swiggy'** | 224 | **74 (33.04%)** | 29 (12.95%) | 121 (54.02%) |
| **Mentioning 'Zomato'** | 191 | **42 (21.99%)** | 29 (15.18%) | 120 (62.83%) |
| **Mentioning BOTH Brands** | 60 | **15 (25.00%)** | 11 (18.33%) | 34 (56.67%) |

### 🔍 Key Empirical Finding
* **Swiggy** experiences a **50% higher rate of negative sentiment (33.04%)** than Zomato (21.99%), driven primarily by its rigid 100% cancellation penalty and automated chatbot deflection loops.
* **Zomato** leads in customer delight and neutral goodwill (+3.4% higher delight), bolstered by its viral **Food Rescue** initiative (70–80% off canceled orders) and ₹1 Gold renewal offers.

---

## 🗺️ Consumer Journey Mapping (CJM) Framework

The consumer journey is modeled across 6 distinct lifecycle stages:

```
[Stage 1: Discovery & Need] ➔ [Stage 2: Exploration & Filtering] ➔ [Stage 3: Trust & Evaluation]
                                                                        ⬇
[Stage 6: Support & Retention] ⬅ [Stage 5: Fulfillment & Delivery] ⬅ [Stage 4: Purchase & Checkout]
```

| Lifecycle Stage | Share of Comments | Prominent Keywords & N-Grams | Sentiment Repetition Dynamics |
| :--- | :---: | :--- | :--- |
| **Stage 1: Discovery & Need** | 14% | restaurant, menu, cravings, local cafe, delivery fee | Low repetition; primarily neutral intent. |
| **Stage 2: Exploration & Filtering** | 18% | veg filter bug, chicken in veg, platform fee, coupons, free cash | Moderate positive repetitions on deals; negative spikes on dietary bugs. |
| **Stage 3: Trust & Evaluation** | 16% | rating mismatch, 4.5 for you, fake AI image, reviews | High negative repetition on deceptive cloud kitchen AI photos. |
| **Stage 4: Purchase & Checkout** | 22% | cancellation fee, charged 100%, negative balance, 23 COD fee | **HIGHEST SEVERITY NEGATIVE REPETITION**: 100% penalty is the #1 churn driver. |
| **Stage 5: Fulfillment & Delivery** | 28% | late delivery, driver, stole food, photo proof scam, spillage | **HIGH LOGISTICS REPETITION**: Delivery delays and photo verification theft. |
| **Stage 6: Support & Retention** | 34% | Pos: food rescue 80%, gold 1 rs, refund<br>Neg: bot loop, muzammil, nch court | **HIGHEST OVERALL VOLUME**: Polarized between support outrage and loyalty praise. |

### 🎯 Where Words Repeat Most
* **Negative Repetitions**: Peak in **Stage 4 (Purchase & Checkout)** (*"100% cancellation fee"*, *"negative balance"*, *"penalty"*) and **Stage 6 (Support & Dispute)** (*"bot deflection"*, *"muzammil"*, *"refund stuck"*, *"escalated to NCH"*).
* **Positive Repetitions**: Peak in **Stage 6 (Loyalty & Retention)** (*"food rescue 80% off"*, *"gold renew 1 rs"*, *"prompt refund"*) and **Stage 2 (Exploration)** (*"free cash"*, *"shreshtho pujo"*).

---

## 🔤 Most Important Words & Expressions (TF-IDF & BERT)

| Sentiment Segment | Top TF-IDF Unigrams | Top Multi-Word Expressions (TF-IDF) | Top BERT Contextual Expressions |
| :--- | :--- | :--- | :--- |
| **1. Swiggy Negative** | cancellation, penalty, refund, instamart, charges | cancellation fees, customer care, negative balance | aint refunding called nch, absolutely unhelpful online payment |
| **2. Swiggy Positive** | discount, refund, cash, coupon, free, happy | free cash, shreshtho pujo, good food, fast delivery | blinkit despite flat discount, better gets free delivery |
| **3. Swiggy Neutral** | delivery, restaurant, tapes, driver, partner | delivery driver, customer support, packaging charges | clubbing stop smartass, delivery partner assignment |
| **4. Zomato Negative** | service, support, scammed, fee, scale, photo | worst cx service, photo verification, cod fee | basically looting customer restaurant, photo bypass |
| **5. Zomato Positive** | rescue, deal, gold, refund, saved, lucky | food rescue, gold membership, great deal | claimed food rescue order, gold membership renew rupee |
| **6. Zomato Neutral** | tip, rating, driver, delivery, code, cash | qr code, cash delivery, rating average | case cash delivery wastage, rating calculation window |

---

## 🛠️ Prioritized Leadership Action Roadmaps

### 🔴 Swiggy Priorities
1. **Reform 100% Cancellation Penalty (Urgent Churn Fix)**: Introduce a 60-second zero-penalty grace window. Charge only nominal kitchen prep fees if canceled before food is cooked, eliminating negative wallet balances (-₹450 to -₹1,100).
2. **Overhaul Support Chatbot Loops ('Muzammil')**: Implement automated escalation triggers for damaged items and repeat queries to connect users to human agents within two prompts.
3. **Instamart Freshness & Pricing Audit**: Enforce strict dark store quality control for perishables and audit pricing algorithms against legal MRP limits.
4. **Transparent Delivery Grouping**: Show multi-stop rider routes clearly on maps and guarantee direct dispatch for Swiggy One and Black members.

### 🟢 Zomato Priorities
1. **Eliminate Doorstep Photo-Theft Scam (Urgent)**: Replace photo-only drop-offs with a mandatory 4-digit customer OTP or QR scan upon physical handover.
2. **Re-evaluate the ₹23 COD Fee**: Remove punitive cash-on-delivery surcharges and incentivize digital prepayments through reward points instead.
3. **Ban Deceptive AI-Generated Food Images**: Require actual, unedited food photography with clear portion/weight descriptions on all listings.
4. **Standardize Cooked Portion Weights**: Mandate net cooked weights or piece counts on cloud kitchen menus to address portion discrepancies.

---

## 📁 Repository Structure

```
├── sentiment_analysis.ipynb              # Jupyter Notebook: Sentiment scoring & charts
├── journey_important_words_expressions.ipynb # Jupyter Notebook: Journey stage NLP extraction
├── sentiment_analysis.py                 # Standalone sentiment analysis engine
├── journey_important_words_expressions.py# Standalone journey map NLP extractor
├── swiggy_zomato_dashboard.py            # Streamlit interactive keyword dashboard
├── app_dashboard.py                      # Streamlit CJM & ABSA dashboard
├── main.py                               # FastAPI REST backend with client auth
├── auth.py                               # API Key & client header authentication
├── dish_absa_engine.py                   # Aspect-based sentiment analysis engine
├── index.html                            # Interactive web dashboard (Vercel & GitHub Pages)
├── vercel.json                           # Vercel deployment configuration
├── Swiggy vs Zomato.xlsx                 # Original raw dataset (358 comments)
├── Swiggy_Zomato_6_Tabs_Sentiment.xlsx   # 6-tab formatted sentiment workbook
├── Swiggy_vs_Zomato_Sentiment_Report.docx# Full analytical report in Word format
├── Swiggy_Zomato_Analysis_Complete_Package.zip # Master deliverable package
├── requirements.txt                      # Project dependencies
└── README.md                             # Project documentation
```

---

## ⚙️ Installation & Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/KartikMankar24/swiggy-vs-zomato-sentiment-analysis.git
cd swiggy-vs-zomato-sentiment-analysis
```

### 2. Set Up Virtual Environment & Dependencies
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
```

### 3. Run the Jupyter Notebooks
```bash
jupyter notebook sentiment_analysis.ipynb
# or
jupyter notebook journey_important_words_expressions.ipynb
```

### 4. Run the Streamlit Dashboard
```bash
streamlit run swiggy_zomato_dashboard.py
```
Open [http://localhost:8502](http://localhost:8502) in your browser.

### 5. Run the FastAPI REST Backend
```bash
uvicorn main:app --reload --port 8000
```
Interactive API docs available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

---

## 📜 License
This project is licensed under the MIT License - feel free to use and adapt for academic and professional analytics.
