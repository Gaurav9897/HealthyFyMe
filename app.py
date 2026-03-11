import os
import pandas as pd
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI

# Lets get the api key from the enviromnt
gemini_api_key = os.getenv('GOOGLE_API_KEY1')


# Lets configure the model

model = ChatGoogleGenerativeAI(
    model= 'gemini-2.5-flash-lite',
    api_key = gemini_api_key)

# Design the UI of application

st.title(':orange[HealthifyMe:] :blue[Your personal Assistant]')
st.markdown('''
This application will assist you to have to get better and customize 
Health advise, you can ask your health related issues and get the personalized guidance.''')
st.write('''
Follow These Steps:
* Enter your details in sidebar
* Rate your activity and fitness on the scale of 0-5
* Submit your details.
* Ask your question on the main page.
* Click generate and relax.''')


# Design the sidebar for all the user parameter
st.sidebar.header(':red[Enter Your Details]')
name= st.sidebar.text_input('Enter Your Name')
gender = st.sidebar.selectbox('Select Your Gender',['Male','Female'])
age = st.sidebar.text_input('Ender Your Age')
weight= st.sidebar.text_input('Enter Your Weight in Kgs')
height= st.sidebar.text_input('Enter Your Height in cms')
bmi = pd.to_numeric(weight)/((pd.to_numeric(height)/100)**2)
active = st.sidebar.slider('Rate your Activity(0-5)',0,5,step=1)
fitness = st.sidebar.slider('Rate your Fitness(0-5)',0,5,step=1)
if st.sidebar.button('Submit'):
    st.sidebar.write(f"{name}, your BMI is {bmi:.2f} Kg/m²")


# Lets use the gemini model to generate the report
user_input = st.text_input('Ask me your question.')
prompt =f'''
<Role> You are an expert in health and wellness and has 10+ years experience in health guidance
<Goal> Generate the customize report addressing the problem of the user
Here is the qustion that has asked.
<Context> Here are the details that the user has provided.
Name = {name}
Age = {age}
Gender = {gender}
Height = {height} cm
Weight = {weight} kg
BMI = {bmi:.2f} kg/m²
Activity rating (0-5) ={activity_level}
Fitness rating (0-5) = {fitness}

<Format>
* Start with the 2-3 line of comment on the details that user has provided
* Explain what the real problem could be on the basis of input the user has provided
* Suggest the possible reasons for the problem 
* What are the possible solutions.
* Mention the doctor from which specialization can be visited if required
* Mention any change in the diet which is required
* In last creat a final summary of all the things that has been discussed

<Instructions>
* Use bullet points where ever possible.
* Create tables to represent any data where ever possible.
* Strictly do not advice any medicine.'''

if st.button('Generate'):
    response = model.invoke(prompt)
    st.write(response.content)



