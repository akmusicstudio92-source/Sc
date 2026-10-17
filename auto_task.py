import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager # Render par Selenium Manager better kaam karta hai
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

TARGET_URL = "https://techaffy.affitra.app/offer?id=2438&aff=6825&aff_click_id=D-22052199-1792199868-34G121G235G22-UDVMH7266&source=771272"
POSTBACK_BASE_URL = "https://acebotechnologiespvtltd122217.o18a.com/p?tid="
WAIT_TIME = 72 

def extract_click_id(url):
    try:
        if "aff_click_id=" in url:
            extracted = url.split("aff_click_id=")[1]
            print(f"[+] Extracted TID: {extracted}")
            return extracted
        return None
    except Exception as e:
        print(f"[-] Error: {e}")
        return None

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage") # Render ke liye bahut zaroori hai
    chrome_options.add_argument("--single-process") # RAM bachane ke liye
    chrome_options.add_argument("--no-zygote")       # RAM bachane ke liye
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.181 Mobile Safari/537.36")

    # Render par direct driver use karein
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def run_automation():
    print("=== Automation Script Start ===")
    extracted_tid = extract_click_id(TARGET_URL)
    if not extracted_tid:
        return

    final_postback_url = POSTBACK_BASE_URL + extracted_tid
    driver = setup_driver()

    try:
        print(f"[*] Opening URL...")
        driver.get(TARGET_URL)
        time.sleep(5) 

        print("[*] 'COMPLETE TASK' button dhundh rahe hain...")
        try:
            button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'COMPLETE TASK')]"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            time.sleep(1)
            button.click()
            print("[+] Button Click Ho Gaya!")
        except Exception as e:
            print(f"[-] Button click nahi ho paya: {e}")
            return

        print(f"[*] Ab {WAIT_TIME} seconds ka wait shuru...")
        time.sleep(WAIT_TIME)

        print(f"[*] Firing Postback...")
        headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G973F)'}
        response = requests.get(final_postback_url, headers=headers, timeout=10)
        print(f"[+] Postback Status Code: {response.status_code}")

    except Exception as e:
        print(f"[-] Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    while True:
        run_automation()
        print("[*] Next cycle in 10 seconds...")
        time.sleep(10)
