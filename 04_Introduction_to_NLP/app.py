# Step 2: Create a Streamlit Application

import streamlit as st
import joblib
from preprocessing import text_preprocessing
# Load the saved pipeline
pipe = joblib.load('spam_classifier_pipeline.pkl', mmap_mode=None)

# Streamlit application title
st.title("Spam Detection using Naïve Bayes Classifier")

# User input for SMS
user_input = st.text_area("Enter your message:")

# Button to make prediction
if st.button("Predict"):
    if user_input:
        prediction = pipe.predict([user_input])
        st.write(f"The message is: **{prediction[0]}**")
    else:
        st.write("Please enter a message to classify.")
