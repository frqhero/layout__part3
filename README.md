# Parse info and download books from tululu.org
The script allows its user to parse info and download books and its covers from [the website](https://tululu.org).

### Setup

1. Create venv
```console
python3 -m venv venv
```
2. Activate venv
```console
source venv/bin/activate
```
3. Install dependencies
```console
pip install -r requirements.txt
```
4. Run the script
```console
python3 main.py
```

### Parameters
The script accepts parameters that set a range of IDs for the script to work through.
Running it this way:
```python
python3 main.py
```
will cause it to run with the default parameters, namely 1 and 10. This means that the books with those IDs will be checked and downloaded.  
Similarly, if it is run like this:
```python
python3 main.py --start_id 10 --end_id 20
```
the script will iterate through the range of IDs from 10 to 20 inclusively.

### Parsing the sci-fi category
The repository has another script which allows you to download sci-fi books and their covers. It also has a set of acceptable parameters.
The script's main task is to iterate through pages of the category, parsing each book on every page. It retrieves the link to download the corresponding text file and the associated image for each book.
```python 
python3 parse_tululu_category.py
```
Please consider using parameters to customize the script's behavior.  
* `--start_page` - choose a value from 1 to 701. If no value is provided, the default starting page for iteration will be 1.  
* `--end_page` - choose a value from 1 to 701. If no value is provided, the default end page for iteration will be 701.  
* `--dest_folder /Users/username` - allows you to specify the directory where you want your results to be saved. By default, the script will use the current directory for saving the results.  
* `--skip_imgs` - if specified, the script will skip the image downloading process.  
* `--skip_txt` - if specified, the script will skip the txt files downloading process.  
* `--json_path /Users/username/dev` - allows you to independently set the file path for the JSON description output..