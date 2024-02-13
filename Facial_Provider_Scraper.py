# Import required libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
from selenium.webdriver.chrome.service import Service

# Function to initialize Chrome WebDriver
def init_webdriver(chrome_driver_path):
    """Initializes and returns the Chrome WebDriver."""
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service)
    return driver

# Function to load and preprocess zip codes from Excel
def load_zip_codes(excel_file_path):
    """Loads zip codes from an Excel file, cleans, and prepares them for processing."""
    df_zip = pd.read_excel(excel_file_path)
    df_zip.drop_duplicates(inplace=True, keep='first')
    df_zip.reset_index(drop=True, inplace=True)
    zipcodes_all = [str(z).zfill(5) for z in df_zip.iloc[:,0]]
    return zipcodes_all

# Function to accept cookies on the page
def accept_cookies(driver):
    """Accepts cookies on the Hydrafacial page if the pop-up appears."""
    try:
        wait = WebDriverWait(driver, 10)
        accept_cookies_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@id="onetrust-accept-btn-handler"]')))
        accept_cookies_btn.click()
    except Exception:
        pass  # Ignore if the cookie button is not found

# Function to perform a search for each zipcode and scrape data
def scrape_data(driver, zipcodes):
    """Searches for Hydrafacial providers by zip code and collects data."""
    data = {
        "Name": [], "Address": [], "Email": [], "Phone": [], "Website": [],
        "IsBlackDiamond": [], "IsConnectMasterCertified": [], "IsSyndeo": [],
        "Connected_names": [], "Diamond_names": [], "Zipcode": []
    }

    for zipcode in zipcodes:
        driver.get('https://www.hydrafacial.com/find-a-provider/')
        accept_cookies(driver)
        time.sleep(2)  # Allow some time for all elements to load properly
        
        try:
            search_box = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//input[@type="text"][@name="storemapper-zip"]')))
            search_box.clear()
            search_box.send_keys(zipcode)
            search_box.send_keys(Keys.ENTER)
            time.sleep(2)  # Wait for the search results to load

            # Click the 'find' button
            driver.find_element(By.XPATH, '//button[@type="button"][@value="find"]').click()
            time.sleep(0.2)

            # Attempt to close any pop-up if present
            try:
                driver.find_element(By.XPATH, '//button[@title="Kapat"]').click()
                time.sleep(0.3)
            except:
                pass  # Ignore if the pop-up is not present
            
            # Scrape the list of providers
            the_list = driver.find_elements(By.XPATH, '//li[@class="tier"]')
            for i in the_list:
                data["Name"].append(i.find_element(By.XPATH, './h4[@aria-label="Location Name"]').text.upper())
                data["Address"].append(i.find_element(By.XPATH, './p[@aria-label="Location Address"]').text)
                data["Phone"].append(i.find_element(By.XPATH, './div/p[@class="storemapper-phone"]/a').text)
                data["Email"].append(i.find_element(By.XPATH, './div/p[@class="storemapper-email"]/a').text)
                data["Website"].append(i.find_element(By.XPATH, './p[@class="storemapper-url"]/a').get_attribute('href'))
                data["IsBlackDiamond"].append("Yes" if i.find_elements(By.XPATH, './div[@class="storemapper-black-diamond"]') else "No")
                data["IsConnectMasterCertified"].append("No")  # Default value as specified
                data["IsSyndeo"].append("No")  # Default value as specified
                data["Zipcode"].append(zipcode)

        except Exception as e:
            print(f"Failed to scrape data for zipcode: {zipcode}. Error: {e}")

    # Convert scraped data into a DataFrame
    df = pd.DataFrame(data)
    return df

# Main function to orchestrate the scraping process
def main():
    # User inputs for paths
    chrome_driver_path = input("Enter the path to your Chrome WebDriver: ")
    excel_file_path = input("Enter the path to your Excel file containing zip codes: ")
    output_file_path = input("Enter the path and filename for the output Excel file (e.g., ./output.xlsx): ")

    driver = init_webdriver(chrome_driver_path)
    zipcodes = load_zip_codes(excel_file_path)
    scraped_data_df = scrape_data(driver, zipcodes)
    scraped_data_df.to_excel(output_file_path, index=False)
    print(f"Data successfully saved to {output_file_path}")
    driver.quit()

if __name__ == "__main__":
    main()
