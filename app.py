import csv
import pandas as pd
import time
import streamlit as st
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Define the function to send a WhatsApp message using Selenium
def send_whatsapp_message(df, message):

    # Loop through each row and send the message to each user
    for index, row in df.iterrows():
        phone = row['phone'] 
        send_message(phone, message)
        st.success(f"Message sent to {phone}")

        # Wait 5 seconds before sending the next message
        time.sleep(5)


# Define the function to send a WhatsApp message
def send_message(phone, message):
     # Initialize Chrome driver
    chromedriver_path = "/usr/local/bin/chromedriver"
    driver = webdriver.Chrome(chromedriver_path)
    # Compose the WhatsApp Web URL with the phone number and message
    url = f"https://web.whatsapp.com/send?phone={phone}&text={message}"

    # Load the WhatsApp Web URL
    driver.get(url)

    # Wait for the chat window to load
    time.sleep(5)

    # Find and click the "send" button
    wait = WebDriverWait(driver, 30)  # Change the timeout value (30 seconds) as needed
    send_button = wait.until(EC.presence_of_element_located((By.XPATH, '//span[@data-icon="send"]')))
    send_button.click()

    # Wait for the message to be sent
    time.sleep(10)

# Define the Streamlit app

# Define the Streamlit app
def app():
    st.title("WhatsApp Automation")

    # Upload the CSV file
    csv_file = st.file_uploader("Upload CSV file", type=["csv"])
    if csv_file is not None:
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(csv_file, dtype={"phone": str})

        # Display the DataFrame using Streamlit
        st.dataframe(df)
  
    # Define the message to send
    message = st.text_input("Enter message to send")

    # Define the send button
    if st.button("Send"):
        # Read the CSV file
        if csv_file is not None:
            send_whatsapp_message(df, message)
        else:
            st.error("Please upload a CSV file.")

# Run the Streamlit app
if __name__ == "__main__":
    app()
