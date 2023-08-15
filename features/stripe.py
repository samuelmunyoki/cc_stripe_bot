import time
import requests
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from telegram import Update
from utils.email_generator import generate_random_email

async def send_card(update: Update, args):
    
    try:
        pattern = r"^\d{16}\|\d{3}\|\d{2}\|\d{2}$"

        if re.match(pattern, args[0]):
            print("Card matches the pattern.")
            
            cc_number, cvv, month, year = args[0].split('|')
            date = ""+month+""+year
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.binary_location = r'../chromedriver_linux64/chromedriver'
            driver = webdriver.Chrome(options=chrome_options)
            driver.get("https://shrlk.xyz")
            iframe_element = driver.find_element(By.CSS_SELECTOR, "iframe[src^='https://js.stripe.com']")
            driver.switch_to.frame(iframe_element)
            email_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "email"))
            )
            email_element.send_keys(f'{generate_random_email()}')
            driver.switch_to.default_content()
            second_iframe_element = driver.find_element(By.CSS_SELECTOR, 'iframe[title="Secure payment input frame"]')
            driver.switch_to.frame(second_iframe_element)
            cc_number_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "Field-numberInput"))
            )
            cc_number_element.clear()
            for digit in cc_number:
                cc_number_element.send_keys(digit)
            expiry_element = driver.find_element(By.ID, "Field-expiryInput")
            expiry_element.clear()
            expiry_element.send_keys(date)
            cvv_element = driver.find_element(By.ID, "Field-cvcInput")
            cvv_element.clear()
            cvv_element.send_keys(cvv)
            driver.switch_to.default_content()
            submit_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "submit"))
            )
            time.sleep(3)
            submit_button.click()
            driver.switch_to.default_content()
            driver.quit()
            api_url = "https://shrlk.xyz/api"
            response = requests.get(api_url)
            
            if response.status_code == 200:
                data = response.json()
                sts = ''
                if data["status"] == "requires_payment_method":
                    sts = "❌ Declined"
                else:
                    sts = data["status"]
                message = f'💳💳 Card Details 💳💳\n\nStatus: {sts}\nCharged: {data["amount"]}\nCurrency: {data["currency"]}\nType: {data["card_types"][0]}'
                await update.message.reply_text(message)
            else:
                await update.message.reply_text(f'Error occured. Contact admin if problem persists.')
        else:
            await update.message.reply_text("❌ Invalid format\n\nUse: cc_number|cvv|month|year \n\neg 4242424242424242|123|09|24")

    except Exception as e:
        print("Error ==== ", e)
        await update.message.reply_text(f'Error occured. Contact admin if problem persists.')