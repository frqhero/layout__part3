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