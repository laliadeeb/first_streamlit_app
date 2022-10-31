import streamlit
# Lession 12 adds
import pandas                     
import requests
import snowflake.connector
# new library for error handling
from urllib.error import URLError 

streamlit.title('My parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🍞Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinack & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑 HAvocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#import pandas
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

# Lesson 12 to convert the ELSE stmts to function
# Create the repeatable code block (called a function)
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
  
# New Section to display fruityvice API Response
streamlit.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    #fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    #fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    # Use function instead
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
    
except URLError as e:
  streamlit.error()

# BEGIN L12 error handling and Loop
#fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')  #  added choice for 9.2
#streamlit.write('The user entered ', fruit_choice)

# Basic data request display
#import requests
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)  #add choice for 9.2 removed watermelon
# streamlit.text(fruityvice_response.json())  #just write the data to the screen

# Better data request display:  take the json version of the response and normailize it - remove line #38 
#fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# Output it the screen as a table
#streamlit.dataframe(fruityvice_normalized)
# END L12 error handling and Loop

# Lession 12 add for DEBUGGING - Don't run anything past here while we troubleshoot
#streamlit.stop()

# Lesson 12 adding Snowflake connector using Pandas python
#import snowflake.connector

# L12 OLD Code 
##my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
##my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
##my_cur.execute("SELECT * from fruit_load_list")
#my_data_row = my_cur.fetchone()                  -- for one row only - line 56: get all row in list table
##my_data_rows = my_cur.fetchall() 
#streamlit.text("The Fruit Load List Contains:")  -- make it look nicer
#streamlit.text(my_data_row)                      -- with frame for all ROWS
##streamlit.header("The Fruit Load List Contains:")  
##streamlit.dataframe(my_data_rows)
# L12 OLD Code

streamlit.header("The Fruit Load List Contains:") 
# Snowflake-related functions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * from fruit_load_list")
        return my_cur.fetchall() 
      
# Add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)


# Ask user what fruit to add 
fruit_choice = streamlit.text_input('What fruit would you like to add?')

#my_cnx2 = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#my_cur2 = my_cnx2.cursor()
#my_cur2.execute("INSERT INTO pc_rivery_db.public.fruit_load_list values('Jackfruit')" )

streamlit.write('Thanks you for adding:  ' , fruit_choice)

# This will not work correctly, but just go with it for now
my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('from streamlit')")

