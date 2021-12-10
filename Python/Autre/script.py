# https://github.com/man-c/pycoingecko
import fear_and_greed
from pycoingecko import CoinGeckoAPI
# from Portfolio import Portfolio


# walletAvax = Portfolio('Wallet_AVAX', 'avalanche-2', 'AVAX', 100, 'usd')
# print(walletAvax.getWallet())

# Instanciation Api
coinApi = CoinGeckoAPI()

# Mes liste de coin
listCoin = ['bitcoin', 'ethereum', 'polkadot', 'avalanche-2', 'terra-luna']
listBlockchain = ['binancecoin', 'ripple', 'solana', 'matic-network', 'cosmos']
listStableCoin = ['usd-coin', 'tether', 'terrausd']
listCurrencies = ['usd', 'eur']

# Get listCoin price & marketcap
print(' --- Coin Price --- ')
result = coinApi.get_price(ids = listCoin, vs_currencies = 'usd', include_market_cap = 'false')

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
