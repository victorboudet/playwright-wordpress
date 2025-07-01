from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import tempfile
import json
import requests

# Set up headless Chrome (still used, though only needed if you scrape HTML pages)
temp_user_data_dir = tempfile.TemporaryDirectory()
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument(f"--user-data-dir={temp_user_data_dir.name}")

driver = webdriver.Chrome(options=options)

blocList = []
blockJson = []

# Load your list of blocks
with open("blocs.json", "r") as f:
    blocList = json.load(f)

for bloc in blocList:
    try:
        # Skip experimental blocks
        if bloc.get("Experimental"):
            continue

        category_slug = bloc["Name"].split("/")[-1]
        url = f"https://raw.githubusercontent.com/WordPress/gutenberg/trunk/packages/block-library/src/{category_slug}/block.json"

        response = requests.get(url)
        response.raise_for_status()
        block_data = response.json()

        bloc_with_json = dict(bloc)  # copy the original bloc
        bloc_with_json["json"] = block_data
        blockJson.append(bloc_with_json)

    except Exception as e:
        print(f"Error accessing {bloc.get('url', 'unknown')}: {e}")

# Save the results
with open("blocsjson.json", "w") as f:
    json.dump(blockJson, f, indent=2, ensure_ascii=False)

driver.quit()
