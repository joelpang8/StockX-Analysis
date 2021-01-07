def log(t):
    ts = datetime.now().strftime('%H:%M:%S')
    print('{} :: {}'.format(ts, t))


def main():
    print("""
   ____             _                   _   
  / __ \   ___   __| | ____ __ _  _ __ | |_ 
 / / _` | / _ \ / _` ||_  // _` || '__|| __|
| | (_| ||  __/| (_| | / /| (_| || |   | |_ 
 \ \__,_| \___| \__,_|/___|\__,_||_|    \__|
  \____/                                    
    
      === Stockx Sales Downloader ===
    """)

    d = Downloader(EMAIL, PASSWORD)
    d.start()


class Downloader(threading.Thread):
    def __init__(self, username, password):
        threading.Thread.__init__(self)
        self.username = username
        self.password = password
        self.S = requests.Session()
        self.S.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'content-type': 'application/json'
        }
        self.S.verify = False
        self.rawsales = {}
        self.sales = {'sales': []}
        self.customer_id = 0

    def login(self):
        log('Logging into {}'.format(self.username))

        r = self.S.request(
            method='post',
            url='https://stockx.com/api/login',
            json={"email": self.username, "password": self.password}
        )
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            log('Login failed [{}] :: {}'.format(r.status_code, r.json()['Error']['description']))
            return False
        log('Successfully logged in')
        j = r.json()
        self.customer_id = j['Customer']['id']
        self.S.headers['jwt-authorization'] = r.headers['jwt-authorization']
        print(r.headers['jwt-authorization'])
        return True

    def get_sales(self):
        log('Retrieving sales history')

        r = self.S.request(
            method='get',
            url='https://stockx.com/api/customers/{}/selling/history'.format(self.customer_id),
            params={
                'sort': 'matched_with_date',
                'order': 'DESC',
                'limit': '10000',
                'page': '1'
            }
        )
        try:
            j = r.json()
        except json.decoder.JSONDecodeError:
            log('Sale history retrieval failed [{}]'.format(r.status_code))
            return False
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            log('Sale history retrieval failed [{}] : {}'.format(r.status_code, j['error']))
            return False
        self.rawsales = j
        log('Retrieved {} sales'.format(len(self.rawsales['PortfolioItems'])))
        return True

    def clean_sales(self):
        log('Cleaning up sales before writing to file')
        for i in range(0, len(self.rawsales['PortfolioItems'])):
            self.sales['sales'].append({
                'Sale Date': self.rawsales['PortfolioItems'][i]['matchedWithDate'],
                'Order Number': self.rawsales['PortfolioItems'][i]['orderNumber'],
                'Product Name': self.rawsales['PortfolioItems'][i]['product']['title'],
                'Size': self.rawsales['PortfolioItems'][i]['product']['shoeSize'],
                'Price': '$' + str(self.rawsales['PortfolioItems'][i]['amount'])
            })
            log('{} | {} | {} | {} | {}'.format(
                self.rawsales['PortfolioItems'][i]['matchedWithDate'],
                self.rawsales['PortfolioItems'][i]['orderNumber'],
                self.rawsales['PortfolioItems'][i]['product']['title'],
                self.rawsales['PortfolioItems'][i]['product']['shoeSize'],
                self.rawsales['PortfolioItems'][i]['amount']
            ))

        return True

    def write_sales(self):
        log('Writing sales to sales.csv')
        with open('sales.csv', 'w') as csvfile:
            fieldnames = ['Sale Date', 'Order Number', 'Product Name', 'Size', 'Price']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for i in range(0, len(self.sales['sales'])):
                writer.writerow(self.sales['sales'][i])

    def run(self):
        if not self.login():
            exit(-1)

        if not self.get_sales():
            exit(-1)

        self.clean_sales()
        self.write_sales()

if __name__ == '__main__':
    main()