import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import undetected_chromedriver as uc
import random
import pdb

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def extract_links(text):
    url_pattern = r"https?://(?:www\.)?(?:facebook|youtube)\.com/[\w\-./?=&#]+"
    return re.findall(url_pattern, text)


links = []
with open("facebook_links.txt", "r", encoding="utf-8") as file:
    for line in file:
        links.extend(extract_links(line))

links = list(set(links))

try:
    options = uc.ChromeOptions()
    options.add_argument("--user-data-dir=C:/Users/nguye/AppData/Local/Google/Chrome/User Data")  # Thay YOUR_USERNAME bằng tên user của bạn
    # options.add_argument("--profile-directory=Profile 7")  # Hoặc thay bằng profile cụ thể

    driver = uc.Chrome(options=options)
    driver.maximize_window()
except Exception as e:
    print(f"Lỗi start chrome: {e}")



for link in links:
    try:
        driver.get(link)
        time.sleep(2) 
        
        if "facebook.com" in link:
            popup = driver.find_elements(By.XPATH, "//div[@role='dialog']")
            is_popup = len(popup) > 0

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
                    like_button.click()
                    print(f"👍 Đã like: {link}")
                else:
                    print(f"✅ Đã like trước đó, bỏ qua: {link}")
            else:
                print(f"Không tìm thấy nút Like: {link}")

        elif "youtube.com" in link:
            # 🟢 Tìm phần tử cha có id="like-button"
            like_button = driver.find_element(By.ID, "like-button")

            # 🟢 Kiểm tra trong phần tử con
            button = like_button.find_element(By.XPATH, ".//button[@aria-pressed]")  
            if button:
                # Kiểm tra trạng thái like
                if button.get_attribute("aria-pressed") == "false":
                    driver.execute_script("arguments[0].click();", button)
                    print(f"👍 Đã like: {link}!")
                else:
                    print(f"✅ Đã like trước đó, bỏ qua: {link}")
            else:
                print(f"❌ Không tìm thấy button bên trong. {link}")

        elif "instagram.com" in link:
            # Tìm nút like (svg có aria-label="Like")
            # like_button = driver.find_element(By.XPATH, "//svg[@aria-label='Like']")
            like_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//svg[@aria-label='Like']"))
            )

            if like_button:
                button_parent = like_button.find_element(By.XPATH, "./ancestor::div[@role='button'] | ./ancestor::button")
                if button_parent:
                    driver.execute_script("arguments[0].click();", button_parent)
                    print(f"👍 Đã like! {link}")
                else:
                    print(f"❌ Không tìm thấy nút Like. {link}")
            else:
                # Kiểm tra nếu đã like trước đó (tìm Unlike)
                unlike_button = driver.find_elements(By.XPATH, "//svg[@aria-label='Unlike']")

                if unlike_button:
                    print(f"✅ Đã like trước đó, bỏ qua. {link}")
                else:
                    print(f"❌ Không tìm thấy nút Like hoặc Unlike. {link}")
            

        time.sleep(random.uniform(0, 2))
    except Exception as e:
        print(f"Lỗi khi xử lý {link}: {e}")

print("Hoàn thành!")
driver.quit()
