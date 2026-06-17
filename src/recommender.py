import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

products = pd.read_csv("data/products.csv")

products["Features"] = (
    products["Category"].fillna("") + " " +
    products["Brand"].fillna("") + " " +
    products["Description"].fillna("")
)

vectorizer = TfidfVectorizer(stop_words="english")

feature_matrix = vectorizer.fit_transform(products["Features"])

similarity_matrix = cosine_similarity(feature_matrix)


def recommend(product_name, top_n=5):

    if product_name not in products["ProductName"].values:
        return []

    idx = products[
        products["ProductName"] == product_name
    ].index[0]

    scores = list(enumerate(similarity_matrix[idx]))

    scores = sorted(
        scores,
        key=lambda x: x[1],
        reverse=True
    )

    recommendations = []

    for score in scores[1:top_n+1]:
        recommendations.append(
            products.iloc[score[0]]["ProductName"]
        )

    return recommendations


if __name__ == "__main__":
    print(recommend("Wireless Mouse"))