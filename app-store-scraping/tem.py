import GetCommon
import pandas as pd
import json
from bs4 import BeautifulSoup
import re
import os
import requests
from langdetect import detect, LangDetectException
import shutil
import json
from urllib.parse import urlparse, urlsplit
from collections import defaultdict
import json
from urllib.parse import urlparse
from collections import defaultdict
import shutil


def make_file():
    for i in range(1,40):
        with open(f"AppInfo_google/appInfo_google_new_{i}.json", "w", encoding="utf-8") as f:
            pass

def del_file(folder_path,end,flagDir):
    with open(r"pythonProject\AppInfo_google\remove.json", "r", encoding="utf-8") as f:
        app_ids = json.load(f)  

    if flagDir:
        target_names = [app_id for app_id in app_ids if app_id.strip()]
    else:
        target_names = [app_id.strip() + end for app_id in app_ids if app_id.strip()]

    count = 0

    for filename in os.listdir(folder_path):
        if filename in target_names:
            file_path = os.path.join(folder_path, filename)

            print(file_path)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
            count += 1
            print(f"remove {count}: {file_path}")

    print("done, total removed files:", count)

def split_file(input_file, output_prefix, lines_per_file=5000):
    with open(input_file, 'r', encoding='utf-8') as infile:
        file_count = 1
        lines = []

        for line_number, line in enumerate(infile, start=1):
            lines.append(line)

            if line_number % lines_per_file == 0:
                output_file = f"{output_prefix}_{file_count}.json"
                with open(output_file, 'w', encoding='utf-8') as outfile:
                    outfile.writelines(lines)
                print(f"already write: {output_file}")

                # empty the lines list for the next file
                lines = []
                file_count += 1

        # handle any remaining lines after the loop
        if lines:
            output_file = f"{output_prefix}_{file_count}.json"
            with open(output_file, 'w', encoding='utf-8') as outfile:
                outfile.writelines(lines)
            print(f"{output_file}")

def create_appInfo():

    csv_file = r"C:\Users\smile\PycharmProjects\pythonProject\data_csv\google_appInfo.csv" 
    df = pd.read_csv(csv_file)

    data_list = df.to_dict(orient="records")  

    json_file = r"/pythonProject/AppInfo_google/appInfo_google_detail.json"

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data_list, f, indent=4, ensure_ascii=False)

    print(f"data save path {json_file}")

def count_words():
    file_path = r"C:\Users\smile\PycharmProjects\pythonProject\Policy_appstore\1569408041_policy"  
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
        words = text.split()  
        word_count = len(words)
        print(f"count num: {word_count}")

