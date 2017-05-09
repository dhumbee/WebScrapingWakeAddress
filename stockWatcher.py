import sys, time
import requests, bs4
import threading, logging, smtplib

# constants
WAIT_INTERVAL = 120
SMTP_HOST = 'smtp.gmail.com'
SMTP_TLS_PORT = 587
LOG_FILE = 'stockPriceLog.txt'


def main():
    '''clear log, setup logging, log a start msg, retrieve list of stock symbols
        from cmd line, start up a thread for each stock listed, sleep to allow the
        stock prices to be logged, have user enter CTRL-C to stop'''

    open(LOG_FILE, 'w').close()
    logging.basicConfig(filename=LOG_FILE,
                        level=logging.INFO,
                        format=' %(asctime)s %(message)s ')
    logging.info("StockWatcher - start program")

    # stage 2 code here
    # Mary: check for arguments being there

    if len(sys.argv) < 2:
        print("No stocks entered")
        logging.info('No Stocks Entered')
        logging.info('StockWatcher - end program')
        sys.exit()

    stock_list = sys.argv[1:]

    for i in range(len(stock_list)):
        stock = stock_list[i].upper()
        print("Begin watch for " + stock)
        thread = threading.Thread(target=getQuote, args=(stock,))
        thread.start()

    time.sleep(5)

    input("\nHit CTRL-BREAK to stop recording.\n\n")
    logging.info("StockWatcher - end program")


def getQuote(symbol):
    # stage 3
    url = "https://www.google.com/finance?q=nasdaq:" + symbol

    # requests and beautifulsoup statements
    resp = requests.get(url)
    stocks = bs4.BeautifulSoup(resp.text, "html.parser")
    bs_elem = stocks.select_one("span.pr")

    if bs_elem is not None:
        price = bs_elem.getText()
        price = price.strip()
        prevPrice = price
    else:
        print("Symbol" + symbol + " not found.")
        # Mary: exit would be better
        # return
        sys.exit()

    text = "Start watching " + symbol + ": Price: " + price
    print(text)
    logging.info(text)

    # i = 0
    while True:
        try:
            # Mary: The loop needs to have accessing of the
            # stock website and parsing of Beatiful Soup

            resp = requests.get(url)
            stocks = bs4.BeautifulSoup(resp.text, "html.parser")
            bs_elem = stocks.select_one('span.pr')
            price = bs_elem.getText()
            price = price.strip()

            # price = prices[i%6]
            logging.info(symbol + "\t" + price)
            # i += 1

            if price != prevPrice:
                text = symbol + " now at " + price + \
                                " ; was " + prevPrice
                print(text)
                sendEmail(text)
                prevPrice = price

            time.sleep(WAIT_INTERVAL)

        except Exception:
            text = "Connection Problem with " + symbol
            print(text)

def sendEmail(msg):
    # stage 4
    smtpObj = smtplib.SMTP(SMTP_HOST, SMTP_TLS_PORT)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login("augierush@gmail.com", 'centralpark')
    smtpObj.sendmail("augierush@gmail.com", "dhummel.1210@gmail.com",
                     "Subject: StockWatcher update \n" + msg)
    smtpObj.quit()

    print("sendEmail: " + msg)

main()