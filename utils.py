import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
from config import *

# region Step 1: Get name2url
def get_name2url_single_page(url_person):
    """
    Given the url of any page, return a dictionary of name to url of all people in that page
    """
    response = requests.get(url_person)
    soup = BeautifulSoup(response.text, 'html.parser')
    persons = soup.find_all('h3', class_='title')
    name2url = {}
    for person in persons:
        name = person.find('span').string
        url_person = person.find('a')['href']
        # print(name, url)
        name2url[name] = url_person
    return name2url

def get_page_num(url_page):
    """
    Given the url of any page, return the max page number
    """
    response = requests.get(url_page)
    soup = BeautifulSoup(response.text, 'html.parser')
    page = soup.find_all('a', class_='step')[-1]
    return int(page.string)

def get_name2url_all_pages(url_root):
    """
    Given the root url, return a dictionary of all people
    """
    max_page = get_page_num(url_root)
    print(f"[info] {max_page} pages found.")
    all_people = {}
    for i in tqdm(range(1, max_page)):
        page_url = url_root + f"&page={i}"
        all_people.update(get_name2url_single_page(page_url))
    return all_people
# endregion

# region Step 2: Get info
def _get_department(soup_profile):
    """
    Given the soup of a person's profile, return the department of that person
    """
    department = soup_profile.find('a', class_='link primary')
    if department is None:
        return None
    return department.find('span').string

def _get_person_type(soup_profile):
    """
    Given the soup of a person's profile, return the person type of that person
    """
    return soup_profile.find('ul', class_='relations keywords').find_next('span').string

def _get_academic_qualification(soup_profile):
    """
    Given the soup of a person's profile, return the academic qualification of that person
    """
    half_div = soup_profile.find_all('div', class_='half')[1]
    all_divs = half_div.find_next('div').find_all('div')

    qualifications = []
    for div in all_divs:
        for p in div.find_all('p'):
            qualifications.append(p.text)
    # Remove the empty strings
    qualifications = [qualification for qualification in qualifications if qualification != '']

    # Separate the qualifications with the INLINE_SEPATOR
    qualifications = INLINE_SEPATOR.join(qualifications)
    return qualifications

def _get_textblock_info(soup_profile):
    """
    Get the information from the profile page (by inputting the soup object)
    """
    info = {}
    # Iterate through the h3 tags
    for h3 in soup_profile.find_all('h3', class_='subheader'):
        class_name = h3.text
        div = h3.find_next('div')
        if div is None:
            break
        # If the div is a textblock, that's what is needed
        if div.get('class') == ['textblock']:
            info[class_name] = []
            p_text = []
            # Iterate through the p tags, and append the text to the list
            for p in div.find_all('p'):
                p_text.append(p.text)
            # Join the list with the INLINE_SEPATOR (list -> str)
            info[class_name] = INLINE_SEPATOR.join(p_text)
    
    # Check whether all items in TEXTBLOCK_LIST are in the info, if not, add them with N/A
    for textblock in TEXTBLOCK_LIST:
        if textblock not in info:
            info[textblock] = 'N/A'
    return info

# -----------------------------------------------------------------------
    
# def get_info_single_person_network(url_profile, cache=True):
#     """
#     Given the url of a person's profile, return the department and research interests of that person
#     """
#     response = requests.get(url_profile)
#     soup_profile = BeautifulSoup(response.text, 'html.parser')
#     if cache:
#         pth = os.path.join(DIR_CACHE_ROOT, url_profile.split('/')[-1])
#         with open(pth, 'w') as f:
#             f.write(str(soup_profile))
#     info = {}
#     info['Department'] = _get_department(soup_profile)
#     info['Academic_qualification'] = _get_academic_qualification(soup_profile)
#     return info

# def get_info_all_people_network(name2url, cache=True):
#     """
#     Given a dictionary of name to url, return a dictionary of name to info
#     """
#     name2info = {}
#     for name, url in tqdm(name2url.items()):
#         name2info[name] = get_info_single_person_network(url, cache=cache)
#     return name2info

