import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import undetected_chromedriver as uc
import random

def extract_links(text):
    url_pattern = r"https?://(?:www\.)?facebook\.com/[\w\-./?=&#]+"
    return re.findall(url_pattern, text)

links = []
with open("facebook_links.txt", "r", encoding="utf-8") as file:
    for line in file:
        links.extend(extract_links(line))

links = list(set(links))

options = uc.ChromeOptions()
options.add_argument("--user-data-dir=C:/Users/USERNAME/AppData/Local/Google/Chrome/User Data")  # Thay YOUR_USERNAME bằng tên user của bạn
options.add_argument("--profile-directory=Default")  # Hoặc thay bằng profile cụ thể

driver = uc.Chrome(options=options)
driver.maximize_window()

for link in links:
    try:
        driver.get(link)
        time.sleep(2) 
        
        like_buttons = driver.find_elements(By.XPATH, "//div[@aria-label='Like' or @aria-label='Thích']")
        if like_buttons:
            like_buttons[0].click()
            print(f"Đã like: {link}")
        else:
            print(f"Không tìm thấy nút Like: {link}")
        
        time.sleep(random.uniform(0, 2)) 
    except Exception as e:
        print(f"Lỗi khi xử lý {link}: {e}")

print("Hoàn thành!")
driver.quit()
