import requests
import pandas as pd
import numpy as np
import pandas_ta as ta
from tqdm import tqdm
import warnings

warnings.filterwarnings("ignore")

# Define symbol, category, interval, start and end dates
symbol = "BTCUSD"
category = "linear"
interval = "15"
start_date = "1609439400000"  # Start timestamp for 1st Jan 2021
end_date = "1672510500000"    # End timestamp for 31st Dec 2022

# Empty DataFrame to store concatenated data
all_data = pd.DataFrame()

# Set the chunk size (1000 per request)
chunk_size = 1000

# Calculate the number of iterations needed
iterations = (int(end_date) - int(start_date)) // (chunk_size * 15 * 60 * 1000)

for i in tqdm(range(iterations + 1), desc='Fetching data'):
    start = int(start_date) + (i * chunk_size * 15 * 60 * 1000)
    end = start + (chunk_size * 15 * 60 * 1000)

    if i == iterations:
        end = int(end_date)  # Adjust the end timestamp for the last chunk

    url = f"https://api-testnet.bybit.com/v5/market/kline?category={category}&symbol={symbol}&interval={interval}&start={start}&end={end}&limit={chunk_size}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()['result']['list']
        columns = ['datetime', 'open', 'high',
                   'low', 'close', 'volume', 'volume_quote']
        df = pd.DataFrame(data, columns=columns)

        # Convert necessary columns to numeric types
        numeric_cols = ['open', 'high', 'low',
                        'close', 'volume', 'volume_quote']
        df[numeric_cols] = df[numeric_cols].apply(
            pd.to_numeric, errors='coerce')

        # Convert 'datetime' column to datetime with IST timezone and set as index
        df['datetime'] = pd.to_numeric(df['datetime'])
        df['datetime'] = pd.to_datetime(df['datetime'], unit='ms', utc=True)
        df['datetime'] = df['datetime'].dt.tz_convert('Asia/Kolkata')
        df.set_index('datetime', inplace=True)

        # Add technical indicators (VMAP, MACD)
        df.ta.vwap(append=True)
        df.ta.macd(append=True)

        # Concatenate the dataframes
        all_data = pd.concat([all_data, df])

        # Sort the index
        df = df.sort_index()  # Sort DataFrame by datetime index

    else:
        print(f"Error in fetching data from API for chunk {i + 1}")


# Save the concatenated dataframe to CSV file 'BTCUSD.csv'
file_name = f"{symbol}.csv"
all_data.sort_index(inplace=True)
all_data.to_csv(file_name)
print(f'Data saved to CSV file {file_name}.')

# Save the concatenated dataframe to Excel file 'BTCUSD.xlsx'
all_data.index = all_data.index.tz_convert(None)
all_data.to_excel('BTCUSD.xlsx')
print('Data saved to Excel file (BTCUSD.xlsx).') 