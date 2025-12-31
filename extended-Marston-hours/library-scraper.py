from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import csv
from datetime import datetime
import pytz
import os

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.uflib.ufl.edu/status/")
time.sleep(3)

target_ids = ["currocclw", "currocc", "currocchscl", "curroccafa", "curroccedu", "curroccsmath", "currocclacc", "curroccgrr", "curroccmap", "curroccpanama"]

est = pytz.timezone('US/Eastern')
timestamp = datetime.now(est).strftime("%Y-%m-%d %H:%M:%S")

data = {"timestamp": timestamp}
for id_name in target_ids:
    try:
        element = driver.find_element(By.ID, id_name)
        count = element.text
        print(f"{id_name}: {count}")
        data[id_name] = count
    except:
        print(f"{id_name}: Not found")
        data[id_name] = "Not found"

driver.quit()

# Write to CSV (append mode)
file_exists = os.path.isfile('library_occupancy.csv')
with open('library_occupancy.csv', 'a', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["timestamp"] + target_ids)
    if not file_exists:
        writer.writeheader()
    writer.writerow(data)

print(f"\nData saved to library_occupancy.csv at {timestamp} EST")