def split_privacy():
    error_keywords = [
        "400", "401", "403", "404", "408",
        "500", "501", "502", "503", "504",
        "301", "302", "307"
    ]
    # logger = GetCommon.getLogger("tem")
    # input_folder = r"C:\Users\smile\PycharmProjects\pythonProject\Policy_google"  
    input_folder = r"C:\Users\smile\PycharmProjects\pythonProject\Policy_google"
    main_privacy_output_folder = r"C:\Users\smile\PycharmProjects\pythonProject\tem\main"
    sub_privacy_output_folder = r"C:\Users\smile\PycharmProjects\pythonProject\tem\sub"
    empty_main_privacy_log = r"\Users\smile\PycharmProjects\pythonProject\Policy_google_split\empty_main_privacy_log.txt"
    info=GetCommon.get_app_info(r"pythonProject\AppInfo_google\b.json")
    os.makedirs(main_privacy_output_folder, exist_ok=True)
    os.makedirs(sub_privacy_output_folder, exist_ok=True)

    open(empty_main_privacy_log, 'w').close()

    for filename in os.listdir(input_folder):
        if filename in info:
            print(f"enter: {filename}")
            try:
                filepath = os.path.join(input_folder, filename)
                clean_name = filename.removesuffix("_policy")

                if os.path.isfile(filepath):
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        lines = content.strip().splitlines()
                    
                        if not content:
                            GetCommon.save_add_json_file(r"AppInfo_google\privacy_content_empty.json",clean_name)
                            continue
                        elif len(lines) <= 3 and any(err in content for err in error_keywords):
                            GetCommon.save_add_json_file(r"AppInfo_google\privacy_less3_lines_error_code.json",clean_name)
                            continue 
                        elif detect(content) != 'en':
                            GetCommon.save_add_json_file(r"AppInfo_google\privacy_non_en.json",clean_name)
                            continue
                        else:
                            if content.count("Sub-section Policy:") == 0:
                                with open(os.path.join(main_privacy_output_folder, filename), 'w', encoding='utf-8') as f_before:
                                    f_before.write(content)
                                # GetCommon.save_add_json_file(r"AppInfo_google\only_main_privacy.json",clean_name)
                                continue
                            elif content.count("Sub-section Policy:") == 1:
                                parts = content.split("Sub-section Policy:", 1)

                                before = parts[0].strip() if len(parts) > 0 else ""
                                after = parts[1].strip() if len(parts) > 1 else ""

                                if before:
                                    with open(os.path.join(main_privacy_output_folder, filename), 'w', encoding='utf-8') as f_before:
                                        f_before.write(before)
                                    GetCommon.save_add_json_file(r"AppInfo_google\main_sub_privacy.json",clean_name)
                                    continue
                                else:
                                    with open(empty_main_privacy_log, 'a', encoding='utf-8') as log:
                                        log.write(filename + '\n')

                                if after:
                                    with open(os.path.join(sub_privacy_output_folder, filename), 'w', encoding='utf-8') as f_after:
                                        f_after.write(after)
                                    GetCommon.save_add_json_file(r"AppInfo_google\main_sub_privacy.json",clean_name)
                                    continue
                                else:
                                    GetCommon.save_add_json_file(r"AppInfo_google\only_main_privacy.json",clean_name)
                                
                            else:
                                GetCommon.save_add_json_file(r"AppInfo_google\mutil_sub_privacy_error.json",clean_name)
                                continue
            except LangDetectException:
                # logger.error(f"cant judege lan:{filename}")
                continue
                   
            except Exception as e:
                # logger.error(filename)
                print(f"error: {e}")
                continue
    print("done")

