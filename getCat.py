from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import tempfile
import json
import requests

# Set up headless Chrome with temporary profile (ideal for VPS)
temp_user_data_dir = tempfile.TemporaryDirectory()
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument(f"--user-data-dir={temp_user_data_dir.name}")

driver = webdriver.Chrome(options=options)

catList = []
driver.get("https://developer.wordpress.org/block-editor/reference-guides/core-blocks/")
cats = driver.find_elements(By.CLASS_NAME, "is-toc-heading")
for cat in cats:
    catList.append(cat.text.lower().replace(" ", "-"))
print(catList)

blocks = []

for cat in catList:
    try:
        url = f"https://raw.githubusercontent.com/WordPress/gutenberg/trunk/packages/block-library/src/{cat}/block.json"
        print(url)
        response = requests.get(url)
        response.raise_for_status()
        block_data = response.json()
        blocks.append({"name": cat.lower(), "data": block_data})
    except Exception as e:
        print(f"Error processing {cat}: {e}")
        continue

print(blocks)

with open("blocks.json", "w") as f:
    json.dump(blocks, f, indent=2)
