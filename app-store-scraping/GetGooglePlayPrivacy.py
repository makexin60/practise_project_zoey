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

def get_privacy_without_lib(original_html_string,item,app_id,dir_path,all_app_ids):
    try:
        # privacy_data = GetCommon.get_privacy_original(html_string,True)
        privacy_data = GetCommon.get_privacy_original(original_html_string)

        if privacy_data != "":
            os.makedirs(dir_path, exist_ok=True) 
            with open(f"{dir_path}/{app_id}_policy.txt", "w", encoding="utf-8") as f:
                f.write(privacy_data)

            if len(all_app_ids) != 1:
                get_same_privacy_url_privacy(dir_path,app_id,all_app_ids)

            logger.error((json.dumps(item, ensure_ascii=False)))
            print("successful!")
            
        else:
            logger.error(f"privacy_data is null results:{(json.dumps(item, ensure_ascii=False))}")
            print("privacy_data is null")
            return
    except Exception as e:
        logger.error(f"enter wrong privacy_url: {(json.dumps(item, ensure_ascii=False))}")
        return
    
def have_sub_privacy_url_privacy(results, privacy_data,policy_url,app_id):
    try:
        visible_privacy_links = GetCommon.get_visible_privacy_links(driver)

        if len(visible_privacy_links) != 0:
            try:
                filtered_urls = GetCommon.filter_urls(visible_privacy_links, policy_url)

                if len(filtered_urls) != 0:
                    try:
                        privacy_data, results = GetCommon.wait_extra_privacy(results, privacy_data,filtered_urls, driver,logger)

                        with open(f"Policy_google/{app_id}_policy", "w", encoding="utf-8") as f:
                            f.write(privacy_data)
                        logger.error((json.dumps(results, ensure_ascii=False)))
                        print("successful!")

                    except TimeoutException:
                        print("TimeoutException")
                        logger.error(f"TimeoutException:{(json.dumps(results, ensure_ascii=False))}")
                        return
                    except Exception as e:
                        logger.error(
                            f"wait_extra_privacy: {(json.dumps(results, ensure_ascii=False))}----{e}")
                        return
                else:
                    logger.error((json.dumps(results, ensure_ascii=False)))
                    with open(f"Policy_google/{app_id}_policy", "w", encoding="utf-8") as f:
                        f.write(privacy_data)
                    print("successful!")
                    return

            except Exception as e:
                logger.error(
                    f"filter_urls: {(json.dumps(results, ensure_ascii=False))}----{e}")
                return

        else:
            logger.error((json.dumps(results, ensure_ascii=False)))
            with open(f"Policy_google/{app_id}_policy", "w", encoding="utf-8") as f:
                f.write(privacy_data)
            print("successful!")
            return

    except Exception as e:
        logger.error(f"visible_privacy_links: {(json.dumps(results, ensure_ascii=False))}----{e}")
        return

def get_privacy_old(results):
    policy_url = results["privacyPolicy"]
    if policy_url:
        try:
            driver.set_page_load_timeout(20)
            driver.get(policy_url)
            time.sleep(limit_time)

            privacy_data = GetCommon.get_privacy_original(driver.page_source)

            if privacy_data != "":
                have_sub_privacy_url_privacy(results, privacy_data,policy_url,app_id)
            else:
                logger.error(f"privacy_data is null results:{(json.dumps(results, ensure_ascii=False))}")
                print("privacy_data is null")
                return

        except Exception as e:
            logger.error(f"enter wrong privacy_url: {(json.dumps(results, ensure_ascii=False))}----{e}")
            return
    else:
        logger.error(f"get wrong privacy_url: {(json.dumps(results, ensure_ascii=False))}")
        return

