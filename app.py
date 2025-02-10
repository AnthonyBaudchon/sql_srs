# pylint: disable=missing-module-docstring

import os
import logging
import duckdb
import streamlit as st
from datetime import date, timedelta


if "data" not in os.listdir():
    print("creating folder data")
    logging.error(os.listdir())
    logging.error("creating folder data")
    os.mkdir("data")

if "exercises_sql_tables.duckdb" not in os.listdir("data"):
    exec(open("init_db.py").read())  # pylint: disable=maybe-no-member
    # subprocess.run(["python", "init_db.py"])

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)


def check_users_solution(user_query: str) -> None:
    """
    Checks that user SQL query is correct by:
    1 : checking the columns
    2 : checking the values
    :param user_query: a string containing the query inserted by the user
    """
    result = con.execute(user_query).df()
    st.dataframe(result)
    # to manage the KeyError if we don't have the same columns as the ones from the solution
    try:
        result = result[solution_df.columns]
        st.dataframe(result.compare(solution_df))  # Compare dataframes result & solution_df
        if result.compare(solution_df).shape == (0,0):
            st.write("Correct !")
            st.balloons()
    except KeyError as e:
        st.write("Some columns are missing")
    # to compare the number of rows
    n_lines_difference = result.shape[0] - solution_df.shape[0]
    if n_lines_difference != 0:
        st.write(
            f"result has a {abs(n_lines_difference)} lines difference with the solution_df"
        )


# the title of the app
st.write(
    """
# SQL SRS
Spaced Repetition System SQL practice
"""
)
st.write("Let's study!")


# to make the user select a topic to study
with st.sidebar:
    available_themes_df = con.execute("SELECT DISTINCT theme FROM memory_state").df()
    theme = st.selectbox(
        "What would you like to study?",
        available_themes_df["theme"].unique(),
        index=None,
        placeholder="Select a topic...",
    )
    # if/else to manage the ValueError when no theme is selected
    if theme:
        st.write(f"You selected {theme}")
        select_exercise_query = f"SELECT * FROM memory_state WHERE theme = '{theme}'"
    else:
        select_exercise_query = f"SELECT * FROM memory_state"
    # then connect to the specific table in the database
    exercise = (
        con.execute(select_exercise_query)
        .df()
        .sort_values("last_reviewed")
        .reset_index(drop=True)
    )
    st.write(exercise)

    exercise_name = exercise.loc[0, "exercise_name"]
    with open(f"answers/{exercise_name}.sql", "r") as f:
        answer = f.read()
    # then we open the solution of the exercise from 'answers' files for using it later
    solution_df = con.execute(answer).df()


# ask the user to write an input & show the output
st.header("Enter your code:")
query = st.text_area(label="Votre code SQL ici", key="User_input")

if query:
    check_users_solution(query)

# creation of buttons for selecting when to re-do the exercise
for n_days in [2,7,21]:
    if st.button(f"revoir dans {n_days} jours"):
        next_review = date.today() + timedelta(days=n_days)
        con.execute(f"UPDATE memory_state SET last_reviewed = '{next_review}' WHERE exercise_name = '{exercise_name}'")
        st.rerun()

if st.button('Reset'):
    con.execute(f"UPDATE memory_state SET last_reviewed = '1970-01-01'")
    st.rerun()


# creation of tabs
tab2, tab3 = st.tabs(["Tables", "Solutions"])

with tab2:
    exercise_tables = exercise.loc[0, "tables"]
    for table in exercise_tables:
        st.write(f"table: {table}")
        df_table = con.execute(f"SELECT * FROM {table}").df()
        st.dataframe(df_table)

with tab3:
    st.text(answer)
