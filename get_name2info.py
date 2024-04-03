from config import *
from utils import *
import argparse

argparser = argparse.ArgumentParser()
argparser.add_argument('--no_cache', action='store_false',
                       help='Whether to cache the html of all people')
argparser.add_argument('--no_update', action='store_false',
                       help='Whether to update the cache')
argparser.add_argument('--update_textblock', action='store_true',
                       help='Whether to update the textblock list | Note: Available only when \"no_cache\" is \"NOT\" checked! (Since that will take too much long...)')
args = argparser.parse_args()
doCache = args.no_cache
doUpdate = args.no_update
doUpdateTextblock = args.update_textblock

if not doCache:
    doUpdateTextblock = False

TEXTBLOCK_LIST = updateTextblockList() if doUpdateTextblock else TEXTBLOCK_LIST

print(
    f"[INFO] You choose to {'NOT ' if not doCache else ''}cache (download) the html file of all people.")

# Proxy off
os.environ['no_proxy'] = '*'

# Read the name2url from the csv file
name2url_all = load_csv2dict(pth_name2url)

if doCache:
    # Judge whether the cache is up-to-date
    if doUpdate:
        num_newest_terms = len(name2url_all.items())
        num_cached_files = len(os.listdir(DIR_CACHE_ROOT))

        # Case 1: If the number of cached files is equal to the number of newest terms, then the cache is up-to-date
        if num_cached_files == num_newest_terms:
            print("[INFO] The cache is up-to-date. (The number of cached files is equal to the number of newest terms detected.)")

        # Case 2: If the number of cached files is not equal to the number of newest terms, then the cache is out-of-date
        else:
            print("[INFO] The cache is out-of-date, start caching...")
            print("       It will take about 100MB.")

            # Backup the cache folder if it is not empty
            if num_cached_files > 10:
                os.rename(DIR_CACHE_ROOT, DIR_CACHE_ROOT + SUFFIX_OUT_OF_DATE)
                print(
                    f"[INFO] Backup the cache folder to {DIR_CACHE_ROOT + SUFFIX_OUT_OF_DATE}")
                os.makedirs(DIR_CACHE_ROOT, exist_ok=True)

            # Cache the html of all people
            save2html_all_people(name2url_all)
            print("[INFO] Caching done.")

            # Check whether the number of cached files is equal to the number of newest terms
            num_cached_files = len(os.listdir(DIR_CACHE_ROOT))
            if num_cached_files == num_newest_terms:
                print("[INFO] The cache is up-to-date.")
            else:
                print(
                    "[WARNING] The number of cached files is not equal to the number of newest terms.")
                print(
                    f"          num_newest_terms: {num_newest_terms}, num_cached_files: {num_cached_files}")
                continue_or_not = input(
                    "[INFO] Do you want to continue? ([y]/n) ")
                if continue_or_not in ['y', 'Y', '']:
                    pass
                else:
                    print("[INFO] Abort.")
                    exit()

    # If doCache, collect info locally
    name2info_all = get_info_all_people_local(DIR_CACHE_ROOT)
    save2file(name2info_all.values(), pth_name2info, columns=BASIC_INFO_LIST + TEXTBLOCK_LIST, type='csv')

    save2file(name2info_all.values(), pth_name2info, columns=BASIC_INFO_LIST + TEXTBLOCK_LIST, type='xlsx')
    save2xlsx_sheeted(name2info_all.values(), pth_name2info, columns=BASIC_INFO_LIST + TEXTBLOCK_LIST)

else:
    # If not doCache, collect info from network
    pass
