import requests

version = '0.0.1'
stable = True

class SyncClient:
    def __init__(self) -> None:
        self.cookies = None
        self.renew_cookies()

    def renew_cookies(self):
        r = requests.get("https://aqms.doe.ir/Home/LoadAQIMap?")
        self.cookies = r.cookies

    def fetch_station(self,id: int, renew_cookies=True):
        if renew_cookies:
            self.renew_cookies()

        r = requests.get(f'https://aqms.doe.ir/Home/LoadAQIMap?id={id}', cookies=self.cookies)
        return r.json()
    
    def fetch_all_stations(self):
        D = []
        T = None
        for i in [1, 2]:
            data = self.fetch_station(i,False)
            T = data['T']
            D.extend(data['D'])
        return D

    def fetch_all_city_stations(self, city:str, data:dict|None=None):
        if data == None:
            data = self.fetch_all_stations()
        
        return list(filter(lambda x: city in x['R'], data))
    
    def fetch_all_regions(self, date: str = "1404/12/08 11:00", type_: int = 2, session_id: str = None) -> dict:
        
        url = "https://aqms.doe.ir/Home/GetAQIDataByRegion/"

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://aqms.doe.ir',  
            'Sec-GPC': '1',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'TE': 'trailers',
        }
        session = requests.Session()
        
        cookies = {'AspxAutoDetectCookieSupport': '1'}
        if session_id:
            cookies['ASP.NET_SessionId'] = session_id
        session.cookies.update(cookies)

        payload = f"Date={date.replace(' ', '+')}&type={type_}"
        
        try:
            response = session.post(
                url, 
                headers=headers, 
                data=payload,  
                timeout=30
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
        except ValueError:
            return {"raw_response": response.text}
        finally:
            session.close()
    
    def fetch_state_aqi_data(self, state:str, data:None|dict=None, names_are_farsi=True):
        if not data:
            data = self.fetch_all_regions()
        
        return list(filter(lambda x: x['StateName_Fa' if names_are_farsi else 'StateName_En'].strip().lower() == state.strip().lower(), data['Data']))
    
    def fetch_city_aqi_data(self, city:str, data:None|dict=None, names_are_farsi=True):
        if not data:
            data = self.fetch_all_regions()
        
        return list(filter(lambda x: x['Region_Fa' if names_are_farsi else 'Region_En'].strip().lower() == city.strip().lower(), data['Data']))
