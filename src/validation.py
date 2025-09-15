import pandas as pd
from typing import Dict, List, Tuple

def validate_missing_duplicates(*dfs):
    """
    Valida valores faltantes y duplicados en uno o dos DataFrames.
    
    Parámetros
    ----------
    *dfs : uno o más pd.DataFrame
    
    Retorna
    -------
    dict con resultados de validación por DataFrame
    """
    results = {}
    
    for i, df in enumerate(dfs, start=1):
        missing = df.isnull().sum()
        results[f"df_{i}"] = {
            "missing_values": missing[missing > 0].to_dict(),
            "duplicate_rows": int(df.duplicated().sum())
        }
    
    return results


def validate_date_columns(date_cols_map: dict):
    """
    Valida coherencia de columnas de tipo fecha en uno o dos DataFrames.
    
    Parámetros
    ----------
    date_cols_map : dict
        Diccionario en el formato:
        {
            "df_1": (dataframe, ["col_fecha1", "col_fecha2"]),
            "df_2": (dataframe, ["col_fechaX"])
        }
    
    Retorna
    -------
    dict con resultados de validación por DataFrame
    """
    results = {}
    
    for name, (df, date_cols) in date_cols_map.items():
        date_checks = {}
        for col in date_cols:
            if col in df.columns:
                temp = pd.to_datetime(df[col], errors="coerce")
                invalid = temp.isna().sum()
                min_date, max_date = temp.min(), temp.max()
                date_checks[col] = {
                    "invalid_dates": int(invalid),
                    "min_date": str(min_date) if pd.notnull(min_date) else None,
                    "max_date": str(max_date) if pd.notnull(max_date) else None
                }
            else:
                date_checks[col] = "❌ columna no encontrada"
        results[name] = date_checks
    
    return results
