import re
import csv
import requests
import pandas as pd
from pydoc import text
from bs4 import BeautifulSoup


def extract_link(text):
    # regular expression for pattern matching link
    url_pattern = r'(https?://[^\s]+)'
    match = re.search(url_pattern, str(text))
    if match:
        link = match.group(0)
        # delete quotes if are
        return link.strip('"').strip("'")
    return text

url = 'https://game8.co/games/Genshin-Impact/archives/304759{}'.format(text)

page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
result = soup.select("[class=a-listItem]")
# soup.select("[class=a-listItem]") --> works fine

print("Codes are founded: ")
for link in result:
    print(link)

with open("codes.csv", "w", newline='') as file:
    writer = csv.writer(file)
    writer.writerows(result)

# Load csv skipping with incorect amoutn of collums
format_file = pd.read_csv('codes.csv', header=None, engine='python', on_bad_lines='skip')
# extracting links
format_file = format_file.apply(lambda col: col.apply(extract_link))

# filtering rows letting only those where the amount of collums equal 2
filtered_file = format_file[format_file.count(axis=1) == 2]

# rewrite our file
filtered_file.to_csv('codes.csv', index=False, header=False)