import streamlit as st
import pandas as pd
import duckdb
import io


# dataframes & solution
csv = '''
beverage,price
orange juice,2.5
expresso,2
tea,3
'''
beverages = pd.read_csv(io.StringIO(csv))

csv2 = '''
food_item,food_price
cookie,2.5
chocolatine,2
muffin,3
'''
food_items = pd.read_csv(io.StringIO(csv2))

answer = """
SELECT * FROM beverages
CROSS JOIN food_items
"""
solution = duckdb.sql(answer).df()


# the title of the app
st.write("""
# SQL SRS
Spaced Repetition System SQL practice
""")
st.write("Let's study!")


# to select a topic to study
with st.sidebar:
    option = st.selectbox(
        "What would you like to study?",
        ("Joins", "GroupBy", "Window Functions"),
        index = None,
        placeholder="Select contact method..."
    )
    st.write('You selected:', option)


# ask the user to write an input
st.header("Enter your code:")
query = st.text_area(label="Votre code SQL ici", key="User_input")
if query:
    result = duckdb.sql(query).df()
    st.dataframe(result)


# creation of tabs
tab2, tab3 = st.tabs(["Tables", "Solutions"])

with tab2:
    st.write("table: beverages")
    st.dataframe(beverages)
    st.write("table: food_items")
    st.dataframe(food_items)
    st.write("expected:")
    st.dataframe(solution)

with tab3:
    st.write(answer)
