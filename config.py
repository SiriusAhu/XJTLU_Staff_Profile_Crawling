import os
import time

DIR_OUTPUT_ROOT = "./output"
os.makedirs(DIR_OUTPUT_ROOT, exist_ok=True)
DIR_CACHE_ROOT = "./.cache"
os.makedirs(DIR_CACHE_ROOT, exist_ok=True)
PTH_LENGTH_RECORD = os.path.join(DIR_OUTPUT_ROOT, f"length_record-{time.strftime('%Y_%m_%d-%H_%M_%S', time.localtime())}.txt")
URL_ROOT = "https://scholar.xjtlu.edu.cn/en/persons/?nofollow=true&indexableKeyword=%2Fdk%2Fatira%2Fpure%2Fkeywords%2FPerson_Types%2Fstaff"  # staff only

INLINE_SEPATOR = " | "
SUFFIX_OUT_OF_DATE = "_out_of_date-at_least_from-" + \
    time.strftime("%Y_%m_%d-%H_%M_%S", time.localtime())
TEXTBLOCK_LIST = ['Personal profile',
                  'Research interests',
                  'Teaching',
                  'Awards and honours',
                  'Experience',]
BASIC_INFO_LIST = ['Name','Person Type', 'Department', 'Academic qualification']

pth_name2url = os.path.join(DIR_OUTPUT_ROOT, "_name2url.csv")
pth_name2info = os.path.join(DIR_OUTPUT_ROOT, "name2info.csv")
