from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import tempfile
import json
import re
from bs4 import BeautifulSoup

# Setup headless browser
temp_user_data_dir = tempfile.TemporaryDirectory()
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument(f"--user-data-dir={temp_user_data_dir.name}")
driver = webdriver.Chrome(options=options)

# Open the page
driver.get("https://developer.wordpress.org/block-editor/reference-guides/core-blocks/")

# Get all <ul> elements
ul_elements = driver.find_elements(By.TAG_NAME, "ul")

# Process each <ul>
all_ul_data = []

for ul in ul_elements:
    ul_html = ul.get_attribute("outerHTML")
    soup = BeautifulSoup(ul_html, "html.parser")

    ul_dict = {}
    for li in soup.find_all("li"):
        strong = li.find("strong")
        if strong:
            key = strong.get_text(strip=True).rstrip(":")
            strong.extract()  # Remove <strong> so only value remains
            # Replace <s> with ~text~ or remove them entirely
            value = li.get_text(strip=True)
            value = re.sub(r'\s+', ' ', value)
            value = re.sub(r'~+', '~', value)
            value = value.replace("~", "")
            ul_dict[key] = value
    if ul_dict:
        all_ul_data.append(ul_dict)

driver.quit()

# Output
with open("blocs.json", "w") as f:
    json.dump(all_ul_data, f, indent=2)
