from lxml import html
import requests
import re
import telebot
from html.parser import HTMLParser
import time

_base_ulr = 'https://www.binance.com'
_url = 'https://www.binance.com/en/support/announcement/c-48';
# symbols_filter =

_api_key_binance = ''
_api_base_endpoint = 'https://api.binance.com'

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.my_links = []
        self.current_link = '/en/support/announcement/02895f23b535433e8563175cfb64d1cd'

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    href = attr[1]
                elif attr[0] == 'class':
                    if attr[1] == 'css-1ej4hfo':
                        self.my_links.append(href)

    def handle_endtag(self, tag):
        pass
        # print("Encountered an end tag :", tag)

    def handle_data(self, data):
        pass
 #       print("Encountered some data  :", data)


parser = MyHTMLParser()


def get_last_listings():

    page = requests.get(_url)
    coins = []

    parser.feed(page.text)
    for page_link in parser.my_links:
        if page_link == parser.current_link:
            print('last')
            break
        article = requests.get(_base_ulr+page_link).content
        html_tree = html.fromstring(article)
        print(_base_ulr+page_link)
        elements = html_tree.xpath("//div/span[contains(.,'USDT') or contains(.,'BUSD')]")
        # elements = html_tree.xpath("//div[@class='css-3fpgoh']/span[text()='USDT']")
        print(elements)
        for el in elements:
            if el.text is not None:
                print(el.text)
                match = re.findall(r'(\w*[/](USDT|BUSD))', el.text)
                print(match)
                coins = coins + match
        #     # if match:
        #     #     print(match)
    parser.current_link = parser.my_links[0]
    return coins


bot = telebot.TeleBot("1565268143:AAEpgoYj70UcsYmcPMqGVQPMZLYrF_lel0E", parse_mode=None)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


# bot.polling()


# https://t.me/joinchat/RdZnChrQODGuV0jL https://t.me/coins_lisling_group
#url = "https://api.telegram.org/1565268143:AAEpgoYj70UcsYmcPMqGVQPMZLYrF_lel0E/sendMessage?chat_id=@coins_lisling_group&text=message"
#res = requests.post(url)


while True:
    time.sleep(60)
    new_coins = get_last_listings()
    print(new_coins)
    headers = {'X-MBX-APIKEY': _api_key_binance}
    for coin in new_coins:
        # curl -H "X-MBX-APIKEY: vmPUZE6mv9SD5VNHk4HlWFsOr6aKE2zvsw0MuIgwCIPy6utIco14y7Ju91duEh8A" -X POST 'https://api.binance.com/api/v3/order?symbol=LTCBTC&side=BUY&type=LIMIT&timeInForce=GTC' -d 'quantity=1&price=0.1&recvWindow=5000&timestamp=1499827319559&signature=0fd168b8ddb4876a0358a8d14d0c9f3da0e9b20c5d52b2a00fcf7d1c602f9a77'
        res = requests.get(_api_base_endpoint+'/api/v3/ticker/price?symbol={}'.format(coin[0].replace('/', '')))
        print(res.json())
        message = coin[0]+'\n' + res.json()['price']
        bot.send_message('-1001171678986', message)