# -----------------------------------------------------------------------

def get_info_single_person_local(name, pth_html):
    """
    Given the path of a person's profile, return the department and research interests of that person
    """
    soup_profile = load_html2soup(pth_html)
    info = {}
    info['Name'] = name
    info['Person Type'] = _get_person_type(soup_profile)
    info['Department'] = _get_department(soup_profile)
    info['Academic Qualification'] = _get_academic_qualification(soup_profile)
    info.update(_get_textblock_info(soup_profile))
    return info

def get_info_all_people_local(dir_html):
    """
    Given a dictionary of name to url, return a dictionary of name to info
    """
    name2info = {}
    for pth_file in tqdm(os.listdir(dir_html)):
        name = pth_file.split('.')[0].replace('_', ' ') # Recover the name
        pth_html = os.path.join(dir_html, pth_file)
        name2info[name] = get_info_single_person_local(name, pth_html)
    return name2info
# -----------------------------------------------------------------------

def save2html_single_person(name, url_profile):
    """
    Given the url of a person's profile, save the html to the cache folder
    """
    response = requests.get(url_profile)
    soup_profile = BeautifulSoup(response.text, 'html.parser')
    pth = os.path.join(DIR_CACHE_ROOT, name.replace(' ', '_')) + '.html'
    with open(pth, 'w') as f:
        f.write(str(soup_profile))

def save2html_all_people(name2url):
    """
    Given a dictionary of name to url, save the html of all people to the cache folder
    """
    for name, url in tqdm(name2url.items()):
        save2html_single_person(name, url)
# endregion

# region load & save
def load_html2soup(html_path):
    """
    Given the html path, return the soup
    """
    with open(html_path, 'r') as f:
        return BeautifulSoup(f.read(), 'html.parser')

def load_csv2dict(file_path):
    """
    Given the file path, return the dictionary of name to info
    """
    df = pd.read_csv(file_path)
    return dict(zip(df['Name'], df['Url']))

def save2file(info, file_path_endwith_csv, columns=None, type='csv'):
    """
    Given the dictionary of name to info, save it to csv or excel
    ---
    type: 'csv' or 'xlsx' (default: 'csv')
    """
    df = pd.DataFrame(info, columns=columns)

    # sort the lines by: 1. Department, 2. Name
    sort_ref = ['Department', 'Name']
    if sort_ref[0] in df.columns and sort_ref[1] in df.columns:
        df = df.sort_values(by=['Department', 'Name'])
    if type == 'csv':
        df.to_csv(file_path_endwith_csv, index=False)
    elif type == 'xlsx':
        df.to_excel(file_path_endwith_csv.replace('.csv', '.xlsx'), index=False)
    else:
        print("[ERROR] Invalid type.")
        return

def save2xlsx_sheeted(info, file_path_endwith_csv, columns=None):
    """
    Given the dictionary of name to info, save it to xlsx with multiple sheets
    """
    writer = pd.ExcelWriter(file_path_endwith_csv.replace('.csv', '.xlsx'))
    df = pd.DataFrame(info, columns=columns)
    df = df.sort_values(by=['Department', 'Name'])
    for department in set(df['Department']):
        df_department = df[df['Department'] == department]
        df_department.to_excel(writer, sheet_name=department.replace(' ', '_') if department else 'None', index=False)
    writer._save()

# endregion
    
# region MISCS
def updateTextblockList(dir_html):
    """
    Given the directory of html files, return the textblock list
    """
    textblock_list = set()
    # Iterate through the html files, and get the textblock names
    for pth_file in os.listdir(dir_html):
        pth_html = os.path.join(dir_html, pth_file)
        soup_profile = load_html2soup(pth_html)
        textblock_list.update(_get_textblock_info(soup_profile).keys())
    return list(textblock_list)
    
# endregion