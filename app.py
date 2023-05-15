import csv
import pandas as pd
import time
import streamlit as st
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse

# Define the function to send a WhatsApp message using Selenium
def send_whatsapp_message(df, msj):

    # Initialize Chrome driver
    chromedriver_path = "/usr/local/bin/chromedriver"
    driver = webdriver.Chrome(chromedriver_path)

    # List of WhatsApp numbers to send messages to
    #numbers = ['+573226130241', '+573156702559', '+573104983987']

    # Loop through the numbers and send the message
    for index, row in df.iterrows():
        name = row['name']
        phone = row['phone']

        # Format the message with the name
        formatted_message = msj.format(name=name)

        # Encode newlines as %0A in the URL query string
        encoded_message = urllib.parse.quote(formatted_message, safe='')


        # Compose the WhatsApp Web URL with the phone number
        url = f"https://web.whatsapp.com/send?phone={phone}&text={encoded_message}"

        # Load the WhatsApp Web URL
        driver.get(url)

        # Wait for the chat window to load
        time.sleep(5)

        # Find and click the "send" button
        wait = WebDriverWait(driver, 60)  # Create a WebDriverWait object with a timeout of 60 seconds
        send_button_locator = (By.XPATH, '//span[@data-icon="send"]')  # Define the locator for the "send" button

        # Wait until the "send" button is present on the page
        send_button = wait.until(EC.presence_of_element_located(send_button_locator))

        # Click the "send" button
        send_button.click()


        # Wait for the message to be sent before moving on to the next number
        time.sleep(10)

    # Close the Chrome driver
    driver.quit()




# Define the Streamlit app
def app():
    st.title("WhatsApp Automation")
    # Agregar la documentación como texto en formato Markdown
    st.markdown("### Instrucciones de Uso")
    st.markdown("1. Ingresa el mensaje en el siguiente formato: 'Hola, mi nombre es {name}'")
    st.markdown("2. Asegúrate de incluir las llaves {name} como marcador de posición para el nombre real.")
    st.markdown("3. {name} será reemplazado por el nombre de cada usuario en la lista.")
    st.markdown("4. La aplicacion abrira una ventada de whatsapp web, y tomara control de ella, para esto hay que iniciar session desde el numero de Whatsapp desde el que se va a enviar los mensajes")


     # Ejemplo de mensaje para un usuario llamado Luis
    name = "Luis"
    message = f"Hola, mi nombre es {name}"
    st.markdown("**Ejemplo:** (para un usuario llamado Luis)")
    st.markdown("input: Hola, mi nombre es {name}")
    st.markdown(f"output: \n{message}")


    # Upload the CSV file
    csv_file = st.file_uploader("Carga el archivo CSV", type=["csv"])
    if csv_file is not None:
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(csv_file, dtype={"phone": str})

        # Display the DataFrame using Streamlit
        st.dataframe(df)
  
    # Define the message to send
    msj = st.text_area("Entra el mensaje que deseas enviar")

    # Define the send button
    if st.button("Send"):
        # Read the CSV file
        if csv_file is not None:
            send_whatsapp_message(df, msj)
        else:
            st.error("Please upload a CSV file.")

# Run the Streamlit app
if __name__ == "__main__":
    app()
