import itertools
import threading
from concurrent.futures import ThreadPoolExecutor
import urllib3
from selenium.common import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import GetCommon
import time

def get_structure_data(url):
    result = []

    try:
        parent_divs = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "Mf2Txd"))
        )

        if parent_divs:
            for parent in parent_divs:
                try:
                    h2_element = parent.find_element(By.TAG_NAME, "h2").text if parent.find_elements(By.TAG_NAME,
                                                                                              "h2") else None

                    ivTO9c_div = parent.find_element(By.CLASS_NAME, "ivTO9c").text if parent.find_elements(By.CLASS_NAME,
                                                                                                           "ivTO9c") else None
                    title = h2_element if h2_element else ""
                    if ivTO9c_div:
                        title += f" ( {ivTO9c_div} )"

                    # handle the case where h2_element is None
                    if h2_element == "Security practices":
                        security_practices = []

                        h3_elements = parent.find_elements(By.TAG_NAME, "h3")
                        h3_texts = [h3.text for h3 in h3_elements]

                        fozKzd_elements = parent.find_elements(By.CLASS_NAME, "fozKzd")
                        fozKzd_texts = [fz.text for fz in fozKzd_elements]

                        if len(h3_texts) == len(fozKzd_texts):
                            security_practices = [{key: value} for key, value in zip(h3_texts, fozKzd_texts)]

                        result.append({
                            "Security practices": security_practices
                        })
                        continue  

                    else:
                        ojPjfd_divs = parent.find_elements(By.XPATH, ".//div[@jscontroller='ojPjfd']")

                        details = []
                        # `jscontroller="ojPjfd"` as the new parent
                        for ojPjfd_div in ojPjfd_divs:

                            # Personal info
                            h3_element = ojPjfd_div.find_element(By.TAG_NAME, "h3").text if ojPjfd_div.find_elements(
                                By.TAG_NAME, "h3") else "Unknown"

                            #Name, Email address, User IDs, Address, Phone number, and Other info
                            h3_content = ojPjfd_div.find_element(By.CLASS_NAME,
                                                                    "fozKzd").text if ojPjfd_div.find_elements(
                                By.CLASS_NAME, "fozKzd") else "Unknown"

                            ZirXzb = ojPjfd_div.find_element(By.CLASS_NAME,
                                                            "ZirXzb").text if ojPjfd_div.find_elements(
                                By.CLASS_NAME, "ZirXzb") else None

                            # find all class="GcNQi" divs
                            GcNQi = ojPjfd_div.find_elements(By.CLASS_NAME, "GcNQi")

                            # store big details
                            big_details_exp = []  

                            for GcNQi_div in GcNQi:
                                h4_elements = [h4.text for h4 in GcNQi_div.find_elements(By.TAG_NAME, "h4")]
                                FnWDnes = [fn.text for fn in GcNQi_div.find_elements(By.CLASS_NAME, "FnWDne")]

                                if len(h4_elements) == len(FnWDnes):
                                    json_obj = {key: value for key, value in zip(h4_elements, FnWDnes)}  
                                    big_details_exp.append(json_obj)  

                            details.append({
                                h3_element: h3_content,
                                ZirXzb: big_details_exp
                            })

                        result.append({
                            title:details
                        })

                except Exception as e:
                    print(f"error: {e}")
                    logger.error(f"error:{url} Exception: {e}")
        else:
            print(f"class='Mf2Txd' div fail:{url}")
            logger.error(f"class='Mf2Txd' div fail:{url}")

    except urllib3.exceptions.ReadTimeoutError as e:
        logger.error(f"ReadTimeoutError: url: {url} Exception: {e}")
        print(f"ReadTimeoutError occurred, skipping url: {url}")

    except Exception as e:
        print(f"class='Mf2Txd' div fail:{url}---- {e}")
        logger.error(f"class='Mf2Txd' div fail:{url}---- {e}")

    logger.warning(url)
    print(f"result: {result}")
    return result

def get_data_safety(app_id):
    print(f"enter get_data_safety {app_id}")
    url = f"https://play.google.com/store/apps/datasafety?id={app_id}&hl=en"
    driver.get(url)

    time.sleep(1)  

    page_text = driver.page_source

    if "We're sorry, the requested URL was not found on this server." not in page_text:    
        wait_open_i()

        parsed_data = get_structure_data(url)

        GetCommon.save_new_json_file(f"Label_google/{app_id}_label.json",parsed_data)

    print("successful!")

def wait_open_i():
    print("enter wait_open_i")

    try:
        # wait for the 'expand_more' icon to be present
        element = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//i[text()='expand_more']"))
        )

        if element:
            print("Found 'expand_more', performing actions...")
            # Scroll to the element and click it
            expand_more_icons = driver.find_elements(By.XPATH, "//i[text()='expand_more']")

            for icon in expand_more_icons:
                try:
                    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", icon)
                    driver.execute_script("arguments[0].click();", icon)

                except ElementClickInterceptedException:
                    print("ElementClickInterceptedException: covered by another element, trying to click again...")

                except Exception as e:
                    print(f"Error clicking 'expand_more': {e}")

    except TimeoutException:
        print("TimeoutException wait_open_i: can not find 'expand_more' button")

    except Exception as e:
        print("Error wait_open_i:", e)

    print("leave wait_open_i")

def process_item(item):
    with driver_lock:  # Ensure thread-safe access to the driver
        get_data_safety(item)  # Pass the shared driver

def batch_iterator(iterable, batch_size):
    """Yield items from iterable in chunks (batches) of batch_size."""
    iterator = iter(iterable)
    while batch := list(itertools.islice(iterator, batch_size)):
        yield batch

def get_all_privacy_threaded():
    with ThreadPoolExecutor(max_workers=MAX_CONCURRENT_THREADS) as executor:
        for batch in batch_iterator(app_info_datas, BATCH_SIZE):  # Process batch by batch
            list(executor.map(process_item, batch))  # Map ensures tasks complete in this batch

if __name__ == "__main__":
    logger = GetCommon.getLogger("GooglePlayLabel")

    app_info_datas = GetCommon.get_app_info(r"AppInfo_google\appInfo_google.json")

    MAX_CONCURRENT_THREADS = 20  # Limit concurrent threads
    BATCH_SIZE = 200  # Control how many items to load into memory at a time
    # Global driver instance (must be accessed in a thread-safe way)
    driver_lock = threading.Lock()
    driver = GetCommon.setup_driver()  # Or any other browser
    # Call the function
    get_all_privacy_threaded()
    driver.quit()