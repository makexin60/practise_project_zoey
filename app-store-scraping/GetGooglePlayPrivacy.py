import itertools
import json
import threading
import shutil
import hashlib
import time
import datetime
from concurrent.futures import ThreadPoolExecutor
from google_play_scraper import app
from selenium.common.exceptions import TimeoutException, WebDriverException
import GetCommon
import requests
from readabilipy import simple_json_from_html_string
import GetCommon
import json
from bs4 import BeautifulSoup
import re
import requests
from langdetect import detect, LangDetectException
import time
import os
from bs4 import BeautifulSoup
from readabilipy import simple_json_from_html_string
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_all_privacy_threaded():
    data = GetCommon.get_app_info(appInfo_google_path)
    with ThreadPoolExecutor(max_workers=MAX_CONCURRENT_THREADS) as executor:
        for batch in batch_iterator(data, BATCH_SIZE):  # Process batch by batch
            list(executor.map(process_item, batch))  # Map ensures tasks complete in this batch

def batch_iterator(iterable, batch_size):
    """Yield items from iterable in chunks (batches) of batch_size."""
    iterator = iter(iterable)
    while batch := list(itertools.islice(iterator, batch_size)):
        yield batch

def process_item(item):
    with driver_lock:  # Ensure thread-safe access to the driver
        get_privacy_url(item)

def get_privacy(item,all_app_ids):  
    print(f"Processing item: {item} - length:{len(all_app_ids)}")

    url = item['privacy_policy_url']
    app_id = item['app_id']
    dir_path = f"pythonProject/Policy_google/{app_id}"

    try:
        response = requests.get(url, timeout=15)
        if response.status_code in [200, 403,406,429]:
            try:
                # if detect(response.text) != "en":
                #     GetCommon.save_add_json_file(r"pythonProject\AppInfo_google\non_en.json", item)
                #     return
                # else:
                driver.get(url)

                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                time.sleep(1)  # Allow time for the page to load

                original_html_string = driver.page_source

                html_string = re.sub(r'<\?xml.*?\?>', '', original_html_string)
                soup = BeautifulSoup(html_string, "lxml")

                for tag in soup.find_all(["header", "footer"]):
                    tag.decompose()

                for tag in soup.find_all(class_=lambda c: c and ("header" in c.lower() or "footer" in c.lower())):
                    tag.decompose()
                    
                html_string = str(soup)  

                result = simple_json_from_html_string(html_string, use_readability=True)

                # if not result or "plain_text" not in result:
                #     logger.error(f"Failed to parse privacy policy for {item}")
                #     print(f"Failed to parse privacy policy for {item}")
                # elif len(result["plain_text"]) <= 2:
                get_privacy_without_lib(original_html_string,item,app_id,dir_path,all_app_ids)
                # else:
                #     os.makedirs(dir_path, exist_ok=True) 
                #     with open(f"{dir_path}/{app_id}_policy.txt", "w", encoding="utf-8") as f:
                #         for item in result["plain_text"]:
                #             if isinstance(item, dict) and "text" in item:
                #                 f.write(item["text"] + "\n\n") 

                if len(all_app_ids) != 1:
                    GetCommon.save_add_json_file(r"pythonProject/a.json",app_id)
                    get_same_privacy_url_privacy(dir_path,app_id,all_app_ids)
                            
            except LangDetectException as e:
                print(f"LangDetectException:{e}")
                GetCommon.save_add_json_file(r"pythonProject\AppInfo_google\have_privacy_url_Language_detection_failed.json", item)
            except Exception as e:
                print(f"Error processing {item}: {e}")
                GetCommon.save_add_json_file(f"pythonProject/AppInfo_google/have_privacy_url_{response.status_code}.json", item)
        elif response.status_code in [404]:
            GetCommon.save_add_json_file(f"pythonProject\AppInfo_google\have_privacy_url_cant_open.json", item)
        else:
            GetCommon.save_add_json_file(f"pythonProject/AppInfo_google/have_privacy_url_{response.status_code}.json", item)
    except requests.exceptions.RequestException as e:
        print(f"Request failed for {item}: {e}")
        GetCommon.save_add_json_file(r"pythonProject\AppInfo_google\have_privacy_url_cant_open.json", item)
    except Exception as e:
        print(f"Error processing {item}:{e}")
        logger.error(f"Error processing {item}:{e}")

def get_same_privacy_url_privacy(dir_path,app_id,all_app_ids):
    print(f"app_id: {app_id} has same privacy num: {len(all_app_ids)} ")

    with open(f"{dir_path}/{app_id}_policy.txt", 'r', encoding='utf-8') as src_file:
        content = src_file.read()

    for filename in all_app_ids:
        new_file_path = f"{dir_path}/{filename}_policy.txt"
        with open(new_file_path, 'w', encoding='utf-8') as new_file:
            new_file.write(content)

if __name__ == "__main__":
    MAX_CONCURRENT_THREADS = 20  # Limit concurrent threads
    BATCH_SIZE = 200  # Control how many items to load into memory at a time
    limit_time = 1
    logger = GetCommon.getLogger("GooglePlayPrivacymethod2")

    have_privacy_app_info_path = r"pythonProject\AppInfo_google\have_privacy_app_info.json"
    not_have_privacy_url_path = r"pythonProject\AppInfo_google\not_have_privacy_url.json"
    appInfo_google_path = r"pythonProject\AppInfo_google\appInfo_google.json"
    category_privacy_url_dir_path =  r"C:\Users\smile\PycharmProjects\pythonProject\privacy_url_num"
    category_privacy_url_jsonfile_path = r"pythonProject\AppInfo_google\privacy_url_category_num.json"


    driver_lock = threading.Lock()
    driver = GetCommon.setup_driver()

    # get_all_privacy_threaded()

    # pre_group_privacy_url()

    get_all_privacy_loop()
 
    # get_app_details()

    driver.quit()