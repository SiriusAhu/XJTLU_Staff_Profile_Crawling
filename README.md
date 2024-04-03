# XJTLU Staff Profile Crawling
This is a simple web crawler that crawls the staff profiles of XJTLU.

## Why this project?
The official website of XJTLU only provides a name-based search for staff profiles. But sometimes we want to search some keywords in the profiles, e.g., "Machine Learning", which is not supported by the official website. 

This project is to crawl all the staff profiles of XJTLU and save them in local files (both `csv` and 'xlsx' formats). Then it is convenient to search the keywords in the local files.

## How to use?
### I just need the output files
Just download the `csv` and `xlsx` files in `Release`.

### I want to run the scripts by myself
1. Clone this repository.
2. Install the required packages by running `pip install -r requirements.txt`.
3. Run the first script to get a list of staff name to profile links by running `python get_name2url.py`.
4. Run the second script to get the staff profiles by running `python get_name2info.py`.
> Note: By running the second script, the `html` files will be saved in the `.cache` folder in case you want to check the raw html files. 
> But there is no need to worry about it downloads the files again and again.
> There is a check machanism to avoid meaningless downloads.
> See the `About information update` section for more details.

The output file will be located in the `output` folder, named `name2info.csv` and `name2info.xlsx`.

### About information update
The scripts are capable to update staff information when the number of people changes.

Here is how it works:
When `get_name2info.py` runs, it will check the number of people in the `name2url.csv` file and the number of files in `.cache` folder (if exists).
1. If the numbers are the same, it will skip the download process.
2. If the numbers are different, it will backup the old files to a `.cache_out_of_date-at_least_from-Y_M_D_H_M_S` folder and download the new files into the `.cache` folder.

> If you really don't want to update even though you may miss some new staff information, you can pass the `--no_update` argument to the script.
```python
python get_name2info.py --no_update
```

## Arguments
Some arguments are provided for the `get_name2info.py` script.
- `--no_cache`: Whether to cache the html of all people. (Just remove the cache files at the end of the script)
- `--no_update`: Whether to check for updates
- `--update_textblock`: Whether to update the textblock list. Note: Available only when `--no_cache` is not checked! (Since that will take too much long...)

> About `textblock`: See the `TEXTBLOCK_LIST` in `config.py`, you will figure out.

## Disclaimer
This project is intended for educational purposes only.

The use of this project for scraping information from the designated website(s) should comply with all applicable laws and the website's terms of service.

The developer assumes no liability for any misuse of this software or any violations of laws or terms of service.

Please ensure that your use of this tool adheres to ethical guidelines and respect the privacy and property rights of others.