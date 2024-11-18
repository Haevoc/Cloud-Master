import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart as mimem
from email.mime.text import MIMEText as mimet
from dotenv import load_dotenv
import os
from jinja2 import Environment, FileSystemLoader
import time
import sys
import logging
from flask import url_for 

BASE_DIR = r'F:/codes/cloud master/'
template_dir = os.path.join(BASE_DIR, 'templates')
log_dir = os.path.join(BASE_DIR, 'logs')

log_file=os.path.join(log_dir, 'email_sending.log')
# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),  # Logs to the file
        logging.StreamHandler()         # Logs to the console (VS Code terminal)
    ]
)

def send_emails(excel_file, template_path):
    # Load environment variables from .env file
    load_dotenv()

    # Read recipient names and emails from Excel (ensure correct path)
    df = pd.read_excel(excel_file)

    df = df.dropna(subset=['Email'])  # Remove rows where the email is NaN
    df['Email'] = df['Email'].astype(str)

    names = df['Name'].values
    emails = df['Email'].values

    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader(template_dir))
    template_file = os.path.basename(template_path)
    template = env.get_template(template_file)

    # Set up email configuration
    SenderAddress = "xyz@ailetechnology.in"
    password = os.getenv("EMAIL_PASSWORD")
    server = smtplib.SMTP_SSL("mail.ailetechnology.in", 465)  # Use SMTP_SSL for port 465

    # Login to the email server
    server.login(SenderAddress, password)

    # Loop through each name and corresponding email, and send email
    for name, email in zip(names, emails):
        # Render the template with dynamic data
        data = {
            'name': name,
            'email' : email,
            'url_for': url_for
        }
        html_content = template.render(data)


        # Prepare email message
        msg = mimem("alternative")
        msg['From'] = SenderAddress
        msg['To'] = email
        msg['Subject'] = "Our Product Showcase(test)"

        # Attach the HTML content as MIMEText
        msg.attach(mimet(html_content, "html"))

        # Request read receipt
        msg.add_header('Disposition-Notification-To', 'xyz@ailetechnology.in')

        try:
            # Send the email
            server.sendmail(SenderAddress, email, msg.as_string())
            logging.info(f'Email sent to {name} at {email}')
            # print(f'Email sent to {name} at {email}')
        except Exception as e:
            logging.error(f'Failed to send email to {name} at {email}: {e}')
        time.sleep(30)

    # Quit the server
    server.quit()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: python send_emails.py <excel_file> <template_file>")
    else:
        excel_file = sys.argv[1]
        template_path = sys.argv[2]
        send_emails(excel_file, template_path)

