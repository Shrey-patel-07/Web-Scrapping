from datetime import datetime
import logging
import urllib
import requests
import json
import pandas as pd

log = logging.getLogger("root")

BASE_URL = "https://www.nseindia.com/"
INDICES = ["NIFTY", "FINNIFTY", "BANKNIFTY"]
OPTIONS_PRICE_INDICES = "api/option-chain-indices?"
OPTIONS_PRICE_EQUITIES = "api/option-chain-equities?"


def get_headers():
    """
    Args:
        ---\n
    Returns:\n
        Json: json containing nse header
    """

    return {
        "Host": "www.nseindia.com",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "X-Requested-With": "XMLHttpRequest",
        "DNT": "1",
        "Connection": "keep-alive",
    }


def get_cookies():
    """
    Args:
        ---

    Returns:

        Json: json containing nse cookies
    """

    response = requests.get(BASE_URL, timeout=30, headers=get_headers())
    if response.status_code != 200:
        raise ValueError("Retry again in a minute.")
    return response.cookies.get_dict()


symbols = [
    {
        "keys": ["NIFTY 50", "NIFTY50", "NIFTY"],
        "indices": "NIFTY 50",
        "derivatives": "NIFTY",
    },
    {
        "keys": ["NIFTY BANK", "NIFTYBANK", "BANKNIFTY"],
        "derivatives": "BANKNIFTY",
        "indices": "NIFTY BANK",
    },
    {
        "keys": ["NIFTY FINANCIAL SERVICES", "FINNIFTY", "NIFTY FIN SERVICE"],
        "derivatives": "FINNIFTY",
        "indices": "NIFTY FINANCIAL SERVICES",
    },
    {"keys": ["NIFTY NEXT 50"], "derivatives": "", "indices": "NIFTY NEXT 50"},
    {"keys": ["NIFTY MIDCAP 50"], "derivatives": "",
        "indices": "NIFTY MIDCAP 50"},
    {"keys": ["NIFTY MIDCAP 100"], "derivatives": "",
        "indices": "NIFTY MIDCAP 100"},
    {"keys": ["NIFTY MIDCAP 150"], "derivatives": "",
        "indices": "NIFTY MIDCAP 150"},
    {"keys": ["NIFTY SMALLCAP 50"], "derivatives": "",
        "indices": "NIFTY SMALLCAP 50"},
    {
        "keys": ["NIFTY SMALLCAP 100"],
        "derivatives": "",
        "indices": "NIFTY SMALLCAP 100",
    },
    {
        "keys": ["NIFTY SMALLCAP 250"],
        "derivatives": "",
        "indices": "NIFTY SMALLCAP 250",
    },
    {
        "keys": ["NIFTY MIDSMALLCAP 400"],
        "derivatives": "",
        "indices": "NIFTY MIDSMALLCAP 400",
    },
    {"keys": ["NIFTY 100"], "derivatives": "", "indices": "NIFTY 100"},
    {"keys": ["NIFTY 200"], "derivatives": "", "indices": "NIFTY 200"},
    {
        "keys": ["NIFTY500 MULTICAP 50:25:25"],
        "derivatives": "",
        "indices": "NIFTY500 MULTICAP 50:25:25",
    },
    {
        "keys": ["NIFTY LARGEMIDCAP 250"],
        "derivatives": "",
        "indices": "NIFTY LARGEMIDCAP 250",
    },
    {
        "keys": ["NIFTY MIDCAP SELECT"],
        "derivatives": "",
        "indices": "NIFTY MIDCAP SELECT",
    },
    {
        "keys": ["NIFTY TOTAL MARKET"],
        "derivatives": "",
        "indices": "NIFTY TOTAL MARKET",
    },
    {
        "keys": ["NIFTY MICROCAP 250"],
        "derivatives": "",
        "indices": "NIFTY MICROCAP 250",
    },
    {"keys": ["NIFTY AUTO"], "derivatives": "", "indices": "NIFTY AUTO"},
    {"keys": ["NIFTY ENERGY"], "derivatives": "", "indices": "NIFTY ENERGY"},
    {
        "keys": ["NIFTY FINANCIAL SERVICES 25/50"],
        "derivatives": "",
        "indices": "NIFTY FINANCIAL SERVICES 25/50",
    },
    {"keys": ["NIFTY FMCG"], "derivatives": "", "indices": "NIFTY FMCG"},
    {"keys": ["NIFTY IT"], "derivatives": "", "indices": "NIFTY IT"},
    {"keys": ["NIFTY MEDIA"], "derivatives": "", "indices": "NIFTY MEDIA"},
    {"keys": ["NIFTY METAL"], "derivatives": "", "indices": "NIFTY METAL"},
    {"keys": ["NIFTY PHARMA"], "derivatives": "", "indices": "NIFTY PHARMA"},
    {"keys": ["NIFTY PSU BANK"], "derivatives": "",
        "indices": "NIFTY PSU BANK"},
    {"keys": ["NIFTY REALTY"], "derivatives": "", "indices": "NIFTY REALTY"},
    {
        "keys": ["NIFTY PRIVATE BANK"],
        "derivatives": "",
        "indices": "NIFTY PRIVATE BANK",
    },
    {
        "keys": ["NIFTY HEALTHCARE INDEX"],
        "derivatives": "",
        "indices": "NIFTY HEALTHCARE INDEX",
    },
    {
        "keys": ["NIFTY CONSUMER DURABLES"],
        "derivatives": "",
        "indices": "NIFTY CONSUMER DURABLES",
    },
    {
        "keys": ["NIFTY OIL &amp; GAS"],
        "derivatives": "",
        "indices": "NIFTY OIL &amp; GAS",
    },
    {
        "keys": ["NIFTY DIVIDEND OPPORTUNITIES 50"],
        "derivatives": "",
        "indices": "NIFTY DIVIDEND OPPORTUNITIES 50",
    },
    {"keys": ["NIFTY50 VALUE 20"], "derivatives": "",
        "indices": "NIFTY50 VALUE 20"},
    {
        "keys": ["NIFTY100 QUALITY 30"],
        "derivatives": "",
        "indices": "NIFTY100 QUALITY 30",
    },
    {
        "keys": ["NIFTY50 EQUAL WEIGHT"],
        "derivatives": "",
        "indices": "NIFTY50 EQUAL WEIGHT",
    },
    {
        "keys": ["NIFTY100 EQUAL WEIGHT"],
        "derivatives": "",
        "indices": "NIFTY100 EQUAL WEIGHT",
    },
    {
        "keys": ["NIFTY100 LOW VOLATILITY 30"],
        "derivatives": "",
        "indices": "NIFTY100 LOW VOLATILITY 30",
    },
    {"keys": ["NIFTY ALPHA 50"], "derivatives": "",
        "indices": "NIFTY ALPHA 50"},
    {
        "keys": ["NIFTY200 QUALITY 30"],
        "derivatives": "",
        "indices": "NIFTY200 QUALITY 30",
    },
    {
        "keys": ["NIFTY ALPHA LOW-VOLATILITY 30"],
        "derivatives": "",
        "indices": "NIFTY ALPHA LOW-VOLATILITY 30",
    },
    {
        "keys": ["NIFTY200 MOMENTUM 30"],
        "derivatives": "",
        "indices": "NIFTY200 MOMENTUM 30",
    },
    {
        "keys": ["NIFTY MIDCAP150 QUALITY 50"],
        "derivatives": "",
        "indices": "NIFTY MIDCAP150 QUALITY 50",
    },
    {"keys": ["NIFTY COMMODITIES"], "derivatives": "",
        "indices": "NIFTY COMMODITIES"},
    {
        "keys": ["NIFTY INDIA CONSUMPTION"],
        "derivatives": "",
        "indices": "NIFTY INDIA CONSUMPTION",
    },
    {"keys": ["NIFTY CPSE"], "derivatives": "", "indices": "NIFTY CPSE"},
    {
        "keys": ["NIFTY INFRASTRUCTURE"],
        "derivatives": "",
        "indices": "NIFTY INFRASTRUCTURE",
    },
    {"keys": ["NIFTY MNC"], "derivatives": "", "indices": "NIFTY MNC"},
    {
        "keys": ["NIFTY GROWTH SECTORS 15"],
        "derivatives": "",
        "indices": "NIFTY GROWTH SECTORS 15",
    },
    {"keys": ["NIFTY PSE"], "derivatives": "", "indices": "NIFTY PSE"},
    {
        "keys": ["NIFTY SERVICES SECTOR"],
        "derivatives": "",
        "indices": "NIFTY SERVICES SECTOR",
    },
    {
        "keys": ["NIFTY100 LIQUID 15"],
        "derivatives": "",
        "indices": "NIFTY100 LIQUID 15",
    },
    {
        "keys": ["NIFTY MIDCAP LIQUID 15"],
        "derivatives": "",
        "indices": "NIFTY MIDCAP LIQUID 15",
    },
    {
        "keys": ["NIFTY INDIA DIGITAL"],
        "derivatives": "",
        "indices": "NIFTY INDIA DIGITAL",
    },
    {"keys": ["NIFTY100 ESG"], "derivatives": "", "indices": "NIFTY100 ESG"},
    {
        "keys": ["NIFTY INDIA MANUFACTURING"],
        "derivatives": "",
        "indices": "NIFTY INDIA MANUFACTURING",
    },
]


