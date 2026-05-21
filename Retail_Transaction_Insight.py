"""
Retail Transactions Analysis Project
------------------------------------

This program analyzes a nationwide retail chain's transaction dataset
to uncover customer behaviour, promotional impact, and seasonal trends.

Why this program is written:
- To perform data preparation and cleaning on the provided CSV file.
- To explore basic statistics such as total transactions, unique customers,
  top products, and city-level activity.
- To analyze customer behaviour (spending patterns, payment preferences,
  store-type trends).
- To evaluate the impact of discounts and promotions on sales.
- To identify seasonality trends in revenue and product demand.
- To generate visualizations (bar charts, pie charts, line charts) that
  summarize insights for business decision-making.

The program uses only simple Python libraries:
- `csv` for reading structured transaction data safely.
- `datetime` for parsing and extracting date-related features.
- `collections` for counting and grouping.
- `matplotlib` for clear, lightweight visualizations.

Deliverables:
- Clean, commented Python code
- Outputs of calculations and visualizations
- A summary of key insights for leadership

This ensures the analysis is reproducible, easy to understand,
and avoids heavy dependencies, making it suitable for graded assignments.

Version:1.0 Author:Bani Assignment:Week4_Graded

"""

import csv
from datetime import datetime
from collections import Counter, defaultdict
import matplotlib.pyplot as plt

# ---------- Task 1: Data Preparation ----------
def load_and_prepare_data(filename):
    data = []
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Parse date
            date_obj = datetime.strptime(row['Date'], "%Y-%m-%d %H:%M:%S")
            row['Date_obj'] = date_obj
            row['Year'] = date_obj.year
            row['Month'] = date_obj.month
            row['DayOfWeek'] = date_obj.strftime("%A")
            # Convert numeric fields
            row['Total_Items'] = int(row['Total_Items'])
            row['Total_Cost'] = float(row['Total_Cost'])
            data.append(row)
    return data

# ---------- Task 2: Basic Exploration ----------
def basic_exploration(data):
    total_transactions = len(data)
    unique_customers = len(set(d['Customer_Name'] for d in data))
    product_counter = Counter()
    city_counter = Counter()

    for d in data:
        # Products are stored like "['Milk','Bread']" → clean them
        products = d['Product'].strip("[]").replace("'", "").split(",")
        product_counter.update([p.strip() for p in products])
        city_counter[d['City']] += 1

    print("Total Transactions:", total_transactions)
    print("Unique Customers:", unique_customers)
    print("Top 5 Products:", product_counter.most_common(5))
    print("Cities with most transactions:", city_counter.most_common(5))

# ---------- Task 3: Customer Behaviour ----------
def customer_behaviour(data):
    spend_by_category = defaultdict(list)
    payment_by_category = defaultdict(Counter)
    items_by_store = defaultdict(list)

    for d in data:
        spend_by_category[d['Customer_Category']].append(d['Total_Cost'])
        payment_by_category[d['Customer_Category']][d['Payment_Method']] += 1
        items_by_store[d['Store_Type']].append(d['Total_Items'])

    for cat, spends in spend_by_category.items():
        print(f"{cat} avg spend: {sum(spends)/len(spends):.2f}")

    for cat, methods in payment_by_category.items():
        print(f"{cat} prefers: {methods.most_common(1)}")

    for store, items in items_by_store.items():
        print(f"{store} avg items: {sum(items)/len(items):.2f}")

# ---------- Task 4: Promotion & Discount ----------
def promotion_discount(data):
    discount_spend = [d['Total_Cost'] for d in data if d['Discount_Applied'].upper() == "TRUE"]
    no_discount_spend = [d['Total_Cost'] for d in data if d['Discount_Applied'].upper() == "FALSE"]

    print("Avg spend with discount:", sum(discount_spend)/len(discount_spend))
    print("Avg spend without discount:", sum(no_discount_spend)/len(no_discount_spend))

    promo_items = defaultdict(list)
    promo_cost = defaultdict(list)
    for d in data:
        promo_items[d['Promotion']].append(d['Total_Items'])
        promo_cost[d['Promotion']].append(d['Total_Cost'])

    for promo, items in promo_items.items():
        print(f"{promo} avg items: {sum(items)/len(items):.2f}")
    for promo, costs in promo_cost.items():
        print(f"{promo} avg cost: {sum(costs)/len(costs):.2f}")

# ---------- Task 5: Seasonality ----------
def seasonality(data):
    revenue_by_season = defaultdict(float)
    for d in data:
        revenue_by_season[d['Season']] += d['Total_Cost']

    print("Revenue by season:", revenue_by_season)
    # Plot
    plt.bar(revenue_by_season.keys(), revenue_by_season.values())
    plt.title("Average Spending per Season")
    plt.show()

# ---------- Task 6: Visualisation Dashboard ----------
def dashboard(data):
    # Transactions per city
    city_counter = Counter(d['City'] for d in data)
    plt.bar(city_counter.keys(), city_counter.values())
    plt.title("Transactions per City")
    plt.xticks(rotation=45)
    plt.show()

    # Payment methods pie chart
    payment_counter = Counter(d['Payment_Method'] for d in data)
    plt.pie(payment_counter.values(), labels=payment_counter.keys(), autopct='%1.1f%%')
    plt.title("Payment Method Distribution")
    plt.show()

    # Monthly revenue line chart
    monthly_revenue = defaultdict(float)
    for d in data:
        key = (d['Year'], d['Month'])
        monthly_revenue[key] += d['Total_Cost']
    sorted_keys = sorted(monthly_revenue.keys())
    values = [monthly_revenue[k] for k in sorted_keys]
    labels = [f"{y}-{m}" for y, m in sorted_keys]
    plt.plot(labels, values, marker='o')
    plt.xticks(rotation=90)
    plt.title("Monthly Revenue Trends")
    plt.show()

# ---------- Main ----------
if __name__ == "__main__":
    data = load_and_prepare_data("Retail_Transactions_Dataset.csv")
    basic_exploration(data)
    customer_behaviour(data)
    promotion_discount(data)
    seasonality(data)
    dashboard(data)
