import requests
import pandas as pd
import pandas_ta as ta
from tqdm import tqdm
import threading
import warnings

warnings.filterwarnings("ignore")

# Define symbols for fetching data
symbols = {
    "BTCUSD": ("1609439400000", "1672425000000"),
    "ETHUSD": ("1609439400000", "1672425000000"),
    "SOLUSD": ("1648060200000", "1668749400000"),
    "XRPUSD": ("1609439400000", "1672425000000"),
    "BITUSD": ("1636396200000", "1672510500000")
}

# Define parameters for API request
category = "linear"
interval = "15"
chunk_size = 1000

# Function to fetch data for a symbol
def fetch_data(symbol, start_date, end_date):
    all_data = pd.DataFrame()
    iterations = (int(end_date) - int(start_date)) // (chunk_size * 15 * 60 * 1000)

    # Loop through chunks of data
    for i in tqdm(range(iterations + 1), desc=f'Fetching {symbol} data'):
        start = int(start_date) + (i * chunk_size * 15 * 60 * 1000)
        end = start + (chunk_size * 15 * 60 * 1000)

        if i == iterations:
            end = int(end_date)  # Adjust the end timestamp for the last chunk

        # Make API request
        url = f"https://api-testnet.bybit.com/v5/market/kline?category={category}&symbol={symbol}&interval={interval}&start={start}&end={end}&limit={chunk_size}"
        response = requests.get(url)

        if response.status_code == 200:
            # Process data and create DataFrame
            data = response.json()['result']['list']
            columns = ['datetime', 'open', 'high', 'low', 'close', 'volume', 'volume_quote']
            df = pd.DataFrame(data, columns=columns)

            numeric_cols = ['open', 'high', 'low', 'close', 'volume', 'volume_quote']
            df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

            df['datetime'] = pd.to_numeric(df['datetime'])
            df['datetime'] = pd.to_datetime(df['datetime'], unit='ms', utc=True)
            df['datetime'] = df['datetime'].dt.tz_convert('Asia/Kolkata')
            df.set_index('datetime', inplace=True)

            df.ta.vwap(append=True)
            df.ta.macd(append=True)

            # Concatenate data
            all_data = pd.concat([all_data, df])

            df = df.sort_index()  # Sort DataFrame by datetime index

    # Save the concatenated dataframe to CSV file
    file_name = f"{symbol}.csv"
    all_data.sort_index(inplace=True)
    all_data.to_csv(file_name)
    print(f'Data for {symbol} saved to CSV file ({file_name}).')

# Start threads for each symbol
threads = []
for symbol, dates in symbols.items():
    start_date, end_date = dates
    thread = threading.Thread(target=fetch_data, args=(symbol, start_date, end_date))
    threads.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()