def get_app_details():
    print(f"enter get_app_details")
    data = GetCommon.get_app_info(appInfo_google_path)
    for app_id in data:
        results = {}
        try:
            result = app(app_id, lang="en", country="us")  
            if result and isinstance(result, dict) and "title" in result:
                results = {
                    "title": result.get("title"),
                    "app_id": app_id,
                    "installs": result.get("installs"),
                    "score": result.get("score"),
                    "ratings": result.get("ratings"),
                    "reviews": result.get("reviews"),
                    "privacyPolicy": result.get("privacyPolicy"),
                    "developerEmail": result.get("developerEmail"),
                    "developerWebsite": result.get("developerWebsite"),
                    "app_url": f"https://play.google.com/store/apps/datasafety?id={app_id}&hl=en"
                }
                if results:
                    # get_privacy_old(results)
                    GetCommon.save_add_json_file(r"pythonProject\AppInfo_google\app_details_info.json",app_id)
                else:
                    GetCommon.save_add_json_file(r"pythonProject\AppInfo_google\get_app_details_error.json",app_id)
            else:
                GetCommon.save_add_json_file(r"pythonProject\AppInfo_google\get_app_details_error.json",app_id)
        except Exception as e:
            logger.error(f"get wrong results: {app_id}----{e}")
            return
    
def create_category_privacy_url_dir():
    have_privacy = GetCommon.get_app_info(have_privacy_app_info_path)
    grouped = {}
    for entry in have_privacy:
        try:
            url = entry['privacy_policy_url']
            if url not in grouped:
                grouped[url] = []
            grouped[url].append(entry)
        except Exception as e:
                print(e)
                logger.error(f"fail entry: {entry}")

    os.makedirs(category_privacy_url_dir_path, exist_ok=True)

    for url, entries in grouped.items():
        try:
            hash_name = hashlib.sha1(url.encode('utf-8')).hexdigest()
            file_path = os.path.join(category_privacy_url_dir_path, f"{hash_name}.json")
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(entries, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(e)
            logger.error(f"fail url: {url}")

    print(f"Done! {len(grouped)} files saved to '{category_privacy_url_dir_path}/'")

def create_category_privacy_url_jsonfile():
    merged_data = {}

    for filename in os.listdir(category_privacy_url_dir_path):
        if filename.endswith(".json"):
            file_path = os.path.join(category_privacy_url_dir_path, filename)
            key = filename[:-5] 
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    merged_data[key] = data
            except Exception as e:
                logger.error(f"fail：{filename}, error: {e}")

    with open(category_privacy_url_jsonfile_path, "w", encoding="utf-8") as f:
        json.dump(merged_data, f, indent=4, ensure_ascii=False)

    print(f"num {len(merged_data)} file path: {category_privacy_url_jsonfile_path}")

def pre_group_privacy_url():
    create_category_privacy_url_dir()
    create_category_privacy_url_jsonfile()

def get_all_privacy(app_list,key):
    print(f"Processing file: {key}")
    try:
        all_app_ids = []
        item = app_list[0] 
        for app_info in app_list:
            app_id = app_info.get('app_id')
            all_app_ids.append(app_id)

        get_privacy(item,all_app_ids)
        
    except Exception as e:
        print(e)
        logger.error(f"parse fail: {app_list}")

def get_privacy_main(privacy_url_dict_path):
    with open(privacy_url_dict_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    try:
        for key, app_list in data.items():
            print(f"Processing file: {key}")
            all_app_ids = []
            item = app_list[0] 
            for app_info in app_list:
                app_id = app_info.get('app_id')
                all_app_ids.append(app_id)

            get_privacy(item,all_app_ids)
            
    except Exception as e:
        print(e)
        logger.error(f"parse fail: {app_list}")

def move_policy_dir_to_single_policy(source_root,target_folder):

    os.makedirs(target_folder, exist_ok=True)
    for subfolder in os.listdir(source_root):
        subfolder_path = os.path.join(source_root, subfolder)
        
        if os.path.isdir(subfolder_path):
            for filename in os.listdir(subfolder_path):
                source_file = os.path.join(subfolder_path, filename)
                if os.path.isfile(source_file):
                    target_file = os.path.join(target_folder, filename)

                    if os.path.exists(target_file):
                        base, ext = os.path.splitext(filename)
                        target_file = os.path.join(target_folder, f"{subfolder}_{base}{ext}")

                    shutil.copy2(source_file, target_file)

    print("done move_policy_dir_to_single_policy")

def handel_url_200_error_path(category_privacy_url_jsonfile_path,have_privacy_url_200_path,have_privacy_url_200_dict_path):
    # create_dict(category_privacy_url_jsonfile_path,have_privacy_url_200_path,have_privacy_url_200_dict_path,True)
    get_privacy_main(have_privacy_url_200_dict_path)

def get_privacy_loop():
    source_root = r"C:\Users\smile\PycharmProjects\pythonProject\Policy_google"
    input_folder = r"C:\Users\smile\PycharmProjects\pythonProject\Policy_google2"
    empty_path = r"pythonProject\AppInfo_google\privacy_content_empty.json"
    less3lines_path = r"pythonProject\AppInfo_google\privacy_less3_lines.json"
    less5lines_errorcode_path = r"pythonProject\AppInfo_google\privacy_less5_lines_error_code.json"
    less3lines_dict_path = r"pythonProject\AppInfo_google\privacy_less3_lines_dict.json"
    have_privacy_url_200_path = r"pythonProject\AppInfo_google\have_privacy_url_200.json"
    have_privacy_url_200_dict_path = r"pythonProject\AppInfo_google\have_privacy_url_200_dict.json"

    # move_policy_dir_to_single_policy(source_root,input_folder)
    # handel_url_200_error_path(category_privacy_url_jsonfile_path,have_privacy_url_200_path,have_privacy_url_200_dict_path)

    vaild_file(category_privacy_url_jsonfile_path,source_root)
    # check_file_content_lessline_errocode(input_folder,empty_path,less3lines_path,less5lines_errorcode_path)
    # handel_less5_lines_error_code(category_privacy_url_jsonfile_path,less5lines_errorcode_path)
    # handel_less3lines_path(category_privacy_url_jsonfile_path,less3lines_path,less3lines_dict_path)
 
def get_all_privacy_loop():
    # privacy_url_dict_path = r'pythonProject\AppInfo_google\privacy_url_category_num.json'
    # privacy_url_dict_path = r'pythonProject\AppInfo_google\test.json'
    # get_privacy_main(privacy_url_dict_path)
    get_privacy_loop()
    # combain_info()

def handel_less5_lines_error_code(category_privacy_url_jsonfile_path,less5lines_errorcode_path):
    with open(category_privacy_url_jsonfile_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    with open(less5lines_errorcode_path, 'r', encoding='utf-8') as f:
        valid_folder_names = set(json.load(f))  

    for key, app_list in data.items():
        if key in valid_folder_names:
            get_all_privacy(app_list,key)

def create_dict(category_privacy_url_jsonfile_path,less3lines_path,less3lines_dict_path,if_json_flag):
    with open(less3lines_path, "r", encoding="utf-8") as f:
        if if_json_flag:
            a_data = json.load(f)
            app_ids = {entry["app_id"] for entry in a_data}
        else:
            app_ids = set(json.load(f))

    with open(category_privacy_url_jsonfile_path, "r", encoding="utf-8") as f:
        b_data = json.load(f)

    filtered_data = {}

    for key, app_list in b_data.items():
        if any(entry["app_id"] in app_ids for entry in app_list):
            filtered_data[key] = app_list 

    with open(less3lines_dict_path, "w", encoding="utf-8") as f:
        json.dump(filtered_data, f, indent=4, ensure_ascii=False)

    print(f"input {len(filtered_data)} group {less3lines_dict_path}")

def handel_less3lines_path(category_privacy_url_jsonfile_path,less3lines_path,less3lines_dict_path):
    create_dict(category_privacy_url_jsonfile_path,less3lines_path,less3lines_dict_path,False)
    # get_privacy_main(less3lines_dict_path)

def combain_info():

    json_folder = r"C:\Users\smile\PycharmProjects\pythonProject\privacy_url_num"
    output_path = r"pythonProject\AppInfo_google\have_privacy_app_info.json"

    merged_data = []

    for filename in os.listdir(json_folder):
        if filename.endswith(".json"):
            file_path = os.path.join(json_folder, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        merged_data.extend(data)
                    else:
                        merged_data.append(data)
            except Exception as e:
                logger.error(f"fail：{filename}, error: {e}")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(merged_data, f, indent=4, ensure_ascii=False)

    print(f"num {len(merged_data)} file path: {output_path}")

def check_file_content_lessline_errocode(input_folder,empty_path,less3lines_path,less5lines_errorcode_path):
    error_keywords = [
        "400", "401", "403", "404", "408",
        "500", "501", "502", "503", "504",
        "301", "302", "307"
    ]

    today = datetime.date.today()

    for filename in os.listdir(input_folder):
       
        try:
            filepath = os.path.join(input_folder, filename)
            if os.path.isfile(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.strip().splitlines()

                if not content:
                    GetCommon.save_add_json_file(empty_path,filename)
                elif len(lines) <= 2 and os.path.getsize(filepath) < 100:
                    GetCommon.save_add_json_file(less3lines_path,filename)
                elif len(lines) <= 4 and any(err in content for err in error_keywords) and os.path.getsize(filepath) < 1025:
                    GetCommon.save_add_json_file(less5lines_errorcode_path,filename)

        except Exception as e:
            print(f"Error processing file {filename}: {e}")
            logger.error(f"Error processing file {filename}") 

# This function checks if the number of files in each subfolder matches the number of entries in the corresponding JSON file.
def vaild_file(json_path, target_root_folder):
    with open(json_path, "r", encoding="utf-8") as f:
        json_data_all = json.load(f)

    json_file_names = set(json_data_all.keys())
    folder_names = {f for f in os.listdir(target_root_folder) if os.path.isdir(os.path.join(target_root_folder, f))}

    json_only = json_file_names - folder_names
    folder_only = folder_names - json_file_names

    if json_only:
        logger.error("Folders missing for the following JSON entries:")
        for name in sorted(json_only):
            print(f"  - {name}/ (folder missing)")

    if folder_only:
        logger.error("JSON entries missing for the following folders:")
        for name in sorted(folder_only):
            print(f"  - {name} (not in JSON)")

    file_count_total = 0

    for subfolder in folder_names:
        subfolder_path = os.path.join(target_root_folder, subfolder)

        json_entries = json_data_all.get(subfolder)
        if not json_entries:
            logger.error(f"No JSON entry found for folder: {subfolder}")
            continue

        json_length = len(json_entries)

        file_count = len([
            f for f in os.listdir(subfolder_path)
            if os.path.isfile(os.path.join(subfolder_path, f))
        ])

        file_count_total += file_count

        if file_count != json_length:
            logger.error(f"Mismatch in {subfolder}: file count = {file_count}, JSON entries = {json_length}")

    print(f"Total files checked: {file_count_total}")

def get_privacy_url(app_id):
    print(f"enter get_data_safety {app_id}")

    url = f"https://play.google.com/store/apps/datasafety?id={app_id}&hl=en"
    driver.get(url)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    a_tags = driver.find_elements(
        By.XPATH,
        '//a[contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "privacy policy") '
        'and not(contains(@href, "policies.google.com/privacy"))]'
    )
    print(f"find a_tags:{len(a_tags)}")
    if a_tags:
        json_data = {
            "app_id": app_id,
            "privacy_policy_url": a_tags[0].get_attribute("href")
        }
        GetCommon.save_add_json_file(have_privacy_app_info_path, json_data)
    else:
        GetCommon.save_add_json_file(not_have_privacy_url_path, app_id)

    print("successful!")

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