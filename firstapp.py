import streamlit as st
from datetime import datetime, timedelta
import json
import os

DATA_FILE = "spending_data.json"
CATEGORIES = ["Booze", "Coffee", "Food"]

# Load/save functions
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

# App title
st.title("Spending Tracker")

# Text input for dollars (whole numbers)
if "amount_input" not in st.session_state:
    st.session_state.amount_input = ""

amount = st.text_input("Enter amount ($ whole dollars)", value=st.session_state.amount_input, key="amount_box")

# Function to log entry and clear input
def log_expense(category):
    try:
        amount_value = int(st.session_state.amount_box)
        data = load_data()
        data.append({
            "amount": amount_value,
            "category": category,
            "timestamp": datetime.now().isoformat()
        })
        save_data(data)
        st.session_state.amount_box = ""  # Clear input box
    except ValueError:
        st.error("Please enter a valid whole dollar amount.")

# Buttons
col1, col2, col3 = st.columns(3)
if col1.button("Booze"):
    log_expense("Booze")
if col2.button("Coffee"):
    log_expense("Coffee")
if col3.button("Food"):
    log_expense("Food")

# Reload and show summaries
data = load_data()

st.subheader("Today")
st.write(summarize(filter_data(data, 1)))

st.subheader("This Week")
st.write(summarize(filter_data(data, 7)))

st.subheader("This Month")
st.write(summarize(filter_data(data, 31)))

# Editable JSON log
st.subheader("Edit Logged Expenses")
log_text = st.text_area("Log (JSON format)", value=json.dumps(data, indent=2), height=300)

if st.button("Save Changes"):
    try:
        new_data = json.loads(log_text)
        save_data(new_data)
        st.success("Changes saved.")
    except Exception as e:
        st.error(f"Error: Invalid JSON\n{e}")