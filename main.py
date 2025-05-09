from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import time
import re
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

def extract_links(text):
    url_pattern = r"https?://(?:www\.)?(?:facebook|youtube|instagram)\.com/[\w\-./?=&#]+"
    return re.findall(url_pattern, text)

def process_links(driver, links, comments, is_comment=False):
    driver.get("https://www.facebook.com")
    time.sleep(10)
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
                if is_comment and comments:
                    time.sleep(1)
                    random_comment = random.choice(comments)

                    # Locate comment box
                    try:
                        comment_box = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[contenteditable="true"]'))
                        )
                        comment_box.click()
                        comment_box.send_keys(random_comment)
                        time.sleep(1)
                        comment_box.send_keys(Keys.ENTER)
                        print(f"💬 Commented: {link}")
                    except:
                        print(f"❌ Comment box not found: {link}")

            elif "youtube.com" in link:
                # Locate like button
                try:
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
                except:
                    print(f"❌ Error locating like button: {link}")

            elif "instagram.com" in link:
                # Locate like button
                try:
                    like_button = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//svg[@aria-label='Like']"))
                    )
                    button_parent = like_button.find_element(By.XPATH, "./ancestor::div[@role='button'] | ./ancestor::button")
                    if button_parent:
                        driver.execute_script("arguments[0].click();", button_parent)
                        print(f"👍 Liked: {link}")
                    else:
                        print(f"❌ Like button parent not found: {link}")
                except:
                    # Check if already liked
                    unlike_button = driver.find_elements(By.XPATH, "//svg[@aria-label='Unlike']")
                    if unlike_button:
                        print(f"✅ Already liked, skipping: {link}")
                    else:
                        print(f"❌ Neither Like nor Unlike button found: {link}")

            time.sleep(2)  # Post-action wait
        except Exception as e:
            print(f"Error processing {link}: {e}")

def main():
    try:
        # Cấu hình Firefox binary (nếu cần)
        firefox_options = Options()
        profile = 'C:/Users/nguye/AppData/Roaming/Mozilla/Firefox/Profiles/{Tên profile}'
        firefox_options.add_argument('-profile')
        firefox_options.add_argument(profile)
        driver = webdriver.Firefox(options=firefox_options)
        
        # Load links
        links = []
        with open("facebook_links.txt", "r", encoding="utf-8") as file:
            for line in file:
                links.extend(extract_links(line))
        links = list(set(links))
        print(f"Loaded {len(links)} unique links")

        # Load comments
        is_comment = False
        comments = []
        if is_comment:
            try:
                with open("comment.txt", "r", encoding="utf-8") as file:
                    comments = [comment.strip() for comment in file.readlines() if comment.strip()]
                print(f"Loaded {len(comments)} comments")
            except FileNotFoundError:
                print("❌ File comment.txt not found, skipping comments")
                is_comment = False

        # Process each link
        if links:
            process_links(driver, links, comments, is_comment)
        else:
            print("❌ No valid links found in facebook_links.txt")

        # Đóng trình duyệt
        driver.quit()
        print("Đã đóng trình duyệt Firefox")

    except Exception as e:
        print(f"Đã xảy ra lỗi: {str(e)}")
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    main()