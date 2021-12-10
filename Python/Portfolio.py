from pycoingecko import CoinGeckoAPI

# Wallet Crypto
class Portfolio:
    fees = 0
    wallet = {}
    walletName = ""
    walletCurr = ""
    walletCoin = ""
    walletInve = 0
    walletSold = 0
    walletInit = ""
    walletTokenNumber = 0
    walletTransactionFees = 0

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
        self.wallet['Profits'] = self.walletSold
        self.wallet['Currencie'] = self.walletCurr
        self.wallet['TokenNumber'] = self.walletTokenNumber
        self.wallet['TransactionFees'] = self.walletTransactionFees


    # --- Add Coin to Wallet --- #
    def initCoinToWallet(self):
        price = self.getCoinPrice()
        self.walletTokenNumber = (self.walletInve - self.fees) / price[self.walletCoin][self.walletCurr]
        self.walletTransactionFees += self.fees


    # --- Get Coin Price Now --- #
    def getCoinPrice(self):
        price = self.coinApi.get_price(ids = self.walletCoin, vs_currencies = self.walletCurr)
        return price


    # --- Transaction Buy Coin --- #
    def buyCoinTransaction(self, amount):
        price = self.getCoinPrice()
        token = (amount - self.fees) / price[self.walletCoin][self.walletCurr]
        self.walletInve += amount - self.fees
        self.walletTokenNumber += token
        self.walletTransactionFees += self.fees
        self.initWallet()


    # --- Transaction Sell Coin --- #
    def sellCoinTransaction(self, percent):
        price = self.getCoinPrice()
        soldToken = self.walletTokenNumber * percent / 100
        benef = round(soldToken * price[self.walletCoin][self.walletCurr], 2)
        self.walletSold += benef - self.fees
        self.walletTokenNumber -= soldToken
        self.walletTransactionFees += self.fees
        self.initWallet()
        return benef


    # --- Global Value Wallet --- #



    # --- Getters --- #
    def getWallet(self):
        return self.wallet

    def getWalletValue(self):
        price = self.getCoinPrice()
        return round(self.walletTokenNumber * price[self.walletCoin][self.walletCurr], 2)

    # --- Setters --- #
    def setMoreCoin(self, invest):
        price = self.getCoinPrice()
        token = (invest - self.fees) / price[self.walletCoin][self.walletCurr]
        self.walletInve += invest
        self.walletTokenNumber += token
        self.walletTransactionFees += self.fees
        self.initWallet()


# Test wallet
# walletBtc = Portfolio('Wallet_BTC', 'bitcoin', 'BTC', 100, 'usd')
# btc = walletBtc.getWallet()
# print(btc)
#
# walletLuna = Portfolio('Wallet_LUNA', 'terra-luna', 'LUNA', 100, 'usd')
# luna = walletLuna.getWallet()
# print(luna)

walletAvax = Portfolio('Wallet_AVAX', 'avalanche-2', 'AVAX', 100, 'usd')
print(walletAvax.getWallet())

walletAvax.buyCoinTransaction(100)
print(walletAvax.getWallet())

print(walletAvax.getWalletValue())

print(walletAvax.sellCoinTransaction(25))
print(walletAvax.getWallet())

print(walletAvax.sellCoinTransaction(50))
print(walletAvax.getWallet())

print(walletAvax.sellCoinTransaction(100))
print(walletAvax.getWallet())



#


# # --- Add Fees Transaction --- #
# def calculFeesTransation(self):
#     return 0






#