def get_symbol(symbol: str, get_key: str) -> str:
    """_summary_

    Args:
        symbol (str): _description_
        get_key (str): _description_

    Returns:
        str: _description_
    """

    symbol_map = symbols
    val = None
    for item in symbol_map:
        key_list = item["keys"]
        if symbol in key_list:
            val = item[get_key]

    return val if val else symbol


def fetch_url(url, cookies, key=None, response_type="panda_df"):
    """
    Args:

        url (str): URL to fetch
        cookies (str): NSE cookies
        key (str, Optional):

    Returns:

        Pandas DataFrame: df containing url data

    """

    response = requests.get(
        url=url,
        timeout=30,
        headers=get_headers(),
        cookies=cookies,
    )

    if response.status_code == 200:
        json_response = json.loads(response.content)

        if response_type != "panda_df":
            return json_response
        if key is None:
            return pd.DataFrame.from_dict(json_response)

        return pd.DataFrame.from_dict(json_response[key])

    raise ValueError("Please try again in a minute.")


def option_chain(
    data_json: str,
    response_type: str,
):
    """_summary_

    Args:
        data_json (str): _description_
        response_type (str): _description_

    Returns:
        _type_: _description_
    """
    if response_type == "json":
        data_json_ret = []
        for record in data_json:
            if "PE" in record:
                record["PE"].pop("strikePrice", None)
                record["PE"].pop("expiryDate", None)
                record["PE"].pop("underlying", None)
                record["PE"].pop("identifier", None)
            if "CE" in record:
                record["CE"].pop("strikePrice", None)
                record["CE"].pop("expiryDate", None)
                record["CE"].pop("underlying", None)
                record["CE"].pop("identifier", None)
            data_json_ret.append(record)
        return data_json_ret

    return (
        pd.json_normalize(data_json)
        .sort_values(by=["expiryDate", "strikePrice"], ascending=True)
        .drop(
            columns=[
                "PE.strikePrice",
                "PE.expiryDate",
                "PE.identifier",
                "CE.strikePrice",
                "CE.expiryDate",
                "CE.identifier",
            ]
        )
    )


