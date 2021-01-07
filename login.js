const stockxAPI = require('stockx-api');
const stockX = new stockxAPI({
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
});

(async () => {
    try {
        console.log('Logging in...');

        //Logs in using account email and password
        await stockX.login({
            user: 'mr.pigofpie@gmail.com',
            password: 'Data3248'
        });

        console.log('Successfully logged in!');


        stockX.fetchProductDetails('https://stockx.com/supreme-motion-logo-tee-ss20-white')
            .then(product => console.log(product.variants))
            .catch(err => console.log(`Error scraping product details: ${err.message}`));

        // //Returns an array of products
        // const productList = await stockX.searchProducts('yeezy');

        // //Fetch variants and product details of the first product
        // const product = await stockX.fetchProductDetails(productList[0]);

        // console.log('Placing an ask for ' + product.name);

        // //Places an ask on that product
        // const ask = await stockX.placeAsk(product, {
        //     amount: 5000000000,
        //     size: '9.5'
        // });

        // console.log('Successfully placed an ask for $5000 for ' + product.name);

        // //Updates the previous ask
        // await stockX.updateAsk(ask, {
        //     amount: 600000
        // });

        // console.log('Updated previous ask!');
    }
    catch (e) {
        console.log('Error: ' + e.message);
    }
})();