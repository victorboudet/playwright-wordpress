import json
import time
import tempfile
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Set up headless Chrome with temporary profile (ideal for VPS)
temp_user_data_dir = tempfile.TemporaryDirectory()
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument(f"--user-data-dir={temp_user_data_dir.name}")

driver = webdriver.Chrome(options=options)

# Load previously scraped URLs
with open("links.json", "r") as f:
    linkList = json.load(f)

results = []
size = len(linkList)
progress = 0

for link in linkList:
    print(f"{progress}/{size} Processing: {link}")
    progress += 1
    try:
        driver.get(link)
        time.sleep(2)

        # Get the copied pattern
        hidden_input = driver.find_element(By.CLASS_NAME, "wp-block-wporg-copy-button__content")
        encoded_value = hidden_input.get_attribute("value")
        decoded_pattern = urllib.parse.unquote(encoded_value)

        # Get tags container
        tags_div = driver.find_element(By.CLASS_NAME, "taxonomy-wporg-pattern-category")
        tag_links = tags_div.find_elements(By.TAG_NAME, "a")
        tags = [tag.text for tag in tag_links]  # or tag.get_attribute("href") if you want URLs

        results.append({
            "url": link,
            "pattern": decoded_pattern,
            "tags": tags
        })

        with open("patterns.json", "w") as f:
            json.dump(results, f, indent=2)

    except Exception as e:
        print(f"Error on {link}: {e}")


# Clean up
driver.quit()
temp_user_data_dir.cleanup()
