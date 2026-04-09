import time 
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask
import threading

def send_mail():
    me = "ajay.raj.635p@gmail.com"
    you = "ajayraj.code@gmail.com"

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Link"
    msg['From'] = "me@gmail.com"
    msg['To'] = you
    
    text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
    html = f"""
    <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Document</title>
            <style>
                body{{font-size: 18px;}}
                #parent{{margin: auto;
                    width: 500px;
                    padding: 10px;   
                    height: 550px;}}
                .button-18 {{align-items: center;
                background-color: #0A66C2;
                border: 0;
                border-radius: 100px;
                box-sizing: border-box;
                color: #ffffff;
                cursor: pointer;
                display: inline-flex;
                font-family: -apple-system, system-ui, system-ui, "Segoe UI", Roboto, "Helvetica Neue", "Fira Sans", Ubuntu, Oxygen, "Oxygen Sans", Cantarell, "Droid Sans", "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Lucida Grande", Helvetica, Arial, sans-serif;
                font-size: 16px;
                font-weight: 600;
                justify-content: center;
                line-height: 20px;
                max-width: 480px;
                min-height: 40px;
                min-width: 0px;
                overflow: hidden;
                padding: 0px;
                padding-left: 20px;
                padding-right: 20px;
                text-align: center;
                touch-action: manipulation;
                transition: background-color 0.167s cubic-bezier(0.4, 0, 0.2, 1) 0s, box-shadow 0.167s cubic-bezier(0.4, 0, 0.2, 1) 0s, color 0.167s cubic-bezier(0.4, 0, 0.2, 1) 0s;
                user-select: none;
                -webkit-user-select: none;
                vertical-align: middle;}}
                
                .button-18:hover,
                .button-18:focus {{background-color: #16437E;
                color: #ffffff;}}
                
                .button-18:active {{background: #09223b;
                color: rgb(255, 255, 255, .7);}}
                
                .button-18:disabled {{cursor: not-allowed;
                background: rgba(0, 0, 0, .08);
                color: rgba(0, 0, 0, .3);}}
            
            </style>
        </head>
        <body>
            <div id="parent">
                <p>Hi,</p>
                <p>To procedd further with your registration process please enter the otp</p>
                
                <h1 style="text-align: center;">Hello Dear</h1>  
                <br>
                <p style="text-align: center;">B C A link is avialable</p>
        

                <br><br>
                <p style="text-align: center; color: darkviolet;">ajay.raj.635p@gmail.com</p>
                <p style="text-align: center; font-weight: bold; margin-bottom: 0px;">Cheers</p>
                <p style="text-align: center; margin-top: 0px;">About Chouhan Gaming</p>
                <script>
                    function copy()/{{
                        var copyText = document.getElementById("otp").innerText;
                        navigator.clipboard.writeText(copyText);
                    }}
                </script>
            </div>
        </body>
        </html>

    """

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    msg.attach(part1)
    msg.attach(part2)
    mail = smtplib.SMTP('smtp.gmail.com', 587)

    # mail.ehlo()

    # mail.starttls()

    # mail.login('ajay.raj.635p@gmail.com', 'nikn dgxq qmqh raal')
    # s = mail.sendmail(me, you, msg.as_string())
    # print(s)

    try:
        # Use 'with' to ensure the connection closes properly
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.set_debuglevel(0) # This will show you the "chat" between Python and Google
            server.starttls() 
            server.login(me, "nikn dgxq qmqh raal")
            server.sendmail(me, you, msg.as_string())
            print("\n✅ Success: Message sent!")
            
    except smtplib.SMTPAuthenticationError:
        print("\n❌ Error: Gmail rejected your login. Use an App Password!")
    except Exception as e:
        print(f"\n❌ Error: {e}")

    # mail.quit()


def scrape():
    try:
        respons = requests.get("https://results.jnvuiums.in/(S(vyelmdpjwhf24w3snjvglwta))/Results/ExamResultDeclare.aspx", timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(respons.text, 'html.parser')
        if respons.status_code == 200:
            print("Scraping successful!")
            bsc_links = soup.find_all('a', string=lambda text: 'B.Sc' in str(text))
            print(f"Found {bsc_links} B.C.A. links.")
            if bsc_links:
                print("B.C.A. link is avilable")
                send_mail()
            else:
                print("B.C.A. link is not avilable")
            
        else:
            print(f"Failed to scrape. Status code: {respons.status_code}")
    except requests.exceptions.Timeout:
        print("Request timed out. Retrying...")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

app = Flask(__name__)

@app.route('/')
def home():
    return "The scraper is running!"

def scrape_loop():
    while True:
        try:
            scrape() # Your existing function
        except Exception as e:
            print(f"Scrape Error: {e}")
        time.sleep(300)

# Start the background thread OUTSIDE the __main__ block
# This ensures it starts even when Gunicorn runs the file
threading.Thread(target=scrape_loop, daemon=True).start()

if __name__ == "__main__":
    # This part only runs when you run 'python main.py' locally
    app.run(host='0.0.0.0', port=10000, debug=False)
