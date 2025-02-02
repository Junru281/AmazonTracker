import requests
from bs4 import BeautifulSoup
import smtplib # mail protocol
import time


"""
Amazon Detected Automated Access and Gave back a CAPTCHA page
-> Ended up adding more headers
"""

URL = 'https://www.amazon.com/Sony-Full-frame-Mirrorless-Interchangeable-Lens-ILCE7M3K/dp/B07B45D8WV/ref=asc_df_B07B45D8WV?mcid=febb44fb68553612bf80b4d546842dd1&hvocijid=17393247122602671105-B07B45D8WV-&hvexpln=73&tag=hyprod-20&linkCode=df0&hvadid=721245378154&hvpos=&hvnetw=g&hvrand=17393247122602671105&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9018948&hvtargid=pla-2281435180938&th=1'

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.amazon.com/",
    "Connection": "keep-alive",
}

def check_price():

    page = requests.get(URL, headers=headers) # return all the data from that website
    soup = BeautifulSoup(page.content, 'html.parser')  # parse, so that we can pull out info
    # print(soup.prettify()) 

    title = soup.find(id = 'productTitle').get_text()
    print(title.strip())

    price = soup.find(class_ = 'a-price-whole').get_text()
    converted_price = float(price.replace(",", ""))
    print(converted_price)

    threshold = 1700.00
    if(converted_price < threshold):
        send_email()

    

def send_email(): 
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('junrujiang719@gmail.com', 'pjpf qxju qyxx obkd')
    subject = 'Price fell down!'
    body = f"Check the amazon link: {URL}"
    msg = f"Subject: {subject}\n\n {body}"

    server.sendmail(
        'junrujiang719@gmail.com',
        'junrujiang281@gmail.com',
        msg
    )
    print("Email has been sent!")

    server.quit()

while(True):
    check_price()
    time.sleep(60 * 60 * 2)