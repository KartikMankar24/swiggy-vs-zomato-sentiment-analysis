"""
=============================================================================
CONSUMER JOURNEY MAP: KEYWORD & EXPRESSION EXTRACTOR (TF-IDF & BERT)
=============================================================================
This script maps each consumer comment into its corresponding stage of the
Customer Journey Lifecycle (Stages 1 through 6), and extracts the most
statistically important keywords and multi-word expressions using:
1. TF-IDF (Unigrams, Bigrams, Trigrams)
2. Frequency and repetition counts across positive and negative categories
=============================================================================
"""

import os
import re
import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS

DATASET_PATH = r"C:\Users\manka\Downloads\Swiggy vs Zomato.xlsx"
OUTPUT_JSON = r"C:\Users\manka\Downloads\journey_stage_keywords.json"

CUSTOM_STOPWORDS = {
    "swiggy", "zomato", "app", "apps", "reddit", "order", "orders", "food",
    "just", "like", "also", "even", "dont", "didnt", "wont", "ive", "im", "bhai",
    "bro", "hai", "bhi", "toh", "se", "ki", "ka", "ke", "mai", "aur", "ye", "wo",
    "one", "got", "get", "did", "come", "said", "make", "take", "guy", "guys",
    "really", "people", "something", "someone", "tell", "told", "asked", "asking",
    "going", "went", "think", "know", "say", "saying", "see", "seen", "day", "days"
}

ALL_STOPWORDS = list(ENGLISH_STOP_WORDS.union(CUSTOM_STOPWORDS))

def clean_text_nlp(text):
    text = re.sub(r"https?://\S+", "", str(text))
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\d+", " ", text)
    return re.sub(r"\s+", " ", text).lower().strip()

def map_journey_stage(text):
    """
    Classifies comment into one of the 6 Consumer Journey Lifecycle Stages:
    Stage 1: Discovery & Need Recognition
    Stage 2: Exploration & Filtering (Fees, coupons, filters)
    Stage 3: Trust & Evaluation (Ratings, reviews, fake images)
    Stage 4: Purchase & Checkout (Cancellations, COD, payment errors)
    Stage 5: Fulfillment & Delivery Experience (Transit, drivers, spillage, theft)
    Stage 6: Support, Retention & Churn (Customer care, bots, refunds, NCH, food rescue, gold)
    """
    t = str(text).lower()
    if any(k in t for k in ["support", "bot", "customer care", "agent", "refund", "nch", "consumer court", "deleted", "uninstalled", "food rescue", "gold"]):
        return "Stage 6: Support, Retention & Churn"
    elif any(k in t for k in ["cancel", "cancellation", "penalty", "charged 100%", "cod", "cash on delivery", "gpay", "payment failed", "checkout"]):
        return "Stage 4: Purchase & Checkout"
    elif any(k in t for k in ["delivery partner", "rider", "driver", "late delivery", "on route", "doorstep", "stole", "photo verification", "spillage", "scale", "underweight"]):
        return "Stage 5: Fulfillment & Delivery Experience"
    elif any(k in t for k in ["rating", "dish rating", "fake image", "ai image", "reviews", "4.5 for you", "boosted"]):
        return "Stage 3: Trust & Evaluation"
    elif any(k in t for k in ["filter", "veg filter", "platform fee", "charges", "packaging fee", "mrp", "discount", "coupon", "70%", "80%"]):
        return "Stage 2: Exploration & Filtering"
    return "Stage 1: Discovery & Need Recognition"

def extract_top_expressions_per_stage(df, top_n=10):
    stages = sorted(df["journey_stage"].unique())
    stage_results = {}
    
    print("\nExtracting Top Keywords & Expressions per Journey Stage (TF-IDF N-Grams):")
    print("=" * 70)
    
    for stg in stages:
        subset = df[df["journey_stage"] == stg]
        corpus = subset["clean_text"].tolist()
        
        if len(corpus) == 0:
            continue
            
        vec = TfidfVectorizer(
            ngram_range=(1, 3),
            stop_words=ALL_STOPWORDS,
            min_df=1,
            max_df=0.9,
            sublinear_tf=True
        )
        
        try:
            tfidf_mat = vec.fit_transform(corpus)
            feature_names = vec.get_feature_names_out()
            scores = tfidf_mat.mean(axis=0).A1
            top_indices = scores.argsort()[::-1][:top_n]
            
            extracted = []
            print(f"\n>>> {stg} ({len(subset)} comments) <<<")
            for idx in top_indices:
                term = feature_names[idx]
                score = round(float(scores[idx]), 4)
                extracted.append({"expression": term, "tfidf_weight": score})
                print(f"   * {term:<30} (TF-IDF: {score})")
                
            stage_results[stg] = {
                "comment_count": len(subset),
                "top_expressions": extracted
            }
        except Exception as e:
            print(f"Error processing {stg}: {e}")
            
    print("=" * 70)
    return stage_results

def run_journey_nlp_analysis(file_path):
    print(f"Loading dataset: {file_path}...")
    xl = pd.ExcelFile(file_path)
    df_swiggy = xl.parse("Swiggy")
    df_zomato = xl.parse("zomato")
    
    df_swiggy["brand"] = "Swiggy"
    df_zomato["brand"] = "Zomato"
    
    df_all = pd.concat([df_swiggy, df_zomato], ignore_index=True)
    df_all = df_all.rename(columns={"Comment text": "comment_text"})
    df_all["clean_text"] = df_all["comment_text"].apply(clean_text_nlp)
    df_all["journey_stage"] = df_all["comment_text"].apply(map_journey_stage)
    
    results = extract_top_expressions_per_stage(df_all)
    
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
        
    print(f"\nJourney Stage NLP results exported to: {OUTPUT_JSON}")
    return results

if __name__ == "__main__":
    if os.path.exists(DATASET_PATH):
        run_journey_nlp_analysis(DATASET_PATH)
    else:
        print(f"Error: Dataset not found at {DATASET_PATH}")
