import threading
import time

import google_play_scraper
from bs4 import BeautifulSoup
from selenium.common import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import GetCommon

enCountries =["US","GB","CA","AU","NZ","IE","IN","SG","ZA","PH","NG","KE","GH","PK","MY","HK","AE","BD","LK","UG","TZ","ZM","ZW","BW","NA","MT","JM","TT","BS","AG","BB","BZ","GD","GY","KN","LC","VC","SL","LR","FJ","PG","SB","TO","WS","VU","MW","RW","LS","SZ","GM","CM"]

# get app IDs from categories using selenium
def get_app_id_method1():
    print("enter get_app_id_method1")
    for country in enCountries:
        tem_app_ids = set()
        for category in categories_new:
            url= f"https://play.google.com/store/apps/category/{category}?hl=en&gl={country}"
            try:
                app_ids = GetCommon.scrape_category_click(url,driver)
                tem_app_ids.update(app_ids)  

            except Exception as e:
                print("Error", e)
                logger.error(url)
                continue
    print(f"Num tem1_app_ids: {len(tem_app_ids)}")
    GetCommon.save_add_json_file(appinfo_original_path, list(tem_app_ids))

#get app IDs from search results using google_play_scraper
def get_app_id_method2():
    print("enter get_app_id_method2")

    seen_app_ids = set()
    all_results = []

    for country in enCountries:
        for keyword in categories_new:
            try:
                # get the search results for the keyword in the specified country
                result = google_play_scraper.search(
                    query=keyword,
                    lang="en",
                    country=country,
                    n_hits=250
                )
                print(f"length:{len(result)}")

                # fiter out the results to only include unique app IDs
                for app in result:
                    app_id = app["appId"]
                    if app_id not in seen_app_ids:
                        seen_app_ids.add(app_id)
                        all_results.append(app["appId"])

                time.sleep(2)  

            except Exception as e:
                print("Error", e)
                logger.error(keyword)
                continue

    print(f"Num tem2_app_ids: {len(all_results)}")
    GetCommon.save_add_json_file(appinfo_original_path, list(all_results))

#get app IDs from search results 
def get_app_id_method3():
    print("enter get_app_id_method3")

    # store unique app IDs
    tem_app_ids = set()
    for country in enCountries:
        tem_app_ids = set()
        for category in categories_new:
            url= f"https://play.google.com/store/search?q={category}&c=apps&hl=en&gl={country}"
            try:
                app_ids = GetCommon.scrape_category_no_click(url,driver)
                if app_ids:
                    tem_app_ids.update(app_ids)  
            except Exception as e:
                print("Error", e)
                logger.error(url)
                continue

    print(f"Num tem3_app_ids: {len(tem_app_ids)}")
    GetCommon.save_add_json_file(appinfo_original_path, list(tem_app_ids))

# get app IDs from "See more information" links
def get_app_id_method4():
    print("enter get_app_id_method4")

    # the buttons that might have more apps
    a_array= ["See more information on About this app","See more information on Data safety","See more information on Ratings and reviews"]
    for country in enCountries:
        for app_info in appinfo_all:
            url= f"https://play.google.com/store/apps/details?id={app_info}&hl=en&gl={country}"
            try:
                print(f"enter url:{url}")
                driver.get(url)

                see_more_links = WebDriverWait(driver, 15).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//a[starts-with(@aria-label, "See more information on ")]'))
                )

                hrefs = []
                if len(see_more_links)!= 0:
                    for see_more_link in see_more_links:
                        aria_label = see_more_link.get_attribute("aria-label")
                        if aria_label not in a_array:
                            print(f"enter aria_label: {aria_label}")
                            href = see_more_link.get_attribute("href")
                            hrefs.append(href)
                else:
                    print(f"can not find 'See more information' ，jump {url}")
                    continue

                if len(hrefs) != 0:
                    for href in hrefs:
                        try:
                            app_ids = GetCommon.scrape_category_no_click(href, driver)
                            print(f"app_ids:{app_ids} num:{len(app_ids)}")
                            if app_ids:
                                GetCommon.save_add_json_file(appinfo_original_path, list(app_ids))

                        except TimeoutException:
                            print(f"access {href} over time, skip!")
                            logger.error(href)

            except TimeoutException:
                print(f"access {url} over time, skip!")
                logger.error(url)
                continue

            except Exception as e:
                print("Error", e)
                logger.error(url)
                continue

