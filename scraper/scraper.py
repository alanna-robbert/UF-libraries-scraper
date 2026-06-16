import argparse
import csv
import os
import time
from datetime import datetime

import pytz
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

LIB_IDS = [
    "currocclw", "currocc", "currocchscl", "curroccafa", "curroccedu",
    "curroccsmath", "currocclacc", "curroccgrr", "curroccmap", "curroccpanama",
]

CSV_PATH = "data/library_occupancy.csv"
URL = "https://www.uflib.ufl.edu/status/"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ids", nargs="+", required=True, help="Element IDs to scrape")
    return parser.parse_args()


def make_driver():
    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=opts)


def scrape(driver, ids):
    driver.get(URL)
    time.sleep(3)

    row = {}
    for lib_id in ids:
        try:
            row[lib_id] = driver.find_element(By.ID, lib_id).text
        except Exception:
            row[lib_id] = ""
        print(f"{lib_id}: {row[lib_id] or 'Not found'}")
    return row


def save(row, timestamp):
    os.makedirs("data", exist_ok=True)
    file_exists = os.path.isfile(CSV_PATH)

    with open(CSV_PATH, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp"] + LIB_IDS, extrasaction="ignore")
        if not file_exists:
            writer.writeheader()
        writer.writerow({"timestamp": timestamp, **row})

    print(f"\nData saved to {CSV_PATH} at {timestamp} EST")


def main():
    args = parse_args()
    timestamp = datetime.now(pytz.timezone("US/Eastern")).strftime("%Y-%m-%d %H:%M:%S")

    driver = make_driver()
    try:
        row = scrape(driver, args.ids)
    finally:
        driver.quit()

    save(row, timestamp)


if __name__ == "__main__":
    main()
