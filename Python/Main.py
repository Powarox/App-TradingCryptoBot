from time import sleep
from pycoingecko import CoinGeckoAPI

from Class.Portfolio import Portfolio
from Class.RepeatedTimer import RepeatedTimer


# # Création d'un wallet
# walletLuna = Portfolio('Wallet_LUNA', 'terra-luna', 'LUNA', 100, 'usd')
#
# # Action Buy & Sell
# walletLuna.sellCoinTransaction(25)
# walletLuna.buyCoinTransaction(100)
#
# # Affichage
# print(walletLuna.getWallet())



# Fonction à répéter
def fun1():
    coinApi = CoinGeckoAPI()
    result = coinApi.get_price(ids = 'terra-luna', vs_currencies = 'usd')
    print(result['terra-luna']['usd'])
    print(result)

fun1()


# # Running Program Time
# repeatedTimer1 = RepeatedTimer(20, fun1)
#
#
# try:
#     sleep(120)
# finally:
#     repeatedTimer1.stop()
















#
