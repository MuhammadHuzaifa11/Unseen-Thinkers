# AI Workflow & Report Generator

### Developed by Unseen Thinkers

## Overview
Unseen Thinkers presents a rapid, AI-driven business intelligence tool designed for non-technical users. This application automates the analysis of complex CSV files, transforming raw data into strategic insights in under 5 seconds.

## Key Features
* **Instant Executive Summary**: Get a high-level financial overview of your data in seconds.
* **Automated Anomaly Detection**: Quickly identify systemic risks and financial losses within your transactions.
* **Strategic Action Planner**: Receive actionable, data-driven business recommendations to boost profit.
* **Deep-Dive Assistant**: A conversational AI powered by Groq (Llama 3) for real-time querying of specific data nuances.
* **One-Click Export**: Generate a professional text-based report for immediate business use.

## Technical Stack
* **Interface**: Streamlit
* **Data Engine**: Pandas (with fuzzy column mapping for flexible CSV uploads)
* **Analysis AI**: Google Gemini Flash
* **Chat AI**: Groq (Llama 3.3)

## How to Run
1. Clone this repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file and add your `GEMINI_API_KEY` and `GROQ_API_KEY`.
4. Run the app: `streamlit run main.py`

---
*Built for the [Engineers code] to empower managers through speed and strategic AI.*