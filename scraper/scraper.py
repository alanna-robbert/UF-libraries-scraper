import argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import csv
from datetime import datetime
import pytz
import os

parser = argparse.ArgumentParser()
parser.add_argument('--ids', nargs='+', required=True, help='Element IDs to scrape')
args = parser.parse_args()

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.uflib.ufl.edu/status/")
time.sleep(3)

est = pytz.timezone('US/Eastern')
timestamp = datetime.now(est).strftime("%Y-%m-%d %H:%M:%S")

rows = []
for id_name in args.ids:
    try:
        element = driver.find_element(By.ID, id_name)
        count = element.text
        print(f"{id_name}: {count}")
    except Exception:
        count = "Not found"
        print(f"{id_name}: Not found")
    rows.append({"timestamp": timestamp, "library_id": id_name, "count": count})

driver.quit()

os.makedirs("data", exist_ok=True)
csv_path = "data/library_occupancy.csv"
file_exists = os.path.isfile(csv_path)

with open(csv_path, 'a', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=["timestamp", "library_id", "count"])
    if not file_exists:
        writer.writeheader()
    writer.writerows(rows)

print(f"\nData saved to {csv_path} at {timestamp} EST")
