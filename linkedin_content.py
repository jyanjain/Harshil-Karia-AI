import time
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")

PROFILE_URL = "https://www.linkedin.com/in/harshilk/recent-activity/all/"

SYSTEM_PROMPT = (
    "You are Harshil Karia, a thoughtful entrepreneur who writes with empathy, "
    "storytelling, and clear decision-making frameworks. Your tone blends reflective anecdotes, "
    "actionable insights, and spiritual grounding."
)

options = Options()
# options.add_argument("--headless")
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(options=options)

driver.get("https://www.linkedin.com/login")
time.sleep(2)

driver.find_element(By.ID, "username").send_keys(LINKEDIN_EMAIL)
driver.find_element(By.ID, "password").send_keys(LINKEDIN_PASSWORD)
driver.find_element(By.XPATH, "//button[@type='submit']").click()
time.sleep(5)

driver.get(PROFILE_URL)
time.sleep(5)
    
for _ in range(15):
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
    time.sleep(3)

page_source = driver.page_source
soup = BeautifulSoup(page_source, "html.parser")

posts_data = []

posts = soup.find_all("div", class_="update-components-text")

for post in posts[:100]:  
    content = post.get_text(separator=" ", strip=True)
    
    posts_data.append({
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "assistant", "content": content.strip()}
        ]
    })

with open("harshil_karia_linkedin.json", "w", encoding="utf-8") as f:
    json.dump(posts_data, f, ensure_ascii=False, indent=2)

driver.quit()