# https://github.com/man-c/pycoingecko
from pycoingecko import CoinGeckoAPI


# Instanciation Api
coinApi = CoinGeckoAPI()


# Mes liste de coin
listCoin = ['bitcoin', 'ethereum', 'polkadot', 'avalanche-2', 'terra-luna']
listBlockchain = ['binancecoin', 'ripple', 'solana', 'matic-network', 'cosmos']
listCurrencies = ['usd', 'eur']


# Get listCoin price & marketcap
result = coinApi.get_price(ids = listCoin, vs_currencies = 'usd', include_market_cap = 'true')
print(result)



# Get listCoin