def get_option_chain(
    symbol: str,
    strike_price: str = None,
    expiry_date: str = None,
    response_type="panda_df",
):

    params = {}
    cookies = get_cookies()
    base_url = BASE_URL
    symbol = get_symbol(symbol=symbol, get_key="derivatives")

    if symbol in INDICES:
        event_api = OPTIONS_PRICE_INDICES
    else:
        event_api = OPTIONS_PRICE_EQUITIES

    params["symbol"] = symbol

    url = base_url + event_api + urllib.parse.urlencode(params)
    data = fetch_url(url, cookies, response_type="json")

    if data is None or data == {}:
        log.error("symbol is wrong or unable to access API")
        raise ValueError

    # filtering data

    if strike_price and expiry_date:
        filtered_data = [
            record
            for record in data["records"]["data"]
            if record["strikePrice"] == strike_price
            and record["expiryDate"]
            == datetime.strptime(expiry_date, "%d-%m-%Y").strftime("%d-%b-%Y")
        ]

    elif strike_price:
        filtered_data = [
            record
            for record in data["records"]["data"]
            if record["strikePrice"] == strike_price
        ]
    elif expiry_date:
        filtered_data = [
            record
            for record in data["records"]["data"]
            if record["expiryDate"]
            == datetime.strptime(expiry_date, "%d-%m-%Y").strftime("%d-%b-%Y")
        ]
    else:
        filtered_data = data["records"]["data"]

    return option_chain(
        filtered_data,
        response_type=response_type,
    )


file_name = "data.csv"


data = get_option_chain(symbol="ADANIPORTS", expiry_date="28-12-2023") # dd-mm-yyyy


data.to_csv(file_name)
print(f'Data saved to CSV file {file_name}.')
