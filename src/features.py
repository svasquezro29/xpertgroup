
import pandas as pd
from typing import Optional

def summarize_customer_activity(
    table: pd.DataFrame,
    cutoff: Optional[str] = None,
    window_days: int = 180,
    fillna: bool = True
) -> pd.DataFrame:
    """
    Devuelve last_order_date, recency_days (si cutoff),
    frequency_{window_days}d y monetary_{window_days}d por customer_id.

    table debe contener al menos ['customer_id', 'order_date'].
    Puede contener opcionalmente 'order_id' y 'order_amount'.
    """
    df = table.copy()
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')

    # Lista de clientes 
    customers = pd.DataFrame({'customer_id': df['customer_id'].unique()})

    # Filtrar hasta cutoff 
    if cutoff is not None:
        cutoff_ts = pd.to_datetime(cutoff)
        df_pre = df[df['order_date'] <= cutoff_ts].copy()
    else:
        cutoff_ts = None
        df_pre = df.copy()

    # Última compra por cliente 
    last = (
        df_pre.groupby('customer_id', as_index=False)['order_date']
              .max()
              .rename(columns={'order_date': 'last_order_date'})
    )

    # Ventana rolling: (cutoff - window_days, cutoff]
    if cutoff_ts is not None:
        window_start = cutoff_ts - pd.Timedelta(days=window_days)
        mask = (df['order_date'] > window_start) & (df['order_date'] <= cutoff_ts)
        df_window = df.loc[mask].copy()
    else:
        df_window = pd.DataFrame(columns=df.columns)  # vacío si no hay cutoff

    # frequency en la ventana de 180d
    if not df_window.empty:
        if 'order_id' in df_window.columns:
            freq = (df_window.groupby('customer_id', as_index=False)['order_id']
                            .nunique()
                            .rename(columns={'order_id': f'frequency_{window_days}d'}))
        else:
            freq = (df_window.groupby('customer_id').size()
                            .reset_index(name=f'frequency_{window_days}d'))
    else:
        freq = pd.DataFrame(columns=['customer_id', f'frequency_{window_days}d'])

    # monetary en la ventana de 180d
    if not df_window.empty and 'order_amount' in df_window.columns:
        mon = (df_window.groupby('customer_id', as_index=False)['order_amount']
                       .sum()
                       .rename(columns={'order_amount': f'monetary_{window_days}d'}))
    else:
        mon = pd.DataFrame(columns=['customer_id', f'monetary_{window_days}d'])

    # Merge todo
    summary = customers.merge(last, on='customer_id', how='left') \
                       .merge(freq, on='customer_id', how='left') \
                       .merge(mon, on='customer_id', how='left')

    # Recency si se pidió
    if cutoff_ts is not None:
        summary['recency_days'] = (cutoff_ts - pd.to_datetime(summary['last_order_date'])).dt.days

    # Rellenar NaNs si fillna=True
    if fillna:
        for c in [f'frequency_{window_days}d', f'monetary_{window_days}d', 'recency_days']:
            if c in summary.columns:
                summary[c] = summary[c].fillna(0)

    return summary.sort_values('customer_id').reset_index(drop=True)
