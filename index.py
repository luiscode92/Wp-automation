import streamlit as st
import pandas as pd
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def send_whatsapp_message(phone_number, message):
    # Function to send WhatsApp message using Twilio

    # Initialize Chrome driver
    chromedriver_path = "/usr/local/bin/chromedriver"
    driver = webdriver.Chrome(chromedriver_path)

    # Loop through the numbers and send the message
    for phone in phone_number:
        # Compose the WhatsApp Web URL with the phone number
        url = f"https://web.whatsapp.com/send?phone={phone}&text={message}"

        # Load the WhatsApp Web URL
        driver.get(url)

        # Wait for the chat window to load
        time.sleep(5)

        # Find and click the "send" button
        wait = WebDriverWait(driver, 30)  # Change the timeout value (30 seconds) as needed
        send_button = wait.until(EC.presence_of_element_located((By.XPATH, '//span[@data-icon="send"]')))
        send_button.click()

        # Wait for the message to be sent before moving on to the next number
        time.sleep(10)

    # Close the Chrome driver
    driver.quit()

st.title('Send WhatsApp Message')

# Input text component
message = st.text_input('Enter message')

# File upload button
file = st.file_uploader('Upload file')

# Submit button
if st.button('Send'):
    if file is not None:
        # Load the uploaded file into a pandas dataframe
        df = pd.read_csv(file)
        print(df)
        
        # Extract phone numbers from the dataframe
        phone_numbers = df['phone'].tolist()

        # Send WhatsApp message
        #send_whatsapp_message(phone_numbers, message)

        # Print success message
        st.success('Message sent successfully')
    else:
        st.warning('Please upload a CSV file.')
