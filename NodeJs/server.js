const http = require("http");

const server = http.createServer(function(req, res) {

    //1. Import coingecko-api
    const CoinGecko = require('coingecko-api');

    //2. Initiate the CoinGecko API Client
    const CoinGeckoClient = new CoinGecko();

    //3. Make calls
    var func = async() => {
        let data = await CoinGeckoClient.ping();
        // let coin = await CoinGeckoClient.getPrice(ids = 'terra-luna', vs_currencies = 'usd');

        res.write(data);
    };
    func()

    res.end();
})

// Lancer le serveur
server.listen(3000)
