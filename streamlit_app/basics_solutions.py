import streamlit as st
import pandas as pd
import numpy as np

# Set the title of your Streamlit app
st.title("Streamlit Basics")

# Add some introductory text
st.write("Streamlit is a powerful tool for building data-powered web applications.")

# Displaying data with DataFrames
st.header("Dataframes and Tables")

# 1. Create and show a basic Pandas DataFrame
st.subheader("1. Simple Pandas DataFrame")
st.write("This is a simple dataframe with two columns.")
df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
})
st.dataframe(df)

# 2. Create and display a Numpy array
st.subheader("2. Numpy Array as DataFrame")
st.write("This is a numpy array with shape (10, 20).")
array_data = np.random.randn(10, 20)
st.dataframe(array_data)

# 3. Custom index and styled DataFrame
st.subheader("3. Highlighted Max in DataFrame")
styled_df = pd.DataFrame(
    np.random.randn(10, 20),
    columns=(f"col {i}" for i in range(20))
)
st.dataframe(styled_df.style.highlight_max(axis=0))

# Charts
st.header("Charts")

# 4. Line chart
st.subheader("4. Line Chart")
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c']
)
st.line_chart(chart_data)

# 5. Bar chart
st.subheader("5. Bar Chart")
bar_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=["a", "b", "c"]
)
st.bar_chart(bar_data)

# Widgets
st.header("Widgets")

# 6. Slider widget
st.subheader("6. Slider")
x = st.slider("Pick a number", 0, 100, 25)
st.write(x, "squared is", x * x)

# 7. Checkbox to show/hide data
st.subheader("7. Checkbox")
if st.checkbox("Show dataframe"):
    checkbox_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
    st.dataframe(checkbox_data)

# 8. Selectbox widget
st.subheader("8. Selectbox")
df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
})
option = st.selectbox("Which number do you like best?", df["first column"])
st.write("You selected:", option)

# 9. Text input
st.subheader("9. Text Input")
title = st.text_input("Movie title", "Life of Brian")
st.write("The current movie title is", title)