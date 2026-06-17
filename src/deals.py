import pandas as pd

products = pd.read_csv("data/products.csv")

products["Savings"] = (
    products["OriginalPrice"] -
    products["Price"]
)

def get_best_deals():
    return products.sort_values(
        by="Savings",
        ascending=False
    ).head(10)