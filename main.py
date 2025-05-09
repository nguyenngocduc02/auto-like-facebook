import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import os

def extract_links(text):
    url_pattern = r"https?://(?:www\.)?(?:facebook|youtube|instagram)\.com/[\w\-./?=&#]+"
    return re.findall(url_pattern, text)

# Load links
links = []
with open("facebook_links.txt", "r", encoding="utf-8") as file:
    for line in file:
        links.extend(extract_links(line))
links = list(set(links))

# Load comments
isComment = True
comments = []
if isComment:
    with open("comment.txt", "r", encoding="utf-8") as file:
        comments = [comment.strip() for comment in file.readlines() if comment.strip()]

# ChromeDriver setup for version 136
try:
    # Path to ChromeDriver executable (ensure ChromeDriver 136 is downloaded)
    chromedriver_path = "path/to/chromedriver"  # Replace with actual path to chromedriver.exe
    service = Service(chromedriver_path)
    
    # Chrome options
    options = webdriver.ChromeOptions()
    
    # Use user profile (adjust path for your system)
    user_data_dir = os.path.expanduser("~") + "/AppData/Local/Google/Chrome/User Data"  # Windows
    # For Linux: user_data_dir = os.path.expanduser("~/.config/google-chrome")
    # For macOS: user_data_dir = os.path.expanduser("~/Library/Application Support/Google/Chrome")
    
    options.add_argument(f"--user-data-dir={user_data_dir}")
    options.add_argument("--profile-directory=Profile 4")  # Adjust profile if needed
    options.add_argument("--no-sandbox")  # Optional for stability
    options.add_argument("--disable-dev-shm-usage")  # Optional for stability
    
    # Initialize driver
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
except Exception as e:
    print(f"Error starting Chrome: {e}")
    exit()

# Process each link
for link in links:
    try:
        driver.get(link)
        time.sleep(2)  # Initial page load wait

        if "facebook.com" in link:
            # Handle potential popups
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            popup = driver.find_elements(By.XPATH, "//div[@role='dialog']")
            is_popup = len(popup) > 0

            # Locate like button
            if is_popup:
                like_buttons = driver.find_elements(By.XPATH, "//div[@role='dialog']//div[@aria-label='Like' or @aria-label='Thích']")
            else:
                like_buttons = driver.find_elements(By.XPATH, "//div[@aria-label='Like' or @aria-label='Thích']")

            if like_buttons:
                like_button = like_buttons[0]
                aria_label = like_button.get_attribute("aria-label")
                aria_pressed = like_button.get_attribute("aria-pressed")
                already_liked = aria_label in ["Like", "Thích"] and aria_pressed == "true"

                if not already_liked:
                    driver.execute_script("arguments[0].click();", like_button)
                    print(f"👍 Liked: {link}")
                else:
                    print(f"✅ Already liked, skipping: {link}")
            else:
                print(f"❌ Like button not found: {link}")

            # Comment on Facebook
            if isComment:
                time.sleep(1)
                random_comment = random.choice(comments)

                # Locate comment box
                comment_box = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[contenteditable="true"]'))
                )
                if comment_box:
                    comment_box.click()
                    comment_box.send_keys(random_comment)
                    time.sleep(1)
                    comment_box.send_keys(Keys.ENTER)
                    print(f"💬 Commented: {link}")
                else:
                    print(f"❌ Comment box not found: {link}")

        elif "youtube.com" in link:
            # Locate like button
            like_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "like-button"))
            )
            button = like_button.find_element(By.XPATH, ".//button[@aria-pressed]")
            if button:
                if button.get_attribute("aria-pressed") == "false":
                    driver.execute_script("arguments[0].click();", button)
                    print(f"👍 Liked: {link}")
                else:
                    print(f"✅ Already liked, skipping: {link}")
            else:
                print(f"❌ Like button not found: {link}")

        elif "instagram.com" in link:
            # Locate like button
            like_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//svg[@aria-label='Like']"))
            )
            if like_button:
                button_parent = like_button.find_element(By.XPATH, "./ancestor::div[@role='button'] | ./ancestor::button")
                if button_parent:
                    driver.execute_script("arguments[0].click();", button_parent)
                    print(f"👍 Liked: {link}")
                else:
                    print(f"❌ Like button parent not found: {link}")
            else:
                # Check if already liked
                unlike_button = driver.find_elements(By.XPATH, "//svg[@aria-label='Unlike']")
                if unlike_button:
                    print(f"✅ Already liked, skipping: {link}")
                else:
                    print(f"❌ Neither Like nor Unlike button found: {link}")

        time.sleep(2)  # Post-action wait
    except Exception as e:
        print(f"Error processing {link}: {e}")

print("Completed!")
driver.quit()