import json
import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

load_dotenv()

SYSTEM_PROMPT = (
    "You are Harshil Karia, a thoughtful entrepreneur who writes with empathy, "
    "storytelling, and clear decision-making frameworks. Your tone blends reflective anecdotes, "
    "actionable insights, and spiritual grounding."
)

IG_USER = os.getenv("IG_USER") 
IG_PASS = os.getenv("IG_PASS")

profile_link = "https://www.instagram.com/harshiljkaria/"

options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(options=options)
    
driver.get("https://www.instagram.com/accounts/login/")
time.sleep(5)

username_input = driver.find_element(By.NAME, "username")
password_input = driver.find_element(By.NAME, "password")
username_input.send_keys(IG_USER)
password_input.send_keys(IG_PASS)

driver.find_element(By.XPATH, "//button[@type='submit']").click()
time.sleep(7)

driver.get(profile_link)
time.sleep(5)

seen_captions = set()
captions = []

for _ in range(6):
    img_elements = driver.find_elements(By.XPATH, '//div[@class="_aagv"]/img')
    
    for img in img_elements:
        alt_text = img.get_attribute("alt")
        try:
            alt_text.split(".")[1]
        except:
            pass
        if alt_text and alt_text not in seen_captions:
            seen_captions.add(alt_text)
            captions.append({
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "assistant", "content": alt_text}
                ]
            })
    
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
    time.sleep(3)
    
with open("harshil_karia_instagram.json", "w", encoding="utf-8") as f:
    json.dump(captions, f, ensure_ascii=False, indent=2)

driver.quit()

# L = instaloader.Instaloader()

# L.login(IG_USER, IG_PASS)
# profile = instaloader.Profile.from_username(L.context, USERNAME)

# posts_data = []

# for count, post in enumerate(profile.get_posts()):
#     if count >= 30:
#         break
    
#     posts_data.append({
#         "caption": post.caption
#     })
#     time.sleep(3)