def combianAPPstoreId():
    folder_path = "AppInfo_appstore"

    json_files = [
        f for f in os.listdir(folder_path)
        if f.endswith(".json") and os.path.isfile(os.path.join(folder_path, f))
    ]

    combined_data = []
    seen_ids = set()

    for filename in json_files:
        filepath = folder_path+"/"+filename
        print(filepath)
        with open(filepath, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if isinstance(data, list):
                    for item in data:
                        item_id = item.get("id")
                        if item_id is not None and item_id not in seen_ids:
                            seen_ids.add(item_id)
                            combined_data.append(item)
                else:
                    print(f"{filename} contains non-list data, skip")
            except json.JSONDecodeError:
                print(f"{filename} not a valid JSON file, skip")

    with open(r"AppInfo_appstore/merged_unique.json", "w", encoding="utf-8") as out_file:
        json.dump(combined_data, out_file, ensure_ascii=False, indent=2)

    print("done, total unique ids:", len(seen_ids))

def load_json_array(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data if isinstance(data, list) else []

def remove_dupulicate_ios():

    file1_data = load_json_array(r"AppInfo_appstore\merged_unique.json")
    file2_data = load_json_array(r"AppInfo_google\tem_app_store\appInfo_data.json")

    file2_ids = {item["id"] for item in file2_data if "id" in item}

    diff_items = [item for item in file1_data if item.get("id") not in file2_ids]

    with open(r"AppInfo_appstore\appInfo_data_new.json", "w", encoding="utf-8") as f_out:
        json.dump(diff_items, f_out, ensure_ascii=False, indent=2)

    print(f"filter done: total num: {len(diff_items)}")

def process_log_file(input_path, output_path):
    # YYYY-MM-DD HH:MM:SS,mmm
    datetime_pattern = re.compile(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}')

    with open(input_path, 'r', encoding='utf-8') as file, \
         open(output_path, 'w', encoding='utf-8') as out_file:

        for line in file:
            line = line.strip()
            if not line:
                continue  
            if datetime_pattern.match(line):
                out_file.write(line + '\n')  

def clean_log(file_path,target_path,reg):
    # YYYY-MM-DD HH:MM:SS,mmm
    datetime_pattern = re.compile(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}')
    app_id_pattern = re.compile(reg)

    seen_app_ids = set()

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if not datetime_pattern.match(line):
                continue  

            app_id_match = app_id_pattern.search(line)
            if app_id_match:
                app_id = app_id_match.group(1)
                if app_id not in seen_app_ids:
                    seen_app_ids.add(app_id)
            else:
                continue
    print(f"len:{len(list(seen_app_ids))}")
    GetCommon.save_new_json_file(target_path,list(seen_app_ids))

def remove_non_en_ios_app():
    english_country_codes = {"US", "GB", "CA", "AU", "NZ", "IE", "SG", "IN"}

    with open(r"AppInfo_appstore\appInfo_data_new.json", 'r', encoding='utf-8') as f:
        data = json.load(f)

    filtered_data = []
    for item in data:
        match = re.search(r'https://apps\.apple\.com/([^/]+)/app', item['url'])
        if match:
            country_code = match.group(1).upper()
            if country_code in english_country_codes:
                filtered_data.append(item)

    with open(r"AppInfo_appstore\appInfo_data_en_new.json", 'w', encoding='utf-8') as f:
        json.dump(filtered_data, f, indent=2, ensure_ascii=False)

    print(f"total num: {len(filtered_data)} ")

def extract_key_from_google(file_path,key,can_open_file,can_not_open_file):
    app_ids = set()
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                match = re.search(r'({.*})', line)
                if match:
                    data = json.loads(match.group(1))
                    app_id = data.get(key)
                    if app_id:
                        if key == "privacyPolicy":
                            try:
                                if can_open_file == "unique_url":
                                    app_ids.add(app_id)
                                elif can_open_file == "pdf":
                                    if app_id.endswith(".pdf"):
                                         with open(r"AppInfo_google\can_open_privacy_pdf", 'a', encoding='utf-8') as vf:
                                            vf.write(line)
                                    else:
                                         with open(r"Logger\split_log\google\can_open_que_unique", 'a', encoding='utf-8') as vf:
                                            vf.write(line)
                                else:
                                    response = requests.get(app_id, timeout=10)
                                    if response.status_code == 200:
                                        with open(can_open_file, 'a', encoding='utf-8') as vf:
                                            vf.write(line)
                                    else:
                                        with open(can_not_open_file, 'a', encoding='utf-8') as ivf:
                                            ivf.write(line)
                            except Exception as e:
                                with open(can_not_open_file, 'a', encoding='utf-8') as ivf:
                                    ivf.write(line)
                        else:
                            app_ids.add(app_id)
                        
            except Exception as e:
                print(f"Error parsing line in A: {line}\n{e}")
    return app_ids

def filter_file_by_app_ids(source_path, app_ids):
    result_lines = []
    with open(source_path, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                match = re.search(r'({.*})', line)
                if match:
                    data = json.loads(match.group(1))
                    app_id = data.get("app_id")
                    if app_id and app_id in app_ids:
                        continue  
                result_lines.append(line)  
            except Exception as e:
                print(f"Error parsing line in {source_path}: {line}\n{e}")
                result_lines.append(line)
    
    with open(source_path, 'w', encoding='utf-8') as file:
        file.writelines(result_lines)

import json

def clean_and_extract_json_lines(input_path, output_path):
    result = []

    with open(input_path, 'r', encoding='utf-8') as file:
        for line in file:
            try:
               
                json_start = line.find('{"app_id"')
                if json_start != -1:
                    json_part = line[json_start:]
                    data = json.loads(json_part)
                    result.append(data)
            except Exception as e:
                print(f"Error parsing line: {line}\n{e}")

    with open(output_path, 'w', encoding='utf-8') as out_file:
        json.dump(result, out_file, indent=2, ensure_ascii=False)

def remove_fix_line_log(input_path, output_path,other_path,target_key,target_value):

    new_lines = []
    app_ids = []

    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.search(r'(\{.*\})', line)
            if match:
                json_part = match.group(1)
                try:
                    data = json.loads(json_part)
                    if data.get(target_key) == target_value:
                        if "app_id" in data:
                            app_ids.append(data["app_id"])
                        continue  
                except json.JSONDecodeError:
                    pass  
            new_lines.append(line)

    with open(output_path, 'w', encoding='utf-8') as out_f:
        for app_id in app_ids:
            out_f.write(json.dumps(app_id) + "\n")
            # out_f.write(f"{app_id}\n")

    # copy the new lines to the original file
    for path in other_path:
        with open(path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)


def analysys_error_log():
    a_file = r"Logger\split_log\google\error_more_links.log"
    b_file = r"Logger\split_log\google\wait_extra_privacy.log"
    c_file = r"Logger\split_log\google\enter_wrong_privacy_url.log"
    d_file = r"Logger\split_log\google\privacy_data_is_null.log"
    e_file = r"Logger\split_log\google\other_types_errors.log"
    can_open_file = r"Logger\split_log\google\can_open"
    can_open_file_que = r"Logger\split_log\google\can_open_que"
    can_not_open_file = r"Logger\split_log\google\can_not_open"
    other_path=[b_file,c_file,d_file,e_file,can_open_file]

    # remove_fix_line_log(can_open_file,r"AppInfo_google\remove.json",other_path,"privacyPolicy","https://blog.naver.com/mkhong0816/222468586349")

    app_ids_from_google = extract_key_from_google(r"AppInfo_google\remove.json","app_id","","")
    GetCommon.save_add_json_file(r"AppInfo_google\error_privacy.json",list(app_ids_from_google))

    # for path in [b_file, c_file, d_file, e_file]:
    #     # filter_file_by_app_ids(path, app_ids_from_google)
    #     extract_key_from_google(path,"privacyPolicy",can_open_file,can_not_open_file)
    
    # clean_and_extract_json_lines(a_file, r"AppInfo_google\sub_privacy_error_app")

    
    # ids = extract_key_from_google(can_open_file,"privacyPolicy","unique_url","")
    # GetCommon.save_new_json_file(r"AppInfo_google\tem_can_open_unique.json",list(ids))

    # extract_key_from_google(can_open_file,"privacyPolicy","pdf","")

    # deduplicate_log_by_app_id(can_open_file,can_open_file_que)

def deduplicate_log_by_app_id(input_path, output_path):
    seen_app_ids = set()
    unique_lines = []

    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                json_start = line.find('{')
                if json_start != -1:
                    data = json.loads(line[json_start:])
                    app_id = data.get("app_id")
                    if app_id and app_id not in seen_app_ids:
                        seen_app_ids.add(app_id)
                        unique_lines.append(line)
            except json.JSONDecodeError:
                pass  

    with open(output_path, 'w', encoding='utf-8') as out_f:
        out_f.writelines(unique_lines)

    print(f"total num: {len(unique_lines)} ")

def read_file_name(flag):

    # fix_dir = r"C:\Users\smile\PycharmProjects\pythonProject\Policy_google"
    fix_dir = r"C:\Users\smile\PycharmProjects\pythonProject\Label_google"

    for filename in os.listdir(fix_dir):
        if(flag=="remove_dup_main_privacy"):
            print(f"enter panduan：{filename}")
            file_path = os.path.join(fix_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            repeated = find_repeated_section(content)
            if repeated:
                print(f"find duplicate content: {filename}")
                GetCommon.save_add_json_file(r"find_dup.json",filename)
                GetCommon.save_new_txt_file(f"C:/Users/smile/PycharmProjects/pythonProject/Policy_google_split/remove/{filename}",repeated)
            else:
                print(f"no duplicate:{filename}")
                GetCommon.save_add_json_file(r"cant_find_dup.json",filename)
        else:
            # GetCommon.save_add_json_file(r"AppInfo_google\a.json",filename)
            GetCommon.save_add_json_file(r"pythonProject\AppInfo_google\b.json",filename)

def find_repeated_section(text):
    n = len(text)
    for i in range(1, n // 2 + 1):
        candidate = text[:i]
        if text.startswith(candidate * 2):
            return candidate
    return None

def repalce_dup_content():

    target_dir = r"C:\Users\smile\PycharmProjects\pythonProject\Policy_google_split\remove"
    reference_file = r"C:\Users\smile\PycharmProjects\pythonProject\Policy_google_split\remove\co.uk.twinkl.twinklaugmentedreality_policy"

    with open(reference_file, 'r', encoding='utf-8') as ref:
        new_content = ref.read()

    for filename in os.listdir(target_dir):
        file_path = os.path.join(target_dir, filename)

        if os.path.isfile(file_path) and os.path.getsize(file_path) == 113193:
            print(f"alternative file: {filename}")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"ok: {filename}")

def replace_file_name():

    target_dir = r"C:\Users\smile\PycharmProjects\pythonProject\Policy_google_split\remove"

    for filename in os.listdir(target_dir):
        if filename.startswith("split_"):
            old_path = os.path.join(target_dir, filename)
            new_filename = filename[len("split_"):]  
            new_path = os.path.join(target_dir, new_filename)

            if os.path.exists(new_path):
                print(f"file exist, skip: {new_filename}")
                continue

            os.rename(old_path, new_path)
            print(f"rename: {filename} → {new_filename}")

def move_fix_file():
    json_path = r'AppInfo_google\que.json'            
    source_folder = r'C:\Users\smile\PycharmProjects\pythonProject\Policy_google_split\main_privacy'        # 原文件夹路径
    destination_folder = r'C:\Users\smile\PycharmProjects\pythonProject\target'  

    os.makedirs(destination_folder, exist_ok=True)

    with open(json_path, 'r', encoding='utf-8') as f:
        target_files = json.load(f)

    for filename in os.listdir(source_folder):
        if filename in target_files:
            src_path = os.path.join(source_folder, filename)
            dst_path = os.path.join(destination_folder, filename)
            shutil.move(src_path, dst_path)
            print(f"Moved: {filename}")

    print("done")

import requests
from readabilipy import simple_json_from_html_string
def test_get_privacy():
    appinfo = GetCommon.get_app_info(r"pythonProject\AppInfo_google\test.json")
    for app in appinfo:
        url = app["privacy_policy_url"]
        app_id = app["app_id"]

        try:
            response = requests.get(url, timeout=10)
            html_string = response.text

            html_string = re.sub(r'<\?xml.*?\?>', '', html_string)

            soup = BeautifulSoup(html_string, "lxml")
            for footer in soup.find_all("footer"):
                footer.decompose()  
            html_string = str(soup)  

            result = simple_json_from_html_string(html_string, use_readability=True)

            with open(f"pythonProject/AppInfo_google/test/test_{app_id}.txt", "w", encoding="utf-8") as f:
                for item in result["plain_text"]:
                    if isinstance(item, dict) and "text" in item:
                        f.write(item["text"] + "\n\n")  
        except Exception as e:
            print(f"❌ Error processing {app_id}: {e}")
            
def vaild_file():
    # target_root_folder = r"C:\Users\smile\PycharmProjects\pythonProject\Policy_google" 

    # for subfolder in os.listdir(target_root_folder):
    #     subfolder_path = os.path.join(target_root_folder, subfolder)
    #     if os.path.isdir(subfolder_path):
    #         GetCommon.save_add_json_file(r"pythonProject\AppInfo_google\d.json",subfolder)


    folder_path = r"C:\Users\smile\PycharmProjects\pythonProject\privacy_url_num_copy"
    d_json_path = r"pythonProject\AppInfo_google\d.json"  

    with open(d_json_path, "r", encoding="utf-8") as f:
        d_app_ids = set(json.load(f))  

    extra_files = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            app_id = filename[:-5]  
            if app_id not in d_app_ids:
                extra_files.append(filename)

    for file in extra_files:
        print(file)

def strip_policy_suffix(filename):
    return filename.removesuffix('_policy.txt') if filename.endswith('_policy.txt') else filename

def change_content():
    target_file = r"pythonProject\Policy_google\me.jlabs.alarmclock\me.jlabs.voicerecorder_policy.txt"
    target_file_path = os.path.abspath(target_file)
    folder_path = os.path.dirname(target_file_path)

    all_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path)
                 if os.path.isfile(os.path.join(folder_path, f))]

    stripped_names = [strip_policy_suffix(os.path.basename(f)) for f in all_files]
    print(f"{stripped_names}")

    if len(all_files) <= 1:
        print("file=1")
        return

    with open(target_file_path, 'rb') as f:
        content = f.read()

    for file in all_files:
        if os.path.abspath(file) != target_file_path:
            with open(file, 'wb') as f:
                f.write(content)
            print(f"use {os.path.basename(target_file_path)} change {os.path.basename(file)}")

    print("done")

def del_json():
    patha=r"pythonProject\AppInfo_google\remove.json"
    pathnew=r"pythonProject\AppInfo_google\a.json"
    # pathb = r"pythonProject\AppInfo_google\appInfo_google.json"
    # pathb=r"pythonProject\AppInfo_google\donot_have_label.json"
    pathb = r"pythonProject\AppInfo_google\have_label.json"
    # pathb = r"pythonProject\AppInfo_google\not_have_privacy_url.json"
    GetCommon.filter_content(patha,pathb,pathnew,True)

def from_dicct_to_json(input_path,output_path):

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"file not exist: {input_path}")

    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if not content:
            raise ValueError("cant parse JSON")

        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON parse fail: {e}")

    flattened = []
    for entries in data.values():
        flattened.extend(entries)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(flattened, f, ensure_ascii=False, indent=4)

def a():

    with open('pythonProject\AppInfo_google\privacy_url_category_num.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    url_to_keys = defaultdict(set)

    for top_key, apps in data.items():
        for app in apps:
            full_url = app.get("privacy_policy_url", "")
            url_base = urlsplit(full_url)._replace(query="").geturl()  
            url_to_keys[url_base].add(top_key)

    for base_url, keys in url_to_keys.items():
        if len(keys) > 1:
            print(f"URL base '{base_url}' appears in multiple top-level keys: {keys}")

if __name__ == "__main__":
    directory_path = r"C:\Users\smile\PycharmProjects\pythonProject\Label_appstore"
    id_file_path = r"\AppInfo_appstore\handle_error_info\missing_ids.json"
    logger = GetCommon.getLogger("GooglePlayPrivacymethod2")
    # a()
    # vaild_file()
    # change_content()
    # pathc = r"pythonProject\AppInfo_google\have_privacy_url_cant_open.json"
    # pathd = r"pythonProject\AppInfo_google\have_privacy_url_cant_open_dict.json"
    # from_dicct_to_json(pathd,pathc)

    # json_folder = r"C:\Users\smile\PycharmProjects\pythonProject\privacy_url_num_copy"         
    # target_root_folder = r"pythonProject\AppInfo_google\have_privacy_url_200.json" 

    # with open(target_root_folder, 'r', encoding='utf-8') as f:
    #     data = json.load(f)  
    
    # for entry in data:
    #     if isinstance(entry, dict) and "app_id" in entry:
    #         app_id = entry["app_id"]
    #         json_filename = f"{app_id}.json"
    #         json_file_path = os.path.join(json_folder, json_filename)
    #         with open(json_file_path, "r", encoding="utf-8") as f:
    #             json_data = json.load(f)
            
    #         json_length = len(json_data)
    #         if json_length > 1:
    #             print(f"{entry} json length: {json_length}")
    #         else:
    #             GetCommon.save_add_json_file(r"pythonProject\AppInfo_google\not_en_app_id.json",entry["app_id"])
    
    # test_get_privacy()
    # process_log_file(r"Logger\GooglePlayPrivacy_new_error.log",r"Logger\GooglePlayPrivacy_new_new_error.log")
    # clean_log(r"Logger\GooglePlayPrivacy_new_error.log",r"AppInfo_google\error_privacy.json",r'"app_id"\s*:\s*"([^"]+)"')
    # split_privacy()
    # analysys_error_log()

    # ids = extract_key_from_google(r"Logger\split_log\google\can_open","app_id")
    # GetCommon.save_add_json_file(r"AppInfo_google\a.json",list(ids))
    

    # GetCommon.get_file_name(r"C:\Users\smile\PycharmProjects\pythonProject\Policy_google_split\main_privacy",r"pythonProject\AppInfo_google\b.json",1080,"size","")
    # GetCommon.get_file_name(r"C:\Users\smile\PycharmProjects\pythonProject\Policy_google_old",r"AppInfo_google\Policy_google_local_file.json",1000000000000,"size","")

    # combianAPPstoreId()
    # remove_dupulicate_ios()
    # remove_non_en_ios_app()

    # process_log_file(r"Logger\GooglePlayLabel_error.log", r"Logger\GooglePlayLabel_unique_error.log")

    
    # app_info_datas = GetCommon.get_app_info(r"pythonProject\AppInfo_google\have_privacy_app_info.json")
    # for entry in app_info_datas:
    #     GetCommon.save_add_json_file(r"pythonProject\AppInfo_google\a_unique.json",entry['app_id'])

    # app_info_datas = GetCommon.get_app_info(r"pythonProject\AppInfo_google\have_privacy_app_info.json")
    # seen = set()
    # deduped = []
    # for entry in app_info_datas:
    #     if entry['app_id'] not in seen:
    #         GetCommon.save_add_json_file(r"pythonProject\AppInfo_google\a_unique.json",entry)
    #         seen.add(entry['app_id'])

    # app_info_datas = GetCommon.get_app_info(r"pythonProject\AppInfo_google\not_have_privacy.json")
    # unique_data = list(set(app_info_datas))
    # print(f"unique_data:{len(unique_data)}")
    # GetCommon.save_new_json_file(r"pythonProject\AppInfo_google\unique.json",unique_data)

    # patha=r"pythonProject\AppInfo_google\have_privacy_url.json"
    # pathb=r"pythonProject\AppInfo_google\a.json"
    # pathnew=r"pythonProject\AppInfo_google\cc.json"
    # GetCommon.filter_content(patha,pathb,pathnew,True)


    # import json

    with open(r'pythonProject\AppInfo_google\privacy_url_category_num.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    all_app_ids = []

    for app_list in data.values():
        for app in app_list:
            app_id = app.get("app_id")
            if app_id:
                GetCommon.save_add_json_file(r"pythonProject\AppInfo_google\a.json",app_id)

    # for dirpath, dirnames, files in os.walk(r"C:\Users\smile\PycharmProjects\pythonProject\Policy_google"):
    #     for file in files:
    #         GetCommon.save_add_json_file(r"pythonProject\AppInfo_google\b.json",file)

    
    # for file in os.listdir(r"C:\Users\smile\PycharmProjects\pythonProject\Label_google"):
    #     GetCommon.save_add_json_file(r"pythonProject\AppInfo_google\b.json",file)


    # with open(r"pythonProject\AppInfo_google\have_privacy_url_cant_open.json", "r", encoding="utf-8") as f:
    #     a_data = json.load(f)

    # with open(r"pythonProject\AppInfo_google\not_en_app_id.json", "r", encoding="utf-8") as f:
    #     b_data = json.load(f)

    # filtered_a_data = [item for item in a_data if item["app_id"] not in b_data]

    # with open(r"pythonProject\AppInfo_google\have_privacy_url_cant_open_que.json", "w", encoding="utf-8") as f:
    #     json.dump(filtered_a_data, f, indent=4, ensure_ascii=False)

    # a = GetCommon.get_app_info(r"pythonProject\AppInfo_google\not_en_app_id.json")
    # with open(r"pythonProject\AppInfo_google\have_privacy_app_info.json", "r", encoding="utf-8") as f:
    #     data = json.load(f)
    # filtered_data = [app for app in data if app["app_id"] not in a]
    # with open(r"pythonProject\AppInfo_google\have_privacy_app_info_filtered.json", "w", encoding="utf-8") as f:
    #     json.dump(filtered_data, f, ensure_ascii=False, indent=2)

    # GetCommon.read_id(r"2025-mcm-bali\src\app-store-scraping\Logger\GooglePlayLabel_error.log",r"AppInfo_google\not_label.json",r'id"\s*:\s*"([^"]+)"')
    # GetCommon.read_id_by_json(r"pythonProject\AppInfo_google\have_privacy_url_cant_open.json",r"pythonProject\AppInfo_google\remove2.json",logger)

    # count_words()

    # create_appInfo()

    # move_fix_file()
    # del_file(r"C:\Users\smile\PycharmProjects\pythonProject\Label_google","_label.json",False)
    # del_file(r"C:\Users\smile\PycharmProjects\pythonProject\Policy_google","_policy.txt",True)
    # del_json()

    # del_file(r"C:\Users\smile\PycharmProjects\pythonProject\privacy_url_num",".json")


    # read_file_name("")
    # read_file_name("remove_dup_main_privacy")
    # replace_file_name()
    # repalce_dup_content()
    # make_file

    # split_file(r"AppInfo_google\appInfo_google.json", r"AppInfo_google\appInfo_google_", 10000)

    # # make_diff()
    # C:\Users\smile\PycharmProjects\pythonProject\Label_google
    # C:\Users\smile\PycharmProjects\pythonProject\Policy_google
    # C:\Users\smile\PycharmProjects\pythonProject\Policy_appstore
    # GetCommon.convert_upper(r"AppInfo_google\scategories_new.json",r"AppInfo_google\categories_target.json")

    # C:\Users\smile\PycharmProjects\pythonProject\AppInfo_appstore\appInfo_data_1.json
    # C:\Users\smile\PycharmProjects\pythonProject\AppInfo_google\Untitled-2.json
    #C:\Users\smile\PycharmProjects\pythonProject\AppInfo_google\appInfo_google_new.json
    #C:\Users\smile\PycharmProjects\pythonProject\AppInfo_google\appInfo_google.json
    # AppInfo_google\appInfo_google.json
    # GetCommon.filter_content(r"AppInfo_google\ids_successful.json",r"AppInfo_google\a.json",
    #                          r"AppInfo_google\diff.json")
    # GetCommon.filter_content(r"AppInfo_google\appInfo_google.json",r"AppInfo_google\appInfo_google_new.json",
    #                          r"AppInfo_google\diff.json")
