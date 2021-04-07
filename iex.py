import requests

#stock = iex.IEXStock(modules.IEX_API_KEY, symbol)
class IEXStock:

    def __init__(self, token, symbol):
        self.base_url = "https://cloud.iexapis.com/stable"
        self.token = token
        self.symbol = symbol

    def get_price(self):
        url = f"{self.base_url}/stock/{self.symbol}.../token={self.token}"
        r = requests.get(url_iex_price)
        return r.json()
