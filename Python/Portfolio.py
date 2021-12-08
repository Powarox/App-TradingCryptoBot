from pycoingecko import CoinGeckoAPI

# Wallet Crypto
class Portfolio:
    wallet = {}
    walletName = ""
    walletCurr = ""
    walletCoin = ""
    walletInve = 0
    walletInit = ""
    walletTokenNumber = 0

    # Instanciation Api
    coinApi = CoinGeckoAPI()

    # --- Constructor --- #
    def __init__(self, name, coin, initial, investie, currencie):
        self.walletName = name
        self.walletCoin = coin
        self.walletInit = initial
        self.walletInve = investie
        self.walletCurr = currencie
        self.initCoinToWallet()
        self.initWallet()

    # --- Initialisation --- #
    def initWallet(self):
        self.wallet['Name'] = self.walletName
        self.wallet['Coin'] = self.walletCoin
        self.wallet['Inital'] = self.walletInit
        self.wallet['Investie'] = self.walletInve
        self.wallet['Currencie'] = self.walletCurr
        self.wallet['TokenNumber'] = self.walletTokenNumber

    # --- Add Coin to Wallet --- #
    def initCoinToWallet(self):
        price = self.getCoinPrice()
        self.walletTokenNumber = self.walletInve / price[self.walletCoin][self.walletCurr]

    # --- Get Coin Price Now --- #
    def getCoinPrice(self):
        price = self.coinApi.get_price(ids = self.walletCoin, vs_currencies = self.walletCurr)
        return price

    # --- Add Fees Transaction --- #
    def calculFeesTransation(self):
        return 0

    # --- Getters --- #
    def getWallet(self):
        return self.wallet

    # --- Setters --- #
    def setMoreCoin(self, invest):
        price = self.getCoinPrice()


# Test wallet
walletBtc = Portfolio('Wallet_BTC', 'bitcoin', 'BTC', 100, 'usd')
btc = walletBtc.getWallet()
print(btc)

walletLuna = Portfolio('Wallet_LUNA', 'terra-luna', 'LUNA', 100, 'usd')
luna = walletLuna.getWallet()
print(luna)

walletAvax = Portfolio('Wallet_AVAX', 'avalanche-2', 'AVAX', 100, 'usd')
avax = walletAvax.getWallet()
print(avax)
