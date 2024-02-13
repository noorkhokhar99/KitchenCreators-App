
import os
os.environ['VECTARA_API_KEY'] = 'zqt_UXrBcnI2UXINZkrv4g1tQPhzj02vfdtqYJIDiA'
os.environ['VECTARA_CORPUS_ID'] = '1'
os.environ['VECTARA_CUSTOMER_ID']='1366999410'

import os
import json
import requests
import streamlit as st

def vectara_query(query: str, config: dict) -> None:


    corpus_key = [
        {
            "customerId": config["customer_id"],
            "corpusId": config["corpus_id"],
            "lexicalInterpolationConfig": {"lambda": config["lambda_val"]},
        }
    ]
    data = {
        "query": [
            {
                "query": query,
                "start": 0,
                "numResults": config["top_k"],
                "contextConfig": {
                    "sentencesBefore": 2,
                    "sentencesAfter": 2,
                },
                "corpusKey": corpus_key,
                "summary": [
                    {
                        "responseLang": "eng",
                        "maxSummarizedResults": 5,
                    }
                ]
            }
        ]
    }

    headers = {
        "x-api-key": config["api_key"],
        "customer-id": config["customer_id"],
        "Content-Type": "application/json",
    }
    response = requests.post(
        headers=headers,
        url="https://api.vectara.io/v1/query",
        data=json.dumps(data),
    )
    if response.status_code != 200:
        print(
            "Query failed %s",
            f"(code {response.status_code}, reason {response.reason}, details "
            f"{response.text})",
        )
        return []

    result = response.json()
    responses = result["responseSet"][0]["response"]
    documents = result["responseSet"][0]["document"]
    summary = result["responseSet"][0]["summary"][0]["text"]

    res = [[r['text'], r['score']] for r in responses]
    return res, summary 




# Set the environment variables
os.environ['VECTARA_API_KEY'] = 'zqt_UXrBcnI2UXINZkrv4g1tQPhzj02vfdtqYJIDiA'
os.environ['VECTARA_CORPUS_ID'] = '1'
os.environ['VECTARA_CUSTOMER_ID'] = '1366999410'

# Load config from environment variables
api_key = os.environ.get("VECTARA_API_KEY", "")
customer_id = os.environ.get("VECTARA_CUSTOMER_ID", "")
corpus_id = os.environ.get("VECTARA_CORPUS_ID", "")

config = {
    "api_key": str(api_key),
    "customer_id": str(customer_id),
    "corpus_id": str(corpus_id),
    "lambda_val": 0.025,
    "top_k": 10,
}

# Streamlit app
st.title("KitchenCreators App")

# Input for the query
query = st.text_input("Enter your query:", "What does Kitchen Creators do?")

# Button to trigger the query
if st.button("Run Query"):
    results, summary = vectara_query(query, config)

    # Display results
    st.header("Results")
    st.write(results)

    # Display summary
    st.header("Summary")
    st.write(summary)