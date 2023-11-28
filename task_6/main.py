import csv

class BF4PyConnector():
    def __init__(self, salt: str=None):
        import requests, re
        
        self.session = requests.Session()
        
        self.session.headers.update({'authority': 'api.boerse-frankfurt.de', 
                                     'origin': 'https://www.boerse-frankfurt.de',
                                     'referer': 'https://www.boerse-frankfurt.de/',})
        
        if salt is None:
            # Step 1: Get Homepage and extract main-es2015 Javascript file
            response = self.session.get('https://www.boerse-frankfurt.de/')
            if response.status_code != 200:
                raise Exception('Could not connect to boerse-frankfurt.de')
            file = re.findall('(?<=src=")main\.\w*\.js', response.text)
            if len(file) != 1:
                raise Exception('Could not find ECMA Script name')
            
            # Step 2: Get Javascript file and extract salt
            response = self.session.get('https://www.boerse-frankfurt.de/'+file[0])
            if response.status_code != 200:
                raise Exception('Could not connect to boerse-frankfurt.de')
            salt_list = re.findall('(?<=salt:")\w*', response.text)
            if len(salt_list) != 1:
                raise Exception('Could not find tracing-salt')
            self.salt = salt_list[0]
        else:
            self.salt = salt
   
    def __del__(self):
        self.session.close()
   
    def _create_ids(self, url):
        import hashlib
        from datetime import datetime
        timeutc = datetime.utcnow()
        timelocal = datetime.now()
        timestr = timeutc.isoformat(timespec='milliseconds') + 'Z'

        traceidbase = timestr + url + self.salt
        encoded = traceidbase.encode()
        traceid = hashlib.md5(encoded).hexdigest()

        xsecuritybase = timelocal.strftime("%Y%m%d%H%M") 
        encoded = xsecuritybase.encode()
        xsecurity = hashlib.md5(encoded).hexdigest()
        
        return {'client-date':timestr, 'x-client-traceid':traceid, 'x-security':xsecurity}
    
    
    
    def _get_data_url(self, function: str, params:dict):
        import urllib
        baseurl = "https://api.boerse-frankfurt.de/v1/data/"
        p_string = urllib.parse.urlencode(params)
        return baseurl + function + '?' + p_string

    
    def data_request(self, function: str, params: dict):
        import json
        
        url = self._get_data_url(function, params)
        header = self._create_ids(url)
        header['accept'] = 'application/json, text/plain, */*'
        req = self.session.get(url, headers=header, timeout=(3.5, 15))
        
        if req.text is None:
            raise Exception('Boerse Frankfurt returned no data, check parameters, especially period!')
        
        data = json.loads(req.text)
        
        if 'messages' in data:
            raise Exception('Boerse Frankfurt did not process request:', *data['messages'])
        
        return data
    
    def _get_search_url(self, function: str, params:dict):
        import urllib
        baseurl = "https://api.boerse-frankfurt.de/v1/search/"
        p_string = urllib.parse.urlencode(params)
        return baseurl + function + ('?' + p_string if p_string != '' else '')

    def search_request(self, function: str, params: dict):
        import json
        
        url = self._get_search_url(function, {})
        header = self._create_ids(url)
        header['accept'] = 'application/json, text/plain, */*'
        header['content-type'] = 'application/json; charset=UTF-8'
        req = self.session.post(url, headers=header, timeout=(3.5, 15), json=params)
        data = json.loads(req.text)
        
        return data


bf_connector = BF4PyConnector()
symbol = input("Enter the symbol: ")

dividend_params = {
    'isin': symbol  # Replace with the ISIN you're interested in
    # 'limit': 5  # Limit the number of results if needed
}

dividend_data = bf_connector.data_request('dividend_information', dividend_params)

csv_filename = f"{symbol}_dividend.csv"

with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Write header row
    writer.writerow(['Last dividend payment', 'Dividend cycle', 'Value', 'ISIN'])
    
    # Write data rows
    for item in dividend_data['data']:
        last_payment = item.get('dividendLastPayment', '')
        cycle = item['dividendCycle']['originalValue'] if 'dividendCycle' in item else ''
        value = f"{item.get('dividendValue', '')} {item.get('dividendCurrency', '')}"
        isin = item.get('dividendIsin', '')
        
        writer.writerow([last_payment, cycle, value, isin])


print(f"Data saved to {csv_filename}")