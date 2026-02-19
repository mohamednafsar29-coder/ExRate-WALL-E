# ExRate-WALL-E
💹 Ex-Rate WALL-E: RAG-Powered Forex Intelligence
Ex-Rate WALL-E is a professional-grade Decision Support System (DSS) designed to analyze 10 years of USD-INR historical exchange rate data (2016-2026). By combining Retrieval-Augmented Generation (RAG) with a high-performance Fintech UI, this tool transforms raw currency ledgers into actionable economic insights.

🚀 Key Features
RAG-Driven Analysis: Uses a Vector Database to retrieve exact historical records, ensuring the AI never "hallucinates" exchange rates.

Intelligent Autofill: A smart search system that allows users to pick years or specific trends for instant analysis.

Dynamic Financial Charting: Built-in time-series visualization to track Rupee volatility and depreciation trends.

Proactive Analyst Persona: The AI doesn't just answer; it suggests the next logical step in the economic investigation.

Fintech Dashboard UI: A Bloomberg-inspired dark mode interface featuring a live-style currency ticker and professional metrics.

🛠️ Technical Architecture
Large Language Model: Gemma 3 (via Ollama) for high-reasoning financial synthesis.

Vector Store: Vector-embedded historical ledger (money_exrate.txt) for high-precision retrieval.

Framework: LangChain for orchestrating the retrieval-to-generation pipeline.

Frontend: Streamlit with custom CSS injection for a professional trading-floor aesthetic.

📂 Project Structure
Bash

├── main.py              # Main Streamlit application and UI logic
├── vector.py            # Vector database & Retriever configuration
├── money_exrate.txt     # Raw historical FX data (2016-2026)
├── requirements.txt     # Project dependencies
└── README.md            # Project documentation
⚙️ Installation & Setup
Clone the Repository:

Bash

git clone https://github.com/YOUR_USERNAME/FX-WALL-E.git
cd FX-WALL-E
Install Dependencies:

Bash

pip install -r requirements.txt
Install & Run Ollama:
Ensure Ollama is installed and the model is pulled:

Bash

ollama pull gemma3
Launch the Application:

Bash

streamlit run main.py
📊 Sample Queries
Test the system's intelligence with these prompts:

"What was the exchange rate on January 1, 2026?"

"Compare the volatility of 2020 vs 2024."

"How much has the Rupee depreciated since 2016?"

"Find the date where the Rupee reached its weakest point in 2025."

🛡️ Economic Guardrails
Temperature Control: Set to 0.1 to ensure mathematical precision and factual consistency.

Groundedness: The system is instructed to state "Insufficient records" if data is missing, preventing false financial advice.

👨‍💻 Developed By
MOHAMED NAFSAR D
