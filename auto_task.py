import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- CONFIGURATION ---
# Jis page par "COMPLETE TASK" button hai us page ka URL yahan daalein
TARGET_URL = "https://techaffy.affitra.app/offer?id=2438&aff=6825&aff_click_id=D-22052199-1792199868-34G121G235G22-UDVMH7266&source=771272"

# Postback URL ka base
POSTBACK_BASE_URL = "https://acebotechnologiespvtltd122217.o18a.com/p?tid="

# Wait time (seconds mein)
WAIT_TIME = 72 

def extract_click_id(url):
    """URL se aff_click_id nikalne ka function"""
    try:
        if "aff_click_id=" in url:
            # 'aff_click_id=' ke baad ka hissa nikalna
            extracted = url.split("aff_click_id=")[1]
            print(f"[+] Extracted TID: {extracted}")
            return extracted
        else:
            print("[-] URL mein 'aff_click_id' nahi mila!")
            return None
    except Exception as e:
        print(f"[-] TID extract karne mein error: {e}")
        return None

def setup_driver():
    """Chromium Browser setup karne ka function (Render/Docker ke liye)"""
    chrome_options = Options()
    
    # Headless mode (Bina screen ke chalane ke liye)
    chrome_options.add_argument("--headless=new") 
    
    # Render/Linux server ke liye zaroori flags (RAM aur stability ke liye)
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage") 
    chrome_options.add_argument("--single-process") 
    chrome_options.add_argument("--no-zygote")
    chrome_options.add_argument("--disable-software-rasterizer")
    
    # Window size aur User-Agent set karna
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.181 Mobile Safari/537.36")

    # Chromium ka path (Jo Dockerfile se install hua hai)
    chrome_options.binary_location = "/usr/bin/chromium"
    
    # Driver ka path
    service = Service("/usr/bin/chromedriver")
    
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def run_automation():
    print("\n=== Automation Script Start ===")
    
    # TID extract karein
    extracted_tid = extract_click_id(TARGET_URL)
    if not extracted_tid:
        print("[-] TID nahi mila, script rok rahi hai.")
        return

    final_postback_url = POSTBACK_BASE_URL + extracted_tid
    print(f"[+] Final Postback URL banaya: {final_postback_url}")

    driver = None
    try:
        driver = setup_driver()
        print(f"[*] Opening URL: {TARGET_URL}")
        driver.get(TARGET_URL)
        
        # Page load hone ka wait karein
        time.sleep(5) 

        print("[*] 'COMPLETE TASK' button dhundh rahe hain...")
        
        try:
            # Wait until button is clickable
            button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'COMPLETE TASK')]"))
            )
            # Scroll to button
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            time.sleep(1)
            button.click()
            print("[+] Button Click Ho Gaya!")
            
        except Exception as e:
            print(f"[-] Button click nahi ho paya: {e}")
            print("[*] Shayad page load nahi hua ya button nahi mila.")
            return

        # 72 Seconds ka wait
        print(f"[*] Ab {WAIT_TIME} seconds ka wait shuru (Postback ke liye)...")
        time.sleep(WAIT_TIME)

        # Postback Fire Karein
        print(f"[*] Firing Postback to: {final_postback_url}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.181 Mobile Safari/537.36',
            'Accept': '*/*',
            'Connection': 'keep-alive'
        }

        response = requests.get(final_postback_url, headers=headers, timeout=15)
        
        print(f"[+] Postback Fire Ho Gaya! Status Code: {response.status_code}")
        if response.status_code == 200:
            print("[+] Success! Postback accept ho gaya.")
        else:
            print("[-] Postback fire toh hua par status code 200 nahi hai. Check karein.")

    except Exception as e:
        print(f"[-] Main loop mein error aaya: {e}")
    
    finally:
        if driver:
            print("[*] Closing Browser...")
            driver.quit()

def start_loop():
    """Loop add karne ka function"""
    iteration = 1
    while True:
        print(f"\n========== ITERATION {iteration} ==========")
        try:
            run_automation()
        except Exception as e:
            print(f"[-] Loop mein unexpected error: {e}")
        
        print("\n[*] Ek cycle complete. Agli cycle 10 seconds mein shuru hogi...")
        time.sleep(10)
        iteration += 1

if __name__ == "__main__":
    try:
        start_loop()
    except KeyboardInterrupt:
        print("\n[!] Script manually stop kar di gayi.")
