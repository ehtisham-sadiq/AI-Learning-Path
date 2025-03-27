# This is a Streamlit application that demonstrates various UI components and features
# Streamlit is a powerful Python library for creating web applications with minimal code

# Import necessary libraries
import streamlit as st
from datetime import datetime
import requests

# 1. Basic Text Elements
# These functions create different levels of text hierarchy in the UI
st.title("This is a title")        # Main title of the application
st.header("This is a header")      # Main header
st.subheader("This is a subheader")# Sub-header
st.text("This is a text")          # Regular text
st.write("Hello World")            # Flexible text output that can handle various data types

# 2. Media Elements
# These functions add visual elements to the application
st.image(
    "https://brunop54.sg-host.com/wp-content/uploads/2024/07/AI-for-medical-diagnosis-1024x576.jpg",
    caption="This is a caption",
    width=200
)  # Display an image with caption and specified width
# st.video("https://www.youtube.com/watch?v=9bZkp7q19f0")  # Uncomment to display a video

# 3. Input Elements
# These functions create various interactive input components

# 3.1 Boolean Inputs
st.checkbox("Yes")  # Creates a checkbox
st.button(
    "Click Me",
    icon=":material/mood:",
    type="primary",
    use_container_width=True
)  # Creates a clickable button with styling options

# 3.2 Selection Inputs
st.radio(
    "Select Your Gender",
    ["Male", "Female"]
)  # Creates radio buttons for single selection
st.selectbox(
    "Select Your Country",
    ["Pakistan", "USA", "Canada"]
)  # Creates a dropdown for single selection
st.multiselect(
    "Select Your Hobbies",
    ["Reading", "Writing", "Coding"]
)  # Creates a dropdown for multiple selections

# 3.3 Range Inputs
st.slider(
    "Select Your Age",
    0,
    100
)  # Creates a numeric slider with min and max values
st.select_slider(
    "Pick a mark : ",
    ["A", "B", "C", "D", "F"]
)  # Creates a categorical slider

# 4. Text Input Elements
# These functions create various text input components
st.number_input(
    "Please enter your age : ",
    min_value=0,
    max_value=100
)  # Creates a numeric input field
name = st.text_input(
    "Please enter your name : ",
    value="John Doe",
    placeholder="Enter your name"
)  # Creates a text input field with default value and placeholder
st.title(f"Your name is : {name}")  # Displays the entered name
st.date_input(
    "Please enter your date of birth : ",
    value=datetime.now()
)  # Creates a date picker
st.text_area(
    "Please enter your future goal : ",
    value="I want to become a data scientist",
    placeholder="Enter your future goal",
    height=100,
    max_chars=1000
)  # Creates a multi-line text input
# st.file_uploader("Upload a file : ", type=["jpg", "png", "pdf"])  # Uncomment to add file upload functionality
st.color_picker(
    "Pick a color : ",
    value="#000000"
)  # Creates a color picker
st.progress(40)  # Creates a progress bar

# 5. Notification Elements
# These functions create different types of notifications
st.success("This is a success message")  # Success notification
st.error("This is an error message")     # Error notification
st.warning("This is a warning message")  # Warning notification
st.info("This is an info message")       # Information notification

# 6. Sidebar Elements
# Creates a sidebar for additional navigation or controls
st.sidebar.title("This is a sidebar")

# 7. API Integration
# Example of making an API call to fetch user data
button = st.button("Get Users")
if button:
    # Make a GET request to the users endpoint
    response = requests.get("http://127.0.0.1:8000/v1/users/")
    st.write(response.status_code)  # Display the HTTP status code
    
    # Process and display the response data
    data = response.json()
    for user in data:
        # Each user object contains:
        # - id: User identifier
        # - email: User email address
        # - created_at: Timestamp of user creation
        st.write(f"ID: {user['id']}, Email: {user['email']}")  # Display user information in a formatted way