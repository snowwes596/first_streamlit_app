import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣    Omerga 3 & Blueberry Oatmeal')
streamlit.text('🥗    Kale, Spinach & Rocker Smoothie')
streamlit.text('🐔    Hard-Boiled Eggs')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Banana','Avocado'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

#Display api response
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get info on.")
  else:
    streamlit.dataframe(get_fruityvice_data(fruit_choice))
                    
except URLError as e:
  streamlit.error()
                    

    
streamlit.header("The fruit load list contains:")
# Snowflake-related functions
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * FROM pc_rivery_db.public.fruit_load_list")
    return my_cur.fetchall()

if streamlit.button('Get fruit load list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  streamlit.dataframe(get_fruit_load_list())

# don't run after this line 
streamlit.stop()

fruit_add=streamlit.text_input('What fruit would you like to add?')
streamlit.write('The user wants to add ', fruit_add)

my_cur.execute("insert into fruit_load_list values('from streamlit')")
