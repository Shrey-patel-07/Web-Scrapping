# Web Scrapping

This repository contains code snippets for various tasks related to data retrieval, web scraping, and API interactions.

## Task 1: Fetching Bybit data for BTCUSD

### Description:
Use the Bybit API to retrieve historical data for BTCUSD in 15-minute intervals from January 1st, 2021 to December 31st, 2022. Convert timestamps to IST timezone, set datetime as the DataFrame index, and calculate VWAP and MACD using the Pandas-TA library.

### Implementation:
- [Code File](task_1/main.py)
- Dependencies: Bybit API, Pandas-TA

## Task 2: Scraping option chain from NSE

### Description:
Scrape the NSE India website to extract option chain data for a given symbol and expiry date. Export the data to an Excel file.

### Implementation:
- [Code File](task_2/main.py)
- Dependencies: BeautifulSoup, requests, Pandas, openpyxl

## Task 3: Concurrently fetching data for multiple symbols

### Description:
Similar to Task 1 but for multiple symbols (BTCUSD, ETHUSD, BITUSD, SOLUSD, XRPUSD). Implement threading/multiprocessing for concurrent data retrieval.

### Implementation:
- [Code File](task_3/main.py)
- Dependencies: Bybit API, Pandas-TA, threading/multiprocessing

## Task 4: Fetching historical candle data from investing.com

### Description:
Retrieve historical candle data for a specified symbol, timeframe, and date range from investing.com without using browser automation tools.

### Implementation:
- [Code File](task_4/main.py)
- Dependencies: requests, Pandas

## Task 5: Programmatically logging in to kite.zerodha.com

### Description:
Find the URL, request type, and payload required for login. Create Python code using the requests module to log in, even with incorrect credentials.

### Implementation:
- [Code File](task_5/main.py)
- Dependencies: requests

## Task 6: Fetching dividend date information from boerse-frankfurt.de

### Description:
Extract dividend date information for a specified symbol from the Boerse Frankfurt website without using browser automation tools.

### Implementation:
- [Code File](task_6/main.py)
- Dependencies: requests, BeautifulSoup

## Task 7 & 8: Getting live order book data for BTCUSDT spot

### Description:
Utilize the Bybit WebSocket API to retrieve live order book data for BTCUSDT spot. Task 7 doesn't require running in the background, while Task 8 involves running it in a background thread using the threading module.

### Implementation:
- [Task 7 Code File](task_7/main.py)
- [Task 8 Code File](task_8/main.py)
- Dependencies: Bybit WebSocket API, threading


## Running the Code

1. Clone the repository.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Navigate to each task directory and execute the corresponding Python file.

## Notes
- Ensure proper API keys and credentials are provided where necessary.
- Review the documentation links provided for detailed information about APIs and web scraping methods.
