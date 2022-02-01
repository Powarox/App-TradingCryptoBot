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

final = ['swissborg', 'the-graph', 'ripple', 'polkadot', 'chiliz', 'matic-network', 'mimo-parallel-governance-token', 'enjincoin', 'Uniswap', 'republic-protocol', 'utrust', 'kyber-network', 'chainlink', 'audiocoin', 'binancecoin', 'aave', 'compound-usdt', 'qtum', 'lisk', 'tron', 'cosmos', 'eos', 'icon', 'ethereum-classic', 'cardano', 'kava', 'stellar', 'vechain', 'bittorrent-2', 'ankr', 'zilliqa', 'pancakeswap-token', 'theta-token']

# Get listCoin price & marketcap
print(' --- Coin Price --- ')
result = coinApi.get_price(ids = 'bittorrent-2', vs_currencies = 'usd', include_symbol = 'true')
print(result)


# test = coinApi.get_coin_by_id('bitcoin')
# print(test)

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
