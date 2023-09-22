import requests
from bs4 import BeautifulSoup

# URL to fetch
url = "https://a-z-animals.com/animals/addax/"

# Define a custom user agent
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.1234.56 Safari/537.36"
}

# Send an HTTP GET request to the URL with custom headers
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the title tag and extract its text
    title = soup.find('title').text
    
    # Print the title
    print("Title of the page:", title)
    print("soup: ", soup)
else:
    print("Failed to fetch the page. Status code:", response.status_code)
