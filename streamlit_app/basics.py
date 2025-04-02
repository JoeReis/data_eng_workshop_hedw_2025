import streamlit as st
import pandas as pd
import numpy as np

# Set the title of your Streamlit app
st.title("___")  # TODO: Use st.title to set your app's title

# Add some introductory text
st.write("___")  # TODO: Use st.write to describe Streamlit

# Displaying data with DataFrames
st.header("Dataframes and Tables")

# 1. Create and show a basic Pandas DataFrame
st.subheader("1. Simple Pandas DataFrame")
st.write("This is a simple dataframe with two columns.")
df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
})
___  # TODO: Display the dataframe using st.write or st.dataframe

# 2. Create and display a Numpy array
st.subheader("2. Numpy Array as DataFrame")
st.write("This is a numpy array with shape (10, 20).")
array_data = ___  # TODO: Generate a 10x20 array of random numbers using np.random.randn
___  # TODO: Display the array using st.dataframe

# 3. Custom index and styled DataFrame
st.subheader("3. Highlighted Max in DataFrame")
styled_df = pd.DataFrame(
    np.random.randn(10, 20),
    columns=(f"col {i}" for i in range(20))
)
___  # TODO: Display the styled DataFrame using st.dataframe + highlight_max

# Charts
st.header("Charts")

# 4. Line chart
st.subheader("4. Line Chart")
chart_data = pd.DataFrame(
    ___,  # TODO: Generate 20x3 random data with np.random.randn
    columns=['a', 'b', 'c']
)
___  # TODO: Display the chart using st.line_chart

# 5. Bar chart
st.subheader("5. Bar Chart")
bar_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=["a", "b", "c"]
)
___  # TODO: Display the chart using st.bar_chart

# Widgets
st.header("Widgets")

# 6. Slider widget
st.subheader("6. Slider")
x = ___  # TODO: Use st.slider to create a slider for a number
st.write(x, "squared is", ___)  # TODO: Show x squared

# 7. Checkbox to show/hide data
st.subheader("7. Checkbox")
if ___:  # TODO: Create a checkbox labeled "Show dataframe"
    checkbox_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
    ___  # TODO: Display the dataframe if the checkbox is selected

# 8. Selectbox widget
st.subheader("8. Selectbox")
df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
})
option = ___  # TODO: Create a selectbox using st.selectbox with the first column of df
st.write("You selected:", ___)

# 9. Text input
st.subheader("9. Text Input")
title = ___  # TODO: Use st.text_input to enter a movie title
st.write("The current movie title is", title)