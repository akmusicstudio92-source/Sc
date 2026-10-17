import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
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
    """Chrome Browser setup karne ka function (Headless mode)"""
    chrome_options = Options()
    # Agar aapko browser screen par dekhna hai, toh neeche wali line comment kar dein
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # User-Agent set karna (Mobile view simulate karne ke liye)
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.181 Mobile Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def run_automation():
    print("=== Automation Script Start ===")
    
    # TID extract karein
    extracted_tid = extract_click_id(TARGET_URL)
    if not extracted_tid:
        print("[-] TID nahi mila, script rok rahi hai.")
        return

    final_postback_url = POSTBACK_BASE_URL + extracted_tid
    print(f"[+] Final Postback URL banaya: {final_postback_url}")

    driver = setup_driver()

    try:
        print(f"[*] Opening URL: {TARGET_URL}")
        driver.get(TARGET_URL)
        
        # Page load hone ka wait karein (Max 15 seconds)
        time.sleep(5) 

        # "COMPLETE TASK" button dhundhein aur click karein
        # XPath ka use karke text ke basis par button dhundh rahe hain
        print("[*] 'COMPLETE TASK' button dhundh rahe hain...")
        
        # Try multiple locator strategies just in case
        try:
            # Wait until button is clickable
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'COMPLETE TASK')]"))
            )
            # Scroll to button
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            time.sleep(1)
            button.click()
            print("[+] Button Click Ho Gaya!")
        except Exception as e:
            print(f"[-] Button click nahi ho paya: {e}")
            print("[*] Shayad page load nahi hua ya button ka text alag hai. Script ruk rahi hai.")
            return

        # 72 Seconds ka wait
        print(f"[*] Ab {WAIT_TIME} seconds ka wait shuru (Postback ke liye)...")
        time.sleep(WAIT_TIME)

        # Postback Fire Karein
        print(f"[*] Firing Postback to: {final_postback_url}")
        
        # Headers dalna zaroori hai taaki block na ho
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.181 Mobile Safari/537.36',
            'Accept': '*/*',
            'Connection': 'keep-alive'
        }

        response = requests.get(final_postback_url, headers=headers, timeout=10)
        
        print(f"[+] Postback Fire Ho Gaya! Status Code: {response.status_code}")
        if response.status_code == 200:
            print("[+] Success! Postback accept ho gaya.")
        else:
            print("[-] Postback fire toh hua par status code 200 nahi hai. Check karein.")

    except Exception as e:
        print(f"[-] Main loop mein error aaya: {e}")
    
    finally:
        print("[*] Closing Browser...")
        driver.quit()

def start_loop():
    """Loop add karne ka function"""
    iteration = 1
    while True:
        print(f"\n========== ITERATION {iteration} ==========")
        run_automation()
        
        print("\n[*] Ek cycle complete. Agli cycle 10 seconds mein shuru hogi...")
        # Next loop se pehle thoda wait
        time.sleep(10)
        iteration += 1

if __name__ == "__main__":
    try:
        start_loop()
    except KeyboardInterrupt:
        print("\n[!] Script manually stop kar di gayi.")
