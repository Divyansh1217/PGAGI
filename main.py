import streamlit as st
import pandas as pd
import hashlib
import re
import os

# Function to hash sensitive data
def hash_data(data):
    return hashlib.sha256(data.encode()).hexdigest()

# Title
st.title("🔍 Secure Resume Screening")

# Name Input
name = st.text_input("Enter your name")

# Email Validation
email = st.text_input("Enter your Email")
email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
if email and not re.match(email_pattern, email):
    st.error("❌ Invalid Email! Please enter a valid email address.")

# Phone Number Validation
phone = st.text_input("Enter your phone number")
phone_pattern = r'^[6-9]\d{9}$'
if phone and not re.match(phone_pattern, phone):
    st.error("❌ Invalid Phone Number! Must start with 6-9 and be 10 digits long.")

# Other Inputs
years_exp = st.number_input("Years of Experience", min_value=0, max_value=50, step=1)
desired_pos = st.text_input("Enter your desired position")
current_loc = st.text_input("Enter your current location")

# Tech Stack Inputs
programming_languages = st.text_area("Programming Languages (e.g., Python, Java, C++)")
frameworks = st.text_area("Frameworks (e.g., Django, React, FastAPI)")
databases = st.text_area("Databases (e.g., PostgreSQL, MongoDB, SQLite)")
tools = st.text_area("Tools & Technologies (e.g., Docker, Git, Kubernetes)")

# Submit Button
if st.button("Submit"):
    if not (name and email and phone and desired_pos and current_loc):
        st.error("All fields must be filled out!")
    else:
        # Hash email & phone number for privacy
        hashed_email = hash_data(email)
        hashed_phone = hash_data(phone)

        # Create DataFrame
        data = pd.DataFrame({
            "Name": [name],
            "Email (Hashed)": [hashed_email],
            "Phone Number (Hashed)": [hashed_phone],
            "Years of Experience": [years_exp],
            "Desired Position": [desired_pos],
            "Current Location": [current_loc],
            "Programming Languages": [programming_languages],
            "Frameworks": [frameworks],
            "Databases": [databases],
            "Tools & Technologies": [tools]
        })

        # Append to CSV (Avoid Overwriting)
        file_path = "secure_data.csv"
        if os.path.exists(file_path):
            data.to_csv(file_path, mode="a", header=False, index=False)
        else:
            data.to_csv(file_path, index=False)

        st.success("✅ Resume Data Saved Securely!")
        st.write("### Your Tech Stack:")
        st.write(f"**Programming Languages:** {programming_languages}")
        st.write(f"**Frameworks:** {frameworks}")
        st.write(f"**Databases:** {databases}")
        st.write(f"**Tools & Technologies:** {tools}")
