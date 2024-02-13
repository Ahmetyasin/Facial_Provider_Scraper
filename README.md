## Hydrafacial Location Scraper

### Project Overview

This Python script automates the process of scraping Hydrafacial provider locations from the official Hydrafacial website. It is designed as a console-based application, allowing users to input the path to their Chrome WebDriver, the path to an Excel file containing zip codes of interest, and the desired path for the output Excel file. The script then scrapes various details about the providers and saves the data into an Excel file.

### Scraped Fields

The script scrapes the following fields for each Hydrafacial provider:

- **Name**: The name of the Hydrafacial provider.
- **Address**: The physical address of the provider.
- **Email**: The email address of the provider.
- **Phone**: The phone number of the provider.
- **Website**: The website URL of the provider.
- **IsBlackDiamond**: Indicates if the provider is a Black Diamond provider (`Yes` or `No`).
- **IsConnectMasterCertified**: Indicates if the provider is Connect Master Certified (`Yes` or `No`, always `No` as per current script logic).
- **IsSyndeo**: Indicates if the provider has Syndeo (`Yes` or `No`, always `No` as per current script logic).
- **Connected_names**: Additional connected names related to the provider (scraped but logic for distinction in output needs to be defined by the user).
- **Diamond_names**: Additional diamond names related to the provider (scraped but logic for distinction in output needs to be defined by the user).
- **Zipcode**: The zipcode for which the provider was found.

### Installation

Before running the script, ensure you have Python installed on your system. Then, follow these steps:

1. **Clone the repository** or download the script to your local machine.
2. **Install required Python packages**. Run the following command to install dependencies:

`pip install selenium pandas`

3. **Download Chrome WebDriver**:
- Download the Chrome WebDriver from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads).
- Ensure the WebDriver version matches your Chrome browser's version.
- Extract the downloaded WebDriver to a known location on your filesystem.

### Usage

To use the script:

1. **Prepare your Excel file** with zip codes listed in the first column. Ensure there are no header rows for zip codes.
2. **Open a terminal or command prompt** and navigate to the script's directory.
3. **Run the script** by executing:

`python hydrafacial_scraper.py`

4. **Follow the prompts** to enter:
- The path to your Chrome WebDriver.
- The path to your Excel file containing zip codes.
- The desired output path and filename for the scraped data Excel file.

The script will execute and save the scraped data to the specified Excel file.