# get all categories from Google Play Store
def get_categories_method1(target_path):

    #get all app paths from the file
    for url in all_app_paths:
        driver.get(url)

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        # click the "Show more" button to load more categories
        GetCommon.scroll_and_click_show_more(driver)

        new_page_content = driver.page_source
        soup = BeautifulSoup(new_page_content, "html.parser")

        # find all div tags with class "kcen6d"
        divs = soup.find_all("div", class_="kcen6d")

        print(f"Found {len(divs)} elements with class 'kcen6d' on {url}")

        # get the text content of each div and save it
        for div in divs:
            category = div.get_text(strip=True)
            GetCommon.save_add_json_file(target_path,category)

def get_categories_method2(target_path):
    driver.get("https://support.google.com/googleplay/android-developer/answer/9859673?hl=en")
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    GetCommon.wait_span_highlights("//div[@class='zippy-overflow']",driver)
    new_page_content = driver.page_source
    soup = BeautifulSoup(new_page_content, "html.parser")
    divs = soup.find_all("table", class_="nice-table")
    for div in divs:
        category = div.get_text(strip=True)
        GetCommon.save_add_json_file(target_path, category)

def get_categories_method3(target_path):
    print("enter get_categories_method3")

    for country in enCountries:
        for category in categories_new:
            url = f"https://play.google.com/store/search?q={category}&c=apps&hl=en&gl={country}"
            try:
                driver.get(url)

                input_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "HWAcU"))
                )

                # move to the input element and click it
                actions = ActionChains(driver)
                actions.move_to_element(input_element).click().perform()
                time.sleep(1)

                new_page_content = driver.page_source
                soup = BeautifulSoup(new_page_content, "html.parser")

                lis = soup.find_all("li", class_="YVhSle")

                print(f"Found {len(lis)} elements on {url}")

                if len(lis) != 0:
                    for li in lis:
                        category = li.get("data-display-text")
                        # check if the category is not None or empty
                        if category:  
                            GetCommon.save_add_json_file(target_path, category)

            except Exception as e:
                print("Error", e)
                logger.error(url)
                continue

# filter out categories that already exist in the previous categories
def filter_category(keywords1,keywords2):
    keywords1 = {word.upper() for word in keywords1}
    keywords2 = {word.upper() for word in keywords2}

    filtered_keywords = keywords2 - keywords1

    # split categories that contain "_AND_" or "&" into separate categories
    final_categories = set(filtered_keywords)  
    for word in filtered_keywords:
        if "_AND_" in word:
            final_categories.update(word.split("_AND_"))
        if "&" in word:
            final_categories.update(word.split("&"))

    unique_keywords = list(set(final_categories))
    GetCommon.save_new_json_file(categories_new_path,unique_keywords)
    print(f"leave filter_category {len(unique_keywords)}")

def get_new_categories():
    target_path = r"AppInfo_google\categories_new.json"
    get_categories_method1(target_path)
    get_categories_method2(target_path)
    get_categories_method3(target_path)

    file1 = GetCommon.get_app_info(r"AppInfo_google\categories_com.json")
    file2 = GetCommon.get_app_info(r"AppInfo_google\categories.json")
    filter_category(file1, file2) 

    categories_new_data_tem = GetCommon.get_app_info(categories_new_path)
    categories_new_data = list(set(categories_new_data_tem))
    if len(categories_new_data_tem) != len(categories_new_data):
        print(f"still have duplicate: {categories_new_data_tem}--{categories_new_data}")
        GetCommon.save_new_json_file(categories_new_path,categories_new_data)

def get_new_app_ids():
    get_app_id_method1()
    get_app_id_method2()
    get_app_id_method3()
    get_app_id_method4()

if __name__ == "__main__":
    print("enter main")

    MAX_CONCURRENT_THREADS = 20  # Limit concurrent threads
    BATCH_SIZE = 200  # Control how many items to load into memory at a time
    # Global driver instance (must be accessed in a thread-safe way)
    driver_lock = threading.Lock()
    driver = GetCommon.setup_driver()  # Or any other browser
    logger = GetCommon.getLogger("GooglePlayInfo")
    categories_new_path = r"pythonProject\AppInfo_google\categories.json"
    appinfo_new_path = r"pythonProject\AppInfo_google\appInfo_google_new.json"
    appinfo_original_path = r"pythonProject\AppInfo_google\appInfo_google_original.json"
    appinfo_all_path = r"pythonProject\AppInfo_google\appInfo_google.json"
    all_app_path = r"pythonProject\AppInfo_google\all_app_entrance_paths.json"

    categories_new = GetCommon.get_app_info(categories_new_path)
    all_app_paths = GetCommon.get_app_info(all_app_path)
    appinfo_all = GetCommon.get_app_info(appinfo_all_path)

    # get_new_categories()
    get_new_app_ids()

    # filter app_id
    # GetCommon.remove_duplicates_json(appinfo_all_path, appinfo_original_path, appinfo_new_path)

    driver.quit()

    print("leave main")
