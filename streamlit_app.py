# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests  


# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie:cup_with_straw: ")
st.write(
  """Choise the fruits you want in your custom Smoothie!
  """
)
title = st.text_input("Name of Smoothie:")
st.write("The Name of your Smoothie is", title)


cnx = st.connection('snowflake')
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"),col("SEARCH_ON"))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

pd_df = my_dataframe.to_pandas()
ingredient_list = st.multiselect(" Coise up to 5 ingredients!",
                                 my_dataframe,
                                 max_selections=5)

if ingredient_list:
    st.write(ingredient_list)
    st.text(ingredient_list)
    ingredient_string = ''
    
    for chosen_fruit in ingredient_list:
        ingredient_string += chosen_fruit + ' '
        
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == chosen_fruit, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', chosen_fruit,' is ', search_on, '.')
        st.subheader(chosen_fruit + ' Nutrition Information')
      
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+search_on)  
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                    values ('""" + ingredient_string + """', '""" + title + """')"""
    time_to_insert = st.button("Submit Order")
    
    if time_to_insert:
       session.sql(my_insert_stmt).collect()
       st.success('Your Smoothie is ordered!', icon="✅")

    
