from config import *
from utils import *

# Proxy off
os.environ['no_proxy'] = '*'

SAVE_COLUMNS = ['Name', 'Url']

name2url_all = get_name2url_all_pages(URL_ROOT)
print(f"[INFO] Got {len(name2url_all)} urls.")

save2file(name2url_all.items(), pth_name2url, columns=SAVE_COLUMNS, type='csv')
print(f"[INFO] Results saved to {pth_name2url}")

save2file(name2url_all.items(), pth_name2url, columns=SAVE_COLUMNS, type='xlsx')
print(f"[INFO] Results saved to {pth_name2url.replace('.csv', '.xlsx')}")

# Record the length of name2url_all.items()
with open(PTH_LENGTH_RECORD, "w") as f:
    f.write(f"Length of up-to-date name2url_all: {len(name2url_all)}")
    f.close()