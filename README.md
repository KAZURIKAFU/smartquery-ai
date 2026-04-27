# 🤖 SmartQuery AI — Natural Language Data Analysis Dashboard

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Dash](https://img.shields.io/badge/Dash-Plotly-orange?style=for-the-badge&logo=plotly)
![Google Cloud](https://img.shields.io/badge/Google_Cloud-BigQuery-4285F4?style=for-the-badge&logo=googlecloud)
![Gemini AI](https://img.shields.io/badge/Gemini-AI-green?style=for-the-badge&logo=google)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**Ask questions in plain English. Get instant data insights.**  
*Powered by Google BigQuery + Gemini AI*

> 🎓 Built by **Abhay Sharma** | Manipal University Jaipur  
> ☁️ Showcases 10 Google Cloud Certifications in action

</div>

---

## 🚀 What is SmartQuery AI?

SmartQuery AI is a **natural language data analytics dashboard** that lets anyone — regardless of SQL knowledge — query and visualize large datasets simply by typing questions in plain English.

```
User types:  "Show me top 10 most polluted cities in the world"
                            ↓
           Gemini AI converts to SQL/Pandas query
                            ↓
           BigQuery / Simulator executes query
                            ↓
           Auto chart builder picks best visualization
                            ↓
           Dashboard renders interactive chart + stats
```

---

## ✨ Features

| Feature | Description |
|---|---|
| 💬 Natural Language Query | Ask questions in plain English |
| 🤖 Gemini AI Engine | Intelligent query parsing & SQL generation |
| ☁️ BigQuery Integration | Google Cloud public dataset support |
| 📊 Auto Visualization | Automatically picks Bar, Line, Pie charts |
| 📁 5 Real Datasets | Air Quality, COVID, India Census, Stocks, E-Commerce |
| 📋 Data Preview Table | View first rows of query results |
| 📈 Summary Statistics | Auto count, mean, max, min, total |
| 🕓 Query History | Tracks your last 10 queries |
| 💡 Example Queries | 15+ pre-built example queries |
| 🎨 Dark Theme UI | Professional dark dashboard |
| ⚡ Offline Mode | Works without GCP account using simulated data |

---

## 📁 Project Structure

```
smartquery-ai/
│
├── app.py                     # Main Dash application & UI
├── gemini_engine.py           # NLP query parser & Gemini AI engine
├── data_simulator.py          # 5 realistic dataset simulators
├── chart_builder.py           # Auto chart generation engine
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── LICENSE.txt                # MIT License
│
└── assets/
    └── sample_queries.json    # 21 pre-built example queries
```

---

## 📊 Datasets Available

| Dataset | Rows | Columns | Description |
|---|---|---|---|
| 🌍 Air Quality | 1,056 | 9 | World AQI, PM2.5, PM10, CO2 (2024) |
| 🦠 COVID-19 | 4,000 | 8 | Global cases, deaths, vaccination (2020–2024) |
| 🇮🇳 India Census | 20 | 12 | State demographics, GDP, literacy |
| 📈 Stocks | 3,132 | 10 | Global & Indian stock prices (2024) |
| 🛒 E-Commerce | 21,900 | 10 | India sales analytics by category & region |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Dash by Plotly, Plotly.js |
| AI Engine | Google Gemini AI (NLP Query Parser) |
| Cloud Database | Google BigQuery (simulated offline) |
| Data Processing | Python, Pandas, NumPy |
| Visualization | Plotly Express, Plotly Graph Objects |
| Deployment | Local / Google Cloud Run |

---

## ⚙️ Installation & Setup

```bash
# 1. Clone the repository
git clone https://github.com/KAZURIKAFU/smartquery-ai.git
cd smartquery-ai

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python app.py

# 4. Open in browser
# Navigate to: http://localhost:8051
```

---

## 💬 Example Queries You Can Ask

**🌍 Air Quality**
- *"Show top 10 most polluted cities"*
- *"CO2 emissions by country"*
- *"Cleanest cities in the world"*

**🦠 COVID-19**
- *"COVID total cases by country"*
- *"Vaccination progress over time"*

**🇮🇳 India Census**
- *"Most populated Indian states"*
- *"Literacy rate by state"*
- *"GDP by Indian state"*

**📈 Stocks**
- *"Stock price trend NVDA MSFT AAPL"*
- *"Indian IT stocks TCS Infosys Wipro"*

**🛒 E-Commerce**
- *"Revenue by product category"*
- *"Monthly sales trend"*
- *"Quarterly revenue comparison"*

---

## ☁️ Google Cloud Skills Demonstrated

This project directly showcases the following Google Cloud certifications:

![GCP](https://img.shields.io/badge/BigQuery_ML_for_Inference-4285F4?style=flat-square&logo=googlecloud&logoColor=white)
![GCP](https://img.shields.io/badge/Work_with_Gemini_in_BigQuery-4285F4?style=flat-square&logo=googlecloud&logoColor=white)
![GCP](https://img.shields.io/badge/Gemini_for_Data_Scientists-4285F4?style=flat-square&logo=googlecloud&logoColor=white)
![GCP](https://img.shields.io/badge/Introduction_to_Generative_AI-4285F4?style=flat-square&logo=googlecloud&logoColor=white)
![GCP](https://img.shields.io/badge/Boost_Productivity_with_Gemini-4285F4?style=flat-square&logo=googlecloud&logoColor=white)

---

## 👤 Author

**Abhay Sharma**
🎓 B.Tech Data Science & Engineering — Manipal University Jaipur
🔗 [LinkedIn](https://linkedin.com/in/abhay-sharma-426702208) | [GitHub](https://github.com/KAZURIKAFU)
📧 abby.official2412@gmail.com

---

## 📄 License

MIT License — see [LICENSE.txt](LICENSE.txt) for details.

---

<div align="center">
⭐ Star this repo if you found it useful!
Built with ❤️ by Abhay Sharma | Manipal University Jaipur
</div>
