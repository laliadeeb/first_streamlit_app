import streamlit

streamlit.title('My parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🍞Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinack & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑 HAvocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
#streamlit.dataframe(my_fruit_list)  -- first lesson
my_fruit_list = my_fruit_list.set_index('Fruit')

#Let's put a pick list here so they can pick the fruit they want to include
#streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))

# Let's put a pick list here so they can pick the fruit they want to include
#streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
# Let's put a pick list here so they can pick the fruit they want to include
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
  
#display the table on the page
#streamlit.dataframe(my_fruit_list)
streamlit.dataframe(fruits_to_show)


# New Section to display fruityvice API Response
streamlit.header('Fruityvice Fruit Advice!')
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')  #  added choice for 9.2
streamlit.write('The user entered ', fruit_choice)


# Basic data request display
import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)  #add choice for 9.2 removed watermelon
# streamlit.text(fruityvice_response.json())  #just write the data to the screen

# Better data request display:  take the json version of the response and normailize it - remove line #38 
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# Output it the screen as a table
streamlit.dataframe(fruityvice_normalized)

# Lesson 12 adding Snowflake connector using Pandas python
import snowflake.connector

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute("SELECT * from fruit_load_list")
my_data_row = my_cur.fetchone()
streamlit.text("The Fruit Load List Contains:")
streamlit.text(my_data_row)
