"""
=============================================================================
SENTIMENT ANALYSIS FOR SWIGGY AND ZOMATO COMMENTS
=============================================================================
This script performs sentiment analysis on consumer comments from the uploaded
dataset ('Swiggy vs Zomato.xlsx'). It specifically identifies and segments
comments mentioning the keywords 'swiggy' and 'zomato', calculates positive,
negative, and neutral sentiment distributions, and exports a summary.
=============================================================================
"""

import os
import re
import json
import pandas as pd

# File Paths
DATASET_PATH = r"C:\Users\manka\Downloads\Swiggy vs Zomato.xlsx"
OUTPUT_JSON = r"C:\Users\manka\Downloads\sentiment_analysis_results.json"

def has_word(text, word):
    """Checks whether a whole word exists in text (case-insensitive)."""
    if not isinstance(text, str):
        return False
    return bool(re.search(r"\b" + re.escape(word) + r"\b", text, re.IGNORECASE))

def analyze_comment_sentiment(text):
    """
    Computes sentiment polarity and label (Positive, Negative, Neutral)
    using domain-specific lexicons tailored for food delivery & quick commerce.
    """
    t = str(text).lower()
    
    pos_words = [
        "good", "great", "love", "loved", "saved", "discount", "lucky", "helpful",
        "refund received", "refunded", "resolved", "solution", "tasty", "delicious",
        "kudos", "respect", "awesome", "decent", "happy", "better", "best", "useful",
        "win", "free cash", "proper", "generous", "heartwarming", "polite", "cheaper"
    ]
    
    neg_words = [
        "scam", "scammed", "pathetic", "worst", "chutiya", "loot", "fraud", "stole",
        "penalty", "cancel", "cancellation", "harassment", "abused", "creepy", "threaten",
        "fight", "lawsuit", "complaint", "nch", "consumer court", "terrible", "stale",
        "cold", "soggy", "bug", "glitch", "fake", "dirty", "uninstalled", "deleted",
        "shitty", "disappointed", "underweight", "spilled", "hate", "robbery", "dumbest",
        "bad", "fuck", "bkl", "overpriced", "expensive", "rip off", "waste", "stuck"
    ]
    
    p = sum(1 for w in pos_words if w in t)
    n = sum(1 for w in neg_words if w in t)
    
    # Contextual high-severity friction weighting
    if any(k in t for k in ["charged 100%", "balance is negative", "not delivered", "never came", "stole my", "did nothing"]):
        n += 2
    if any(k in t for k in ["refund was processed", "initiated a refund", "got full refund", "always got good food"]):
        p += 2
        
    diff = p - n
    if diff > 0:
        return "Positive", round(min(1.0, 0.4 + diff * 0.15), 2)
    elif diff < 0:
        return "Negative", round(max(-1.0, -0.4 + diff * 0.15), 2)
    return "Neutral", 0.0

def run_sentiment_pipeline(file_path):
    print(f"Loading dataset: {file_path}...")
    xl = pd.ExcelFile(file_path)
    df_swiggy = xl.parse("Swiggy")
    df_zomato = xl.parse("zomato")
    
    df_swiggy["brand_sheet"] = "Swiggy"
    df_zomato["brand_sheet"] = "Zomato"
    
    df_all = pd.concat([df_swiggy, df_zomato], ignore_index=True)
    df_all = df_all.rename(columns={"Comment text": "comment_text"})
    df_all["comment_text"] = df_all["comment_text"].astype(str).str.strip()
    
    # 1. Identify keyword presence
    df_all["mentions_swiggy"] = df_all["comment_text"].apply(lambda t: has_word(t, "swiggy"))
    df_all["mentions_zomato"] = df_all["comment_text"].apply(lambda t: has_word(t, "zomato"))
    
    # 2. Score sentiment
    print("Scoring sentiment across all comments...")
    res = df_all["comment_text"].apply(analyze_comment_sentiment)
    df_all["sentiment"] = [r[0] for r in res]
    df_all["polarity_score"] = [r[1] for r in res]
    
    # 3. Compute statistics for mentions
    def calculate_stats(df_subset, label):
        total = len(df_subset)
        counts = df_subset["sentiment"].value_counts().to_dict()
        pos = counts.get("Positive", 0)
        neg = counts.get("Negative", 0)
        neu = counts.get("Neutral", 0)
        return {
            "category": label,
            "total_comments": total,
            "positive_count": pos,
            "positive_percentage": round((pos / max(1, total)) * 100, 2),
            "negative_count": neg,
            "negative_percentage": round((neg / max(1, total)) * 100, 2),
            "neutral_count": neu,
            "neutral_percentage": round((neu / max(1, total)) * 100, 2)
        }
        
    swiggy_stats = calculate_stats(df_all[df_all["mentions_swiggy"]], "Mentions 'Swiggy'")
    zomato_stats = calculate_stats(df_all[df_all["mentions_zomato"]], "Mentions 'Zomato'")
    both_stats = calculate_stats(df_all[df_all["mentions_swiggy"] & df_all["mentions_zomato"]], "Mentions BOTH Brands")
    
    summary = {
        "swiggy": swiggy_stats,
        "zomato": zomato_stats,
        "both": both_stats
    }
    
    print("\n" + "="*65)
    print(" SENTIMENT ANALYSIS RESULTS")
    print("="*65)
    for k, v in summary.items():
        print(f"\n[{v['category']}] (Total: {v['total_comments']})")
        print(f"  * Negative: {v['negative_count']} ({v['negative_percentage']}%)")
        print(f"  * Positive: {v['positive_count']} ({v['positive_percentage']}%)")
        print(f"  * Neutral:  {v['neutral_count']} ({v['neutral_percentage']}%)")
    print("="*65)
    
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"\nResults saved to: {OUTPUT_JSON}")
    return df_all, summary

if __name__ == "__main__":
    if os.path.exists(DATASET_PATH):
        run_sentiment_pipeline(DATASET_PATH)
    else:
        print(f"Error: Dataset not found at {DATASET_PATH}")
