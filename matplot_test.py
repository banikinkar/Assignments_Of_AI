"""test how matplotlib works"""
import matplotlib.pyplot as plt

cities = ["Los Angeles", "San Francisco", "New York", "Houston", "Chicago"]
transactions = [120, 95, 150, 200, 180]

plt.bar(cities, transactions)
plt.title("Transactions per City")
plt.xticks(rotation=5)   # rotate labels diagonally
plt.show()