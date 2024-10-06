import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define the URL of the page to scrape (replace with the actual sightings page)
url = 'https://journeynorth.org/sightings/querylist.html?map=monarch-adult-fall&year=2019&season=fall'  # Replace with the actual URL for monarch sightings

# Send a GET request to fetch the page content
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    print("Successfully fetched the page.")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

# Parse the content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table containing sightings data
# Inspect the page to find the correct tags/classes for the table
table = soup.find('table')  # Add the appropriate class or ID of the table if needed

# Extract table rows
rows = table.find_all('tr')

# Process data and extract into lists
data = []
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    if cols:  # Ignore empty rows
        data.append(cols)

# Print data to inspect the number of columns being scraped
print(data)

# Check if the data has 8 columns instead of 7
# Modify the columns based on the number of columns in the data

if len(data) > 0 and len(data[0]) == 8:
    # If 8 columns are present, add an extra column name
    df = pd.DataFrame(data, columns=['SNo','Date', 'Town', 'State/Province', 'Latitude', 'Longitude', 'Number', 'Image'])
elif len(data) > 0 and len(data[0]) == 7:
    # If 7 columns, use the original column names
    df = pd.DataFrame(data, columns=['Date', 'Town', 'State/Province', 'Latitude', 'Longitude', 'Number', 'Image'])
else:
    print(f"Unexpected number of columns: {len(data[0])} found.")

# Display the DataFrame to ensure it's correct
print(df.head())

# Save the data to a CSV file for later use
df.to_csv('/Users/duthie/Desktop/Datathon/monarch_sightings_2019.csv', index=False)

