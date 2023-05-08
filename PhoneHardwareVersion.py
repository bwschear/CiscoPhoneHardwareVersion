import csv
import requests
from bs4 import BeautifulSoup

# Read URLs from input CSV file
with open('IPAddresses.csv', 'r') as input_file:
    reader = csv.reader(input_file)
    urls = [row[0] for row in reader]

# Write scraped data to output CSV file
with open('output.csv', 'w', newline='') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(['URL', 'MAC Address', 'Model Number', 'Hardware revision'])

    # Cycle through URLs and scrape data
    for url in urls:
        # Prepend http:// to the URL if it doesn't already have a protocol specified
        if not url.startswith('http'):
            url = 'http://' + url

        # Concatenate the endpoint to the URL
        url = url.rstrip('/') + '/CGI/Java/Serviceability?adapter=device.statistics.device'

        try:
            # Make a request to the URL and parse the HTML response
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find MAC Address, Model Number, and Hardware revision information in the HTML
            mac_address_element = soup.find('b', string=' MAC address')
            mac_address = mac_address_element.find_next('b').text.strip() if mac_address_element else 'Data not found'

            model_number_element = soup.find('b', string=' Model number')
            model_number = model_number_element.find_next('b').text.strip() if model_number_element else 'Data not found'

            hw_revision_element = soup.find('b', string=' Hardware revision')
            hw_revision = hw_revision_element.find_next('b').text.strip() if hw_revision_element else 'Data not found'

            # Write scraped data to output CSV file
            writer.writerow([url, mac_address, model_number, hw_revision])
        except Exception as e:
            print(f"An error occurred while processing {url}: {str(e)}")
            writer.writerow([url, 'Data not found', 'Data not found', 'Data not found'])

