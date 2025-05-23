import streamlit as st
from datetime import datetime, timedelta
import json
import os

DATA_FILE = "spending_data.json"
CATEGORIES = ["Booze", "Coffee", "Food"]

# Load/save data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# Filter by time
def filter_data(data, days):
    cutoff = datetime.now() - timedelta(days=days)
    return [entry for entry in data if datetime.fromisoformat(entry["timestamp"]) > cutoff]

# Summarize by category
def summarize(data):
    summary = {cat: 0.0 for cat in CATEGORIES}
    for entry in data:
        summary[entry["category"]] += entry["amount"]
    return summary

# UI
st.title("Spending Tracker")

amount = st.number_input("Enter amount", min_value=0.0, step=0.01)

col1, col2, col3 = st.columns(3)
if col1.button("Booze"):
    entry = {"amount": amount, "category": "Booze", "timestamp": datetime.now().isoformat()}
    data = load_data()
    data.append(entry)
    save_data(data)
if col2.button("Coffee"):
    entry = {"amount": amount, "category": "Coffee", "timestamp": datetime.now().isoformat()}
    data = load_data()
    data.append(entry)
    save_data(data)
if col3.button("Food"):
    entry = {"amount": amount, "category": "Food", "timestamp": datetime.now().isoformat()}
    data = load_data()
    data.append(entry)
    save_data(data)

# Show summaries
data = load_data()
st.subheader("Today")
st.write(summarize(filter_data(data, 1)))

st.subheader("This Week")
st.write(summarize(filter_data(data, 7)))

st.subheader("This Month")
st.write(summarize(filter_data(data, 31)))