# pylint: disable=missing-module-docstring

import duckdb
import streamlit as st

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

# ANSWER_STR = """
# SELECT * FROM beverages
# CROSS JOIN food_items
# """
# solution_df = duckdb.sql(ANSWER_STR).df()


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
    theme = st.selectbox(
        "What would you like to study?",
        ("cross_joins", "GroupBy", "Window Functions"),
        index=None,
        placeholder="Select contact method...",
    )
    st.write("You selected:", theme)

    exercise = con.execute(f"SELECT * FROM memory_state WHERE theme = '{theme}'").df()
    st.write(exercise)


# ask the user to write an input
st.header("Enter your code:")
query = st.text_area(label="Votre code SQL ici", key="User_input")
# if query:
#     result = duckdb.sql(query).df()
#     st.dataframe(result)
#
#     # to manage the KeyError if we don't have the same columns as the ones from the solution
#     try:
#         result = result[solution_df.columns]
#         st.dataframe(
#             result.compare(solution_df)
#         )  # Compare dataframes result & solution_df
#     except KeyError as e:
#         st.write("Some columns are missing")
#
#     n_lines_difference = result.shape[0] - solution_df.shape[0]
#     if n_lines_difference != 0:
#         st.write(
#             f"result has a {abs(n_lines_difference)} lines difference with the solution_df"
#         )
#
#
# # creation of tabs
# tab2, tab3 = st.tabs(["Tables", "Solutions"])
#
# with tab2:
#     st.write("table: beverages")
#     st.dataframe(beverages)
#     st.write("table: food_items")
#     st.dataframe(food_items)
#     st.write("expected:")
#     st.dataframe(solution_df)
#
# with tab3:
#     st.write(ANSWER_STR)
