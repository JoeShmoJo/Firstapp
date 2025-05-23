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
        json.dump(data, f, indent=2)

def filter_data(data, days):
    cutoff = datetime.now() - timedelta(days=days)
    return [entry for entry in data if datetime.fromisoformat(entry["timestamp"]) > cutoff]

def summarize(data):
    summary = {cat: 0 for cat in CATEGORIES}
    for entry in data:
        summary[entry["category"]] += entry["amount"]
    return summary

# Streamlit app
st.title("Spending Tracker")

# Session state to clear input after use
if "amount" not in st.session_state:
    st.session_state.amount = 0

# Input field: whole dollars only
amount = st.number_input("Enter amount ($)", min_value=0, step=1, value=st.session_state.amount)

# Buttons
data = load_data()
col1, col2, col3 = st.columns(3)

def log_expense(category):
    data.append({
        "amount": amount,
        "category": category,
        "timestamp": datetime.now().isoformat()
    })
    save_data(data)
    st.session_state.amount = 0  # Reset input

if col1.button("Booze"):
    log_expense("Booze")
if col2.button("Coffee"):
    log_expense("Coffee")
if col3.button("Food"):
    log_expense("Food")

# Summaries
data = load_data()
st.subheader("Today")
st.write(summarize(filter_data(data, 1)))

st.subheader("This Week")
st.write(summarize(filter_data(data, 7)))

st.subheader("This Month")
st.write(summarize(filter_data(data, 31)))

# Raw JSON Editor for all entries
st.subheader("Edit Expense Log")

raw_text = st.text_area("Logged Entries (JSON format)", value=json.dumps(data, indent=2), height=300)
if st.button("Save Changes"):
    try:
        new_data = json.loads(raw_text)
        save_data(new_data)
        st.success("Changes saved.")
    except Exception as e:
        st.error(f"Invalid JSON: {e}")