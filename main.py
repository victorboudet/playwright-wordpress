from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import tempfile
import json

# Set up headless Chrome with temporary profile (ideal for VPS)
temp_user_data_dir = tempfile.TemporaryDirectory()
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument(f"--user-data-dir={temp_user_data_dir.name}")

driver = webdriver.Chrome(options=options)

# ✅ Function to get all post links from a page
def getOnPage(link: str):
    driver.get(link)
    driver.implicitly_wait(2)
    posts = driver.find_elements(By.CLASS_NAME, "wp-block-post")

    page_links = []
    for post in posts:
        try:
            link_element = post.find_element(By.TAG_NAME, "a")
            href = link_element.get_attribute("href")
            if href:
                page_links.append(href)
        except:
            print("No link found in post")
    return page_links

# ✅ Go through all pages and collect all links
linkList = []
for i in range(1, 50):
    print(f"Processing page {i}")
    page_links = getOnPage(f"https://wordpress.org/patterns/page/{i}/?curation=all")
    linkList.extend(page_links)

# ✅ Save to JSON file
with open("links.json", "w") as f:
    json.dump(linkList, f, indent=2)

# ✅ Clean up
driver.quit()
temp_user_data_dir.cleanup()
