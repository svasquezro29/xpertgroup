import pandas as pd
from typing import Dict, List, Tuple

def summary_stats(df: pd.DataFrame) -> dict:
    """
    Genera un resumen estadístico de variables numéricas y categóricas.
    
    Args:
        df (pd.DataFrame): DataFrame de entrada.
    
    Returns:
        dict: Diccionario con resúmenes por tipo de variable.
    """
    results = {}

    # =====================
    # Variables Numéricas
    # =====================
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
    if len(numeric_cols) > 0:
        results["numeric"] = df[numeric_cols].agg(
            ["count", "mean", "min", "max"]
        ).transpose()
    else:
        results["numeric"] = "No numeric columns found."

    # =====================
    # Variables Categóricas
    # =====================
    cat_cols = df.select_dtypes(include=["object", "category"]).columns
    cat_summary = {}
    
    for col in cat_cols:
        counts = df[col].value_counts(dropna=False)
        total = counts.sum()
        top_cat = counts.index[0]
        freq = counts.iloc[0]
        perc = (freq / total) * 100
        
        cat_summary[col] = {
            "count": total,
            "unique_categories": df[col].nunique(dropna=False),
            "top_category": top_cat,
            "top_count": freq,
            "top_percentage": round(perc, 2)
        }
    
    results["categorical"] = pd.DataFrame(cat_summary).transpose() if cat_summary else "No categorical columns found."

    return results
