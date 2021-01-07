const stockxAPI = require('stockx-api');
const stockX = new stockxAPI({
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1'
});

stockX.fetchProductDetails('https://stockx.com/supreme-motion-logo-tee-ss20-white')
    .then(product => console.log(product))
    .catch(err => console.log(`Error scraping product details: ${err.message}`));


// https://stockx.com/supreme-motion-logo-tee-ss20-white
// https://stockx.com/adidas-yeezy-boost-700-magnet