import json
import logging
import os
import re
import time
from collections import OrderedDict
from urllib.parse import urlparse, urlunparse
from pathlib import Path
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

limit_time = 0.8

def find_repeated_section(text):
    n = len(text)
    for i in range(1, n // 2 + 1):
        candidate = text[:i]
        if text.startswith(candidate * 2):
            return candidate
    return None

def read_file_name(input_path, output_path):
    for filename in os.listdir(input_path):
        save_add_json_file(output_path,filename)

def getLogger(address):
    # Create a logger
    logger = logging.getLogger("my_logger")
    # Allow all levels of logs to enter the processor
    logger.setLevel(logging.DEBUG)  

    # Define the log format (including milliseconds)
    log_format = logging.Formatter(
        "%(asctime)s,%(msecs)03d - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Create an ERROR level log file handler
    error_handler = logging.FileHandler(f"pythonProject/Logger/{address}_error.log",encoding="utf-8")
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(log_format)

    # Create an WARNING level log file handler
    # warning_handler = logging.FileHandler(f"Logger/{address}_warning.log",encoding="utf-8")
    # warning_handler.setLevel(logging.WARNING)
    # warning_handler.setFormatter(log_format)

    # Add a filter to ensure that warning_handler only processes WARNING level logs
    # warning_handler.addFilter(lambda record: record.levelno == logging.WARNING)

    error_handler.addFilter(lambda record: record.levelno >= logging.ERROR)

    logger.addHandler(error_handler)
    # logger.addHandler(warning_handler)

    return logger

def get_app_info(target_path):
    with open(target_path, "r", encoding="utf-8") as file:
        content = json.load(file, object_pairs_hook=lambda pairs: OrderedDict(pairs))
    print(f"open {target_path} file length: {len(content)}")
    return content

def save_new_txt_file(target_path,data):
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(data)

def save_new_json_file(target_path, data):
    with open(target_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def save_add_json_file(target_path, data):
    with open(target_path, "a+", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=4) + ",\n")


def scroll_to_load_apps(driver, max_scrolls=10):
    print("Start scrolling to load more apps...")

    last_height = driver.execute_script("return document.body.scrollHeight")
    scroll_attempt = 0

    while scroll_attempt < max_scrolls:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        try:
            WebDriverWait(driver, 2).until(
                lambda d: driver.execute_script("return document.body.scrollHeight") > last_height
            )
        except Exception:
            print("No new content detected, all apps may have been loaded")

        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:  
            print("Scrolling is complete and all apps are loaded")
            break

        last_height = new_height
        scroll_attempt += 1

    print("Scrolling is complete")

# Extract app IDs from the current page
def extract_app_ids(driver):
    app_ids = set()
    app_links = driver.find_elements(By.XPATH, "//a[contains(@href, '/store/apps/details?id=')]")
    for link in app_links:
        match = re.search(r"id=([^&]+)", link.get_attribute("href"))
        if match:
            app_ids.add(match.group(1))
    return app_ids

# Scrape app IDs from a category page without clicking "Show more"
def scrape_category_no_click(url,driver):
    print(f"enter scrape_category_no_click")
    driver.set_page_load_timeout(15)
    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
    except Exception:
        print("The main element of the page was not found")
        return None

    scroll_to_load_apps(driver)  
    app_ids = extract_app_ids(driver)

    print(f"leave {url} get {len(app_ids)} applications")
    return app_ids

# Scrape app IDs from a category page without clicking "Show more" and without URL
# This function is used when the URL is not provided, and we just want to scroll and extract app IDs
def scrape_category_no_click_no_url(driver):
    time.sleep(limit_time)
    scroll_to_load_apps(driver)  
    app_ids = extract_app_ids(driver)

    print(f"leave scrape_category_no_click_no_url get {len(app_ids)} applications")
    return app_ids

# Scroll to the bottom of the page and click the "Show more" button until it no longer appears
def scroll_and_click_show_more(driver):
    print("enter scroll_and_click_show_more")
    while True:
        scroll_to_load_apps(driver)
        time.sleep(limit_time)
        try:
            show_more_button = driver.find_element(By.XPATH, "//span[contains(text(), 'Show More')]")
            ActionChains(driver).move_to_element(show_more_button).click().perform()
            print("click 'Show more' button")
            time.sleep(limit_time) 

            # After clicking the button, scroll to the bottom again to ensure new content is loaded
            scroll_to_load_apps(driver)

        except Exception as e:
            print(f"leave scroll_and_click_show_more not find 'Show more' button{e}")
            break

        # Check if the page continues to grow
        last_height = driver.execute_script("return document.documentElement.scrollHeight")
        time.sleep(limit_time)
        new_height = driver.execute_script("return document.documentElement.scrollHeight")

        if new_height == last_height:
            print("leave scroll_and_click_show_more")
            break

#scroll page and click button
def scrape_category_click(url,driver):
    driver.get(url)
    time.sleep(limit_time)

    scroll_and_click_show_more(driver)
    app_ids = extract_app_ids(driver)

    print(f"leave scrape_category_click {url} get {len(app_ids)} applications")
    return app_ids

#remove_duplicates_json in two files
def remove_duplicates_json(file1,target_file,output_file):
    try:
        with open(file1, "r", encoding="utf-8") as f1:
            data1 = set(json.load(f1))  
        with open(target_file, "r", encoding="utf-8") as f2:
            data2 = set(json.load(f2))
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}")
        return
    except FileNotFoundError as e:
        print(f"file not find: {e}")
        return

    # Calculate the difference between the two sets
    new_app_ids = list(data2 - data1)

    # Save the new app IDs to the output file
    if not new_app_ids:
        print("No new app IDs found, nothing to save.")
        return
    save_new_json_file(output_file,new_app_ids)

    print(f"success，data1:{len(data1)}, data2:{len(data2)}, new_app_ids:{len(new_app_ids)}, resule file path{output_file}")

# Install ChromeDriver using webdriver_manager
CHROMEDRIVER_PATH = ChromeDriverManager().install()

def setup_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--lang=en-US")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    )
    prefs = {"profile.managed_default_content_settings.images": 2,
             "profile.managed_default_content_settings.javascript": 1}
    options.add_experimental_option("prefs", prefs)
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)

    return driver

