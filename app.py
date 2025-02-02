# pylint: disable=missing-module-docstring

import io

import duckdb
import pandas as pd
import streamlit as st

# dataframes & solution
CSV = """
beverage,price
orange juice,2.5
expresso,2
tea,3
"""
beverages = pd.read_csv(io.StringIO(CSV))

CSV2 = """
food_item,food_price
cookie,2.5
chocolatine,2
muffin,3
"""
food_items = pd.read_csv(io.StringIO(CSV2))

ANSWER_STR = """
SELECT * FROM beverages
CROSS JOIN food_items
"""
solution_df = duckdb.sql(ANSWER_STR).df()


# the title of the app
st.write(
    """
# SQL SRS
Spaced Repetition System SQL practice
"""
)
st.write("Let's study!")


# to select a topic to study
with st.sidebar:
    option = st.selectbox(
        "What would you like to study?",
        ("Joins", "GroupBy", "Window Functions"),
        index=None,
        placeholder="Select contact method...",
    )
    st.write("You selected:", option)


# ask the user to write an input
st.header("Enter your code:")
query = st.text_area(label="Votre code SQL ici", key="User_input")
if query:
    result = duckdb.sql(query).df()
    st.dataframe(result)

    # to manage the KeyError if we don't have the same columns as the ones from the solution
    try:
        result = result[solution_df.columns]
        st.dataframe(
            result.compare(solution_df)
        )  # Compare dataframes result & solution_df
    except KeyError as e:
        st.write("Some columns are missing")

    n_lines_difference = result.shape[0] - solution_df.shape[0]
    if n_lines_difference != 0:
        st.write(
            f"result has a {abs(n_lines_difference)} lines difference with the solution_df"
        )


# creation of tabs
tab2, tab3 = st.tabs(["Tables", "Solutions"])

with tab2:
    st.write("table: beverages")
    st.dataframe(beverages)
    st.write("table: food_items")
    st.dataframe(food_items)
    st.write("expected:")
    st.dataframe(solution_df)

with tab3:
    st.write(ANSWER_STR)
