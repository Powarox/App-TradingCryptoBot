# https://github.com/man-c/pycoingecko
import fear_and_greed
from pycoingecko import CoinGeckoAPI

# Instanciation Api
coinApi = CoinGeckoAPI()

# Mes liste de coin
listCoin = ['bitcoin', 'ethereum', 'polkadot', 'avalanche-2', 'terra-luna']
listBlockchain = ['binancecoin', 'ripple', 'solana', 'matic-network', 'cosmos']
listCurrencies = ['usd', 'eur']

# Get listCoin price & marketcap
print(' --- Coin Price --- ')
result = coinApi.get_price(ids = listCoin, vs_currencies = 'usd', include_market_cap = 'true')

# Affichage
for coin, price in result.items():
    print(coin + ' : ' + str(price['usd']) + '$')




# Fear And Greed Index
indexFAG = fear_and_greed.get()
print(' \n' + ' --- Fear And Greed Index --- ')
print(indexFAG[1] + ' : ' + str(indexFAG[0]))
print('date : ' + str(indexFAG[2]))
print(indexFAG)








#
