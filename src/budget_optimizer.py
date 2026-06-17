import pandas as pd

products = pd.read_csv("data/products.csv")

def recommend_by_budget(budget):
    results = products[products["Price"] <= budget]

    results = results.sort_values(
        by=["Rating", "Price"],
        ascending=[False, True]
    )

    return results.head(10)