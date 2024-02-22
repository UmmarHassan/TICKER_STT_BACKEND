import requests
from bs4 import BeautifulSoup
# URL of the webpage to scrape
url = 'https://en.wikipedia.org/wiki/Main_Page'
# Send an HTTP GET request to the URL
response = requests.get(url)
# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the content of the webpage using Beautiful Soup
    soup = BeautifulSoup(response.content, 'html.parser')
    # Find specific elements in the webpage using BeautifulSoup methods
    # For example, let's say we want to extract all the links from the page
    links = soup.find_all('a')
    # Print the links found on the webpage
    for link in links:
        print(link.get('href'))
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")