def wait_span_highlights(click_path,driver):
    print("enter wait_span_highlights")

    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, click_path))
        )

        if element:
            print("Found 'Highlights', performing actions...")

            # Find all <span> tags with the text "Highlights"
            highlights_spans = driver.find_elements(By.XPATH, click_path)

            # click each <span> element
            for span in highlights_spans:
                driver.execute_script("arguments[0].scrollIntoView();", span)  # 滚动到元素
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable(span)).click()

    except TimeoutException:
        print("TimeoutException wait_span_highlights:")

    except Exception as e:
        print("Error wait_span_highlights:", e)

    print("leave wait_span_highlights")

def get_privacy_original(page_source):
    print(f"enter get_privacy_original")

    soup = BeautifulSoup(page_source, "html.parser")
    # Defining possible content areas
    possible_selectors = [
        "main#brx-content",  # Justalk
        "div[class*='xg6iff7']",  # Facebook 
        "article",
        "main",
        "body"  # Bottom-line strategy
    ]
    for selector in possible_selectors:
        content = soup.select_one(selector)
        if content:
            for tag in content.find_all(["header", "footer"]):
                tag.decompose()

            for tag in content.find_all(class_=lambda c: c and ("header" in c.lower() or "footer" in c.lower())):
                tag.decompose()

            time.sleep(limit_time)
            privacy_text = content.get_text(separator="\n", strip=True)
            print(f"okay get_privacy_original")
            return privacy_text

    print(f"cant find content get_privacy_original")
    return ""

def get_visible_privacy_links(driver):
    script = """
    return Array.from(document.querySelectorAll('a')).filter(a => {
        let rect = a.getBoundingClientRect();
        if (!a.textContent.toLowerCase().includes('privacy')) return false;
        if (document.head.contains(a)) return false;  

        let elem = a;
        while (elem) {
            let style = window.getComputedStyle(elem);
            if (style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0') {
                return false;   
            }
            if (elem.tagName.toLowerCase() === 'footer' || elem.tagName.toLowerCase() === 'header') {
                return false;   
            }
            elem = elem.parentElement;
        }

        return true;  # Eligible
    }).map(a => a.href);
    """
    return driver.execute_script(script)

# Filter URLs to remove duplicates and normalize them
def filter_urls(urls,original_url):
    print(f"enter filter_urls original_urls:{urls}")

    ## Record the paths that have appeared (ignore language/region code, fragment and trailing `/`)
    seen_paths = set()  
    # Record the complete URL that has appeared
    seen_urls = set() 

    normalized_url = normalize_url(original_url)
    seen_paths.add(normalized_url)

    filtered_urls = []

    for url in urls:
        # remove `mailto:` URL
        if url.startswith("mailto:"):
            continue

        if not (url.startswith("http://") or url.startswith("https://")):
            continue  

        normalized_url = normalize_url(url)

        if normalized_url in seen_paths:
            continue  

        seen_paths.add(normalized_url)  

        if url in seen_urls:
            continue  

        seen_urls.add(url) 

        filtered_urls.append(url)

    print(f"leave filter_urls: {filtered_urls}")
    return filtered_urls

# Normalize URL by removing fragment, trailing `/`, and converting to lowercase
def normalize_url(url):
    parsed = urlparse(url)
    parsed = parsed._replace(fragment="")
    path = parsed.path.rstrip("/")
    netloc = parsed.netloc.lower().replace("www.", "")
    scheme = "https"  
    normalized = urlunparse((scheme, netloc, path, "", "", ""))

    return normalized

def read_id_by_json(original_path,target_path,logger):
    with open(original_path, "r", encoding="utf-8") as f:
        try:
            json_data = json.load(f)
            if isinstance(json_data, list):
                for item in json_data:
                    if isinstance(item, dict) and "app_id" in item:
                        app_id = item["app_id"]
                        save_add_json_file(target_path, app_id)
                    else:
                        logger.error(f"Item is not a dictionary or does not contain 'id': {item}")
                        print("cant find App ID in item")
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            return
    print(f"save file path: {target_path}")

def read_id(original_path,target_path,express):
    with open(original_path, "r", encoding="utf-8") as file:
        for line in file:
            json_str = line.strip()
            match = re.search(express, json_str)
            if match:
                app_id = match.group(1)
                save_add_json_file(target_path, app_id)
                print(f"extract App ID: {app_id}")
            else:
                print("cant find App ID")

    print(f"save file path: {target_path}")

# Delete files in the directory that match the IDs in the ID file
def delete_matching_files(directory, id_file):
    with open(id_file, "r", encoding="utf-8") as f:
        id_list = json.load(f) 

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        file_name_without_ext, _ = os.path.splitext(filename)
        new_name = file_name_without_ext.rsplit("_", 1)[0]  

        # If the file name is in the ID list, delete it
        if new_name in id_list:
            try:
                os.remove(file_path)
                print(f"remove success: {file_path}")
            except Exception as e:
                print(f"remove fail: {file_path}, error: {e}")

def wait_extra_privacy_only_sub(results,filtered_urls,driver,logger):
    print(f"enter wait_extra_privacy")

    sub_privacy_data = "Sub-section Policy: "
    results.update({
        "sub-section_urls": filtered_urls
    })

    for index, href in enumerate(filtered_urls):
        try:
            driver.set_page_load_timeout(10)  
            driver.get(href)
            driver.execute_script("window.stop();")  # Stop unnecessary loading

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            new_page_content = driver.page_source

            soup = BeautifulSoup(new_page_content, "html.parser")

            body_content = soup.find(id="ph-body")

            if not body_content:
                body_content = soup.select_one("body")

            if body_content:
                for tag in body_content.find_all(["header", "footer"]):  
                    tag.decompose()

                for tag in body_content.find_all(
                        class_=lambda c: c and ("header" in c.lower() or "footer" in c.lower())):
                    tag.decompose()  

                time.sleep(limit_time)
                sub_data = body_content.get_text(separator="\n", strip=True)
                sub_privacy_data += "\n" + "Sub-policy " + str(index) + "-" + href + ":\n" + sub_data 

        except TimeoutException:
            sub_privacy_data += "\n" + "Sub-policy " + str(index) + "-" + href + ":\n"
            logger.error(f"wait_extra_privacy TimeoutException: {(json.dumps(results, ensure_ascii=False))}")
            continue

        except Exception:
            sub_privacy_data += "\n" + "Sub-policy " + str(index) + "-" + href + ":\n"
            logger.error(f"Error more links:{href}---{(json.dumps(results, ensure_ascii=False))}")
            continue

    print("leave wait_extra_privacy")
    return sub_privacy_data,results

def wait_extra_privacy(results, privacy_data,filtered_urls,driver,logger):
    print(f"enter wait_extra_privacy")

    privacy_data += privacy_data + "\n" + "Sub-section Policy: "
    results.update({
        "sub-section_urls": filtered_urls
    })

    for index, href in enumerate(filtered_urls):
        try:
            driver.set_page_load_timeout(10)  
            driver.get(href)

            # wait for the new page load finish
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            # get new page content
            driver.execute_script("window.stop();")  # Stop unnecessary loading
            new_page_content = driver.page_source

            soup = BeautifulSoup(new_page_content, "html.parser")

            # get DID id="ph-body" 
            body_content = soup.find(id="ph-body")

            # If not found, fallback to body
            if not body_content:
                body_content = soup.select_one("body")

            if body_content:
                # Remove elements whose class contains 'header' or 'footer'
                for tag in body_content.find_all(["header", "footer"]):  # Remove tags whose class contains 'header' or 'footer'
                    tag.decompose()

                for tag in body_content.find_all(
                        class_=lambda c: c and ("header" in c.lower() or "footer" in c.lower())):
                    tag.decompose()  # Remove elements whose class contains 'header' or 'footer'

                time.sleep(limit_time)
                privacy_text = body_content.get_text(separator="\n", strip=True)
                privacy_data += "\n" + "Sub-policy " + str(index) + "\n" + href + ":\n" + privacy_text  # 每次拼接后加真实换行符

        except TimeoutException:
            privacy_data += "\n" + "Sub-policy " + str(index) + "\n" + href + ":\n"
            logger.error(f"wait_extra_privacy TimeoutException: {(json.dumps(results, ensure_ascii=False))}")
            continue

        except Exception:
            privacy_data += "\n" + "Sub-policy " + str(index) + "\n" + href + ":\n"
            logger.error(f"Error more links:{href}---{(json.dumps(results, ensure_ascii=False))}")
            continue


    print("leave wait_extra_privacy")
    return privacy_data,results

# calculate content file2 have but file1 not have
def filter_content(file1,file2,output_file,flag_id):


    if flag_id:
        with open(file2, "r", encoding="utf-8") as file_A_bac:
            apps = set(json.load(file_A_bac))
        with open(file1, "r", encoding="utf-8") as file_A:
            original = set(json.load(file_A))  # Convert to set for easy deduplication and comparison
        diff = list(apps - original)
    else:
        with open(file2, "r", encoding="utf-8") as file_A_bac:
            apps = json.load(file_A_bac)
        with open(file1, "r", encoding="utf-8") as file_A:
            original = json.load(file_A)
        diff = [app for app in apps if app["app_id"] not in original]

    with open(output_file, "w", encoding="utf-8") as output:
        json.dump(diff, output, ensure_ascii=False, indent=4)

    print("Processing complete, generated file:", output_file,len(diff))


def convert_upper(path,output_path):
    data = get_app_info(path)
    data = [str(item).upper() for item in data]
    save_new_json_file(output_path,data)

def get_file_name(directory,target_path,size,flag,non_200_app_id_path):
    files = [
        f for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f)) and os.path.getsize(os.path.join(directory, f)) < size
    ]
    print(f"Number of files in '{directory}': {len(files)}")

    if flag == "size":
        # extract the content before the last `_`
        for file in files:
            file_prefix = file.rsplit("_", 1)[0]
            save_add_json_file(target_path, file_prefix)
    else:
        error_codes = {"301", "302", "303", "307", "400", "403", "404", "408",  "410", "429", "500", "502", "503", "504"}

        for file in files:
            file_path = os.path.join(directory, file)
            file_prefix = file.rsplit("_", 1)[0]

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                if len(lines) < 4:
                    print(lines)
                    file_content = " ".join(lines)
                    if any(code in file_content for code in error_codes):
                        save_add_json_file(non_200_app_id_path, file_prefix)
                    else:
                        save_add_json_file(target_path, file_prefix)
            except Exception as e:
                print(f"handel {file_path} fail: {e}")

def filter_data(file_a, file_b, output_file):
    with open(file_a, "r", encoding="utf-8") as f:
        id_list = json.load(f)  

    with open(file_b, "r", encoding="utf-8") as f:
        data_list = json.load(f)  

    # Filter data in file B based on IDs from file A
    filtered_data = [item for item in data_list if str(item["id"]) in id_list]

    # Write the matched results to a new file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(filtered_data, f, indent=4, ensure_ascii=False)

    print(f"result path: {output_file}")


def get_header():
    authorization = "Bearer eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlU4UlRZVjVaRFMifQ.eyJpc3MiOiI3TktaMlZQNDhaIiwiaWF0IjoxNzM5MTkyNzIzLCJleHAiOjE3NDY0NTAzMjMsInJvb3RfaHR0cHNfb3JpZ2luIjpbImFwcGxlLmNvbSJdfQ.wuLUSBq_qWD4MAkmwbxoaJDQTRyUBZzEqDMuvT-nAJNarxda8F5TLXpRy_OjonWBuUcnD-eyWb86qn4w6xfang"

    # Headers (Apple may require authorization tokens, these are standard ones)
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "*/*",
        "Origin": "https://apps.apple.com",
        "Referer": "https://apps.apple.com/",
        "Authorization": authorization
    }

    return headers

def get_subfolders(folder_path):
    return [f.name for f in Path(folder_path).iterdir() if f.is_dir()]