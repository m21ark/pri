import requests
from bs4 import BeautifulSoup
import time

def get_animal_name_fromURL(url):
    parts = url.split('/')
    return parts[-2].replace('-', ' ').title()


def curl_web(url):

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

        # Remove script and style tags from the parsed HTML
        for script in soup(["script", "style","meta", "link","header","svg","aside", "img"]):
            script.extract()

        def has_noprint_class(tag):
            return tag.has_attr('class') and 'noprint' in tag['class']

        # Find and remove tags with the "noprint" class
        for tag in soup.find_all(has_noprint_class):
            tag.extract()


        # Convert the BeautifulSoup object to a string
        html_string = soup.prettify()

        file_name = "./animals/" + get_animal_name_fromURL(url)
        
        # Write the HTML content to a .txt file
        with open(file_name+".txt", 'w', encoding='utf-8') as file:
            file.write(html_string)
        return 0
    else:
        print("Failed to fetch the page. Status code:", response.status_code)
        return 1


def read_links(file_path):


    counter = 0
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:

            counter += 1
            if counter == 20:
                time.sleep(3)
                counter = 0

            url = line.strip()
            if len(url) == 0:
                break
            name = get_animal_name_fromURL(url)
            res = curl_web(url)

            if (res == 0):
                print(f"Fetched '{name}'")
            else:
                print("Error in curl at name: "+ name)
                break


read_links("animal_links.txt")








