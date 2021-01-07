const supremeCommunity = require("supreme-community-api");

supremeCommunity()
    .then((items) => console.log(items)) // [{name: 'Box Logo', price: '$50', image: 'http://'}, ...]
    .catch((err) => console.log(err));

