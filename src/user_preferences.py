import pandas as pd

products = pd.read_csv("data/products.csv")

def recommend_by_category(category):

    results = products[
        products["Category"] == category
    ]

    return results.sort_values(
        by="Rating",
        ascending=False
    ).head(10)