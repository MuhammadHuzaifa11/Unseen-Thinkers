import pandas as pd

def process_csv(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file, encoding='latin1')
        for col in df.columns:
            if df[col].dtype == 'object':
                # Remove $, commas, and spaces, then convert to numeric
                clean_col = df[col].astype(str).str.replace(r'[$, ]', '', regex=True)
                df[col] = pd.to_numeric(clean_col, errors='ignore')
        cols = {col.lower(): col for col in df.columns}
        s_col = next((cols[c] for c in ['sales', 'revenue'] if c in cols), df.columns[0])
        p_col = next((cols[c] for c in ['profit', 'gain'] if c in cols), df.columns[1])
        cat_col = next((cols[c] for c in ['category', 'type'] if c in cols), df.columns[2])

        total_sales = df[s_col].sum()
        total_profit = df[p_col].sum()
        margin = (total_profit / total_sales) * 100 if total_sales != 0 else 0
        
        # Find top 3 losses for the Anomaly Detection requirement [cite: 32, 377]
        losses = df[df[p_col] < 0].sort_values(by=p_col).head(3)
        risk_list = [f"Loss in {row[cat_col]}: ${abs(row[p_col]):.0f}" for _, row in losses.iterrows()]

        # Structural Summary for LLM - keeping keys consistent with UI [cite: 66]
        vital_stats = {
            "financials": {
                "sales": f"${total_sales:,.0f}",
                "profit": f"${total_profit:,.0f}",
                "margin": f"{margin:.1f}%"
            },
            "risks": risk_list if risk_list else ["No significant losses detected."],
            "champions": {"category": str(df.groupby(cat_col)[s_col].sum().idxmax())},
            "scope": f"{len(df)} transactions"
        }
        
        return vital_stats, df, (s_col, p_col, cat_col)
    except Exception as e:
        raise RuntimeError(f"Data Error: {str(e)}")