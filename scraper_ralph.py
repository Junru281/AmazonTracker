import requests
from bs4 import BeautifulSoup
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time



URL = input("Enter your desired item at Ralph Lauren(Copy and Paste the URL): ")

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.ralphlauren.com/",
    "Connection": "keep-alive",
}
TARGET_SIZE = input("Enter your desired size: ").strip().upper()
TARGET_COLOR = input("Enter your desired color: ").strip()
INTERVAL = int(input("Enter the interval you want to wait between each check (Minutes): ").strip())


def check_restock():

    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    # print(soup.prettify()) 
    title = soup.find(class_='product-name').get_text().strip()
    # print(title.strip())
    imgsrc = soup.find("picture", class_="rlc-picture swiper-zoomable").get("data-highres-images")
    
    COLOR_CHECK = False
    SIZE_CHECK = False

    color_options = soup.find_all('a', class_='js-variation-link swatchanchor swatch')
    if color_options:
        for color in color_options:
            color_name = color.get("data-selected")
            if TARGET_COLOR == color_name:
                COLOR_CHECK = True
    
    if COLOR_CHECK: 
        size_unavailable = soup.find_all('li', class_='variations-attribute selectable out tooltip has-tooltip')
        SIZE_CHECK = True
        if size_unavailable: 
            for size in size_unavailable: 
                size_span = size.find_all('span', class_='attribute-value')
                if size_span:
                    for size_span_item in size_span:
                        size_name = size_span_item.get_text().strip()
                        if size_name == TARGET_SIZE:
                            SIZE_CHECK = False
                            
    
    if SIZE_CHECK and COLOR_CHECK:
        send_email(title=title, imgsrc=imgsrc)
    if not COLOR_CHECK: 
        print("Color is Not Available Now :(")
    if not SIZE_CHECK: 
        print("Size is Not Available Now :(")

    # notifymsg = soup.find(class_='product-not-available')
    # if not notifymsg:
    #     send_email(title)

def send_email(title, imgsrc):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login("junrujiang719@gmail.com", 'pjpf qxju qyxx obkd')
    subject = f"{title} {TARGET_SIZE} {TARGET_COLOR} Have Been Restock!"
    body = f"""
          <body>
            <h2 style="color: #333; font-family: Arial, sans-serif;">Hey!</h2>
            <p style="color: #555; font-family: Arial, sans-serif;">
              The following item is back in stock:
            </p>
            <ul style="color: #555; font-family: Arial, sans-serif;">
              <li><strong>Item:</strong> {title}</li>
              <li><strong>Size:</strong> {TARGET_SIZE}</li>
              <li><strong>Color:</strong> {TARGET_COLOR}</li>
            </ul>
            <p style="text-align: center;">
                <img src="{imgsrc}" style="width: 50%; display: block; margin: 0 auto;">
            </p>
            <p style="color: #555; font-family: Arial, sans-serif;">
              Buy it before it's gone! 🚀
            </p>
            <p style="color: #555; font-family: Arial, sans-serif;">
              <a href="{URL}" style="color: #1a73e8; text-decoration: none;">Check the link here</a>
            </p>
            <p style="color: #777; font-family: Arial, sans-serif; font-size: 12px;">
              This is an automated notification. Please do not reply to this email.
            </p>
          </body>
        """
    receiver = input("Enter whom are you sending the notification to: ")

    msg = MIMEMultipart()
    msg["From"] = "junrujiang719@gamil.com"
    msg["To"] = receiver
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "html"))


    server.sendmail(
        'junrujiang719@gmail.com',
        receiver,
        msg.as_string()
    )
    print("Email has been sent!")

    server.quit()

while(True):
    check_restock()
    print(f"Waiting for {INTERVAL} minutes before checking again...")
    time.sleep(INTERVAL * 60)
    quit = input("Do you want to stop tracking? Y or N ")
    if quit == "Y":
        print("Now you quit the tracking! Thanks for using it!")
        break
    
    
