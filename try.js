const stockxAPI = require('stockx-api');
const stockX = new stockxAPI({
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1'
});

stockX.searchProducts('supreme', {
    limit: 5,
    dataType: "product"
})
    .then(products => console.log(products))
    .catch(err => console.log(`Error searching: ${err.message}`));