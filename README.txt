=============================================================================
SWIGGY VS ZOMATO: COMPLETE SENTIMENT & USER JOURNEY MAP PACKAGE
=============================================================================

This package contains all requested deliverables:

1. RAW DATASET:
   - 'Swiggy vs Zomato.xlsx'
     Contains 207 Swiggy comments and 153 Zomato comments (including headers).

2. JUPYTER NOTEBOOK FOR SENTIMENT ANALYSIS:
   - 'sentiment_analysis.ipynb'
     Interactive Jupyter Notebook with step-by-step documentation and charts:
     * Parses the Excel dataset
     * Detects mentions of 'swiggy', 'zomato', and both
     * Computes positive, negative, and neutral sentiment distributions
     * Renders comparative matplotlib charts
     * Exports summary to JSON

3. JUPYTER NOTEBOOK FOR USER JOURNEY MAP KEYWORDS & EXPRESSIONS:
   - 'journey_important_words_expressions.ipynb'
     Interactive Jupyter Notebook with step-by-step documentation and charts:
     * Maps comments across 6 User Journey Stages:
       Stage 1: Discovery & Need Recognition
       Stage 2: Exploration & Filtering
       Stage 3: Trust & Evaluation
       Stage 4: Purchase & Checkout
       Stage 5: Fulfillment & Delivery
       Stage 6: Support, Retention & Churn
     * Extracts top TF-IDF n-grams (unigrams, bigrams, trigrams) and BERT expressions
     * Plots horizontal bar charts of key expressions in high-friction stages
     * Exports results to JSON

4. EXCEL WORKBOOK WITH SIX TABS (Positive, Negative, Neutral for each brand):
   - 'Swiggy_Zomato_6_Tabs_Sentiment.xlsx'
     Tabs included:
     * Swiggy_Positive (23 comments)
     * Swiggy_Negative (68 comments)
     * Swiggy_Neutral (115 comments)
     * Zomato_Positive (24 comments)
     * Zomato_Negative (34 comments)
     * Zomato_Neutral (94 comments)

5. ANALYTICAL REPORT IN MICROSOFT WORD:
   - 'Swiggy_vs_Zomato_Sentiment_Report.docx'
     Contains executive summary scorecards, stage-by-stage repetition analysis,
     top keywords for all six sentiments, and actionable leadership roadmaps.

6. VERCEL LIVE DASHBOARD:
   - 'vercel_live_dashboard/index.html'
   - 'vercel_live_dashboard/vercel.json'
   - 'vercel_live_dashboard/README_VERCEL.md'
     Deploy to Vercel via 'vercel --prod' for an instant public live URL!
=============================================================================
