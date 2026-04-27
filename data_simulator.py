"""
Data Simulator — SmartQuery AI
Author: Abhay Sharma | github.com/KAZURIKAFU
Simulates realistic public datasets for offline BigQuery-style analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

# ── Dataset 1: World Air Quality ─────────────────────────────────────────────
def get_air_quality_data() -> pd.DataFrame:
    countries = ["India","China","USA","Germany","Brazil","Australia","Japan",
                 "UK","France","Canada","Russia","South Africa","Mexico","Italy",
                 "Spain","Pakistan","Bangladesh","Indonesia","Nigeria","Egypt",
                 "UAE","Singapore","Sweden","Norway","Denmark"]
    city_map = {
        "India":["Delhi","Mumbai","Kolkata","Chennai","Bangalore","Hyderabad"],
        "China":["Beijing","Shanghai","Guangzhou","Shenzhen","Chengdu"],
        "USA":["New York","Los Angeles","Chicago","Houston","Phoenix"],
        "Germany":["Berlin","Munich","Hamburg","Frankfurt","Cologne"],
        "Brazil":["São Paulo","Rio de Janeiro","Brasília","Salvador"],
        "Australia":["Sydney","Melbourne","Brisbane","Perth"],
        "Japan":["Tokyo","Osaka","Kyoto","Nagoya","Sapporo"],
        "UK":["London","Manchester","Birmingham","Leeds"],
        "France":["Paris","Lyon","Marseille","Toulouse"],
        "Canada":["Toronto","Vancouver","Montreal","Calgary"],
        "Russia":["Moscow","Saint Petersburg","Novosibirsk"],
        "South Africa":["Johannesburg","Cape Town","Durban"],
        "Mexico":["Mexico City","Guadalajara","Monterrey"],
        "Italy":["Rome","Milan","Naples","Turin"],
        "Spain":["Madrid","Barcelona","Valencia","Seville"],
        "Pakistan":["Karachi","Lahore","Islamabad"],
        "Bangladesh":["Dhaka","Chittagong","Rajshahi"],
        "Indonesia":["Jakarta","Surabaya","Bandung"],
        "Nigeria":["Lagos","Abuja","Kano"],
        "Egypt":["Cairo","Alexandria","Giza"],
        "UAE":["Dubai","Abu Dhabi","Sharjah"],
        "Singapore":["Singapore City"],
        "Sweden":["Stockholm","Gothenburg"],
        "Norway":["Oslo","Bergen"],
        "Denmark":["Copenhagen","Aarhus"],
    }
    base_aqi = {"India":160,"China":145,"Pakistan":155,"Bangladesh":150,
                "Nigeria":120,"Egypt":115,"Indonesia":110,"Mexico":100,
                "USA":55,"Germany":30,"Sweden":18,"Norway":16,
                "Denmark":20,"Singapore":35,"Australia":28}
    rows = []
    for country in countries:
        for city in city_map.get(country, [country+" City"]):
            b = base_aqi.get(country, 60)
            for month in range(1, 13):
                aqi = max(5, b + 20*np.sin(np.pi*month/6) + np.random.normal(0,15))
                rows.append({"country":country,"city":city,"month":month,"year":2024,
                             "aqi":round(aqi,1),"pm25":round(aqi*0.6+np.random.normal(0,5),1),
                             "pm10":round(aqi*0.9+np.random.normal(0,8),1),
                             "co2_emissions":round(np.random.uniform(2,15),2),
                             "population_millions":round(np.random.uniform(0.5,30),1)})
    return pd.DataFrame(rows)


# ── Dataset 2: Global COVID Statistics ───────────────────────────────────────
def get_covid_data() -> pd.DataFrame:
    countries = ["USA","India","Brazil","France","Germany","UK","Russia",
                 "South Korea","Italy","Japan","Australia","Canada","Spain",
                 "Argentina","Mexico","Turkey","Indonesia","Netherlands","Poland","Ukraine"]
    rows = []
    start = datetime(2020, 3, 1)
    for country in countries:
        base = np.random.randint(500000, 50000000)
        cumulative = 0
        for week in range(200):
            date = start + timedelta(weeks=week)
            wave = 1 + 2*abs(np.sin(np.pi*week/26))
            new_cases = max(0, int(base*0.002*wave*np.random.uniform(0.5,1.5)))
            cumulative += new_cases
            rows.append({"country":country,"date":date.strftime("%Y-%m-%d"),
                         "week":week+1,"new_cases":new_cases,"total_cases":cumulative,
                         "deaths":int(new_cases*np.random.uniform(0.005,0.025)),
                         "recovered":int(new_cases*np.random.uniform(0.85,0.95)),
                         "vaccinated_pct":min(95,round(week*0.45+np.random.uniform(0,5),1))})
    return pd.DataFrame(rows)


# ── Dataset 3: Indian Census & Demographics ───────────────────────────────────
def get_india_census_data() -> pd.DataFrame:
    states = ["Uttar Pradesh","Maharashtra","Bihar","West Bengal","Rajasthan",
              "Madhya Pradesh","Tamil Nadu","Karnataka","Gujarat","Andhra Pradesh",
              "Odisha","Telangana","Kerala","Jharkhand","Assam",
              "Punjab","Chhattisgarh","Haryana","Delhi","Himachal Pradesh"]
    rows = []
    for state in states:
        pop = np.random.randint(5000000, 240000000)
        rows.append({"state":state,"population":pop,
                     "population_millions":round(pop/1e6,2),
                     "area_sq_km":np.random.randint(10000,340000),
                     "literacy_rate":round(np.random.uniform(55,96),1),
                     "sex_ratio":np.random.randint(850,1050),
                     "gdp_billion_usd":round(np.random.uniform(20,400),1),
                     "per_capita_income_usd":round(np.random.uniform(800,4500),0),
                     "urban_population_pct":round(np.random.uniform(18,98),1),
                     "internet_penetration_pct":round(np.random.uniform(25,85),1),
                     "hospitals_per_lakh":round(np.random.uniform(0.5,4.5),2),
                     "schools_per_lakh":round(np.random.uniform(15,65),1)})
    return pd.DataFrame(rows)


# ── Dataset 4: Stock Market Data ─────────────────────────────────────────────
def get_stock_data() -> pd.DataFrame:
    stocks = {"AAPL":("Apple Inc.","Technology",150),
              "GOOGL":("Alphabet Inc.","Technology",130),
              "MSFT":("Microsoft Corp.","Technology",380),
              "AMZN":("Amazon.com Inc.","E-Commerce",180),
              "TSLA":("Tesla Inc.","Automotive",200),
              "META":("Meta Platforms","Social Media",500),
              "NVDA":("NVIDIA Corp.","Semiconductors",800),
              "RELIANCE":("Reliance Industries","Conglomerate",2800),
              "TCS":("Tata Consultancy","IT Services",3900),
              "INFY":("Infosys Ltd.","IT Services",1600),
              "WIPRO":("Wipro Ltd.","IT Services",550),
              "HDFC":("HDFC Bank","Banking",1700)}
    rows = []
    start = datetime(2024, 1, 1)
    for ticker,(name,sector,base_price) in stocks.items():
        price = base_price
        for day in range(365):
            date = start + timedelta(days=day)
            if date.weekday() >= 5: continue
            price = max(10, price*(1+np.random.normal(0.0003,0.015)))
            rows.append({"ticker":ticker,"company":name,"sector":sector,
                         "date":date.strftime("%Y-%m-%d"),
                         "open":round(price*np.random.uniform(0.995,1.005),2),
                         "close":round(price,2),
                         "high":round(price*np.random.uniform(1.005,1.025),2),
                         "low":round(price*np.random.uniform(0.975,0.995),2),
                         "volume":np.random.randint(1000000,50000000),
                         "market_cap_billion":round(price*np.random.uniform(5,30),1)})
    return pd.DataFrame(rows)


# ── Dataset 5: E-Commerce Sales ───────────────────────────────────────────────
def get_ecommerce_data() -> pd.DataFrame:
    categories = ["Electronics","Fashion","Home & Garden","Books","Sports",
                  "Beauty","Toys","Automotive","Food","Healthcare"]
    regions = ["North India","South India","East India","West India","Central India","North East India"]
    base_sales = {"Electronics":50000,"Fashion":35000,"Home & Garden":25000,
                  "Books":8000,"Sports":18000,"Beauty":22000,"Toys":15000,
                  "Automotive":30000,"Food":45000,"Healthcare":20000}
    rows = []
    start = datetime(2024, 1, 1)
    for day in range(365):
        date = start + timedelta(days=day)
        for category in categories:
            for region in regions:
                b = base_sales.get(category, 20000)
                seasonal = 1 + 0.3*np.sin(np.pi*day/182)
                weekend = 1.3 if date.weekday() >= 5 else 1.0
                sales = b * seasonal * weekend * np.random.uniform(0.7,1.3)
                rows.append({"date":date.strftime("%Y-%m-%d"),"month":date.month,
                             "quarter":(date.month-1)//3+1,"category":category,
                             "region":region,"revenue":round(sales,2),
                             "orders":int(sales/np.random.uniform(300,800)),
                             "avg_order_value":round(np.random.uniform(250,2500),2),
                             "returns_pct":round(np.random.uniform(2,15),1),
                             "customer_rating":round(np.random.uniform(3.2,4.9),1)})
    return pd.DataFrame(rows)


# ── Dataset Registry ─────────────────────────────────────────────────────────
DATASETS = {
    "air_quality":   {"loader":get_air_quality_data,  "icon":"🌍",
                      "description":"World Air Quality & CO2 Emissions (2024)"},
    "covid":         {"loader":get_covid_data,         "icon":"🦠",
                      "description":"Global COVID-19 Statistics (2020–2024)"},
    "india_census":  {"loader":get_india_census_data,  "icon":"🇮🇳",
                      "description":"Indian State Demographics & Census"},
    "stocks":        {"loader":get_stock_data,         "icon":"📈",
                      "description":"Global Stock Market Data (2024)"},
    "ecommerce":     {"loader":get_ecommerce_data,     "icon":"🛒",
                      "description":"India E-Commerce Sales Analytics (2024)"},
}

_cache = {}

def get_dataset(name: str) -> pd.DataFrame:
    if name not in _cache:
        _cache[name] = DATASETS[name]["loader"]()
    return _cache[name]
