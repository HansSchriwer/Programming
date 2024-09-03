### Step 1: Install Required Libraries
# First, ensure you have Python installed, and then install any required libraries using `pip`:

! pip install schedule
### Step 2: Create the Email Sending Script

import smtplib
import os
import schedule
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_email():
    # Email configuration
    sender_email = "your_email@example.com"
    receiver_email = "receiver_email@example.com"
    subject = "Daily Report"
    body = "Please find the daily report attached."

    # Email credentials
    smtp_server = "smtp.example.com"
    smtp_port = 587  # or 465 for SSL
    sender_password = os.getenv('EMAIL_PASSWORD')  # Store your email password as an environment variable

    # Email setup
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach the email body
    msg.attach(MIMEText(body, 'plain'))

    # Attach a file (optional)
    filename = "report.pdf"
    attachment_path = "/path/to/your/report.pdf"
   
    with open(attachment_path, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )
        msg.attach(part)

    # Sending the email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

# Schedule the script to run daily at a specific time
schedule.every().day.at("9:00").do(send_email)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(60)

### Step 3: Set Up the Script

1. **Email Configuration**: Replace `your_email@example.com` and `receiver_email@example.com` with the appropriate email addresses. Replace `smtp.example.com` with your SMTP server address, and adjust the `smtp_port` if necessary.

2. **Email Credentials**: Store your email password in an environment variable (`EMAIL_PASSWORD`) for security. You can set this in your terminal or in the environment where the script will run:
   ```bash
   export EMAIL_PASSWORD='your_email_password'
   ```

3. **Attachment**: If you have a report to attach, update the `filename` and `attachment_path` with the correct file name and path.

4. **Scheduling**: The script is set to send the email daily at 9:00 AM (`schedule.every().day.at("9:00")`). You can change the time to suit your needs.

### Step 4: Running the Script
You can run the script manually by executing it:

python send_daily_report.py

### Step 5: Automating the Script Execution
To automate the script execution daily without manual intervention:

1. **Linux/Unix**: Use `cron` jobs.
   - Edit the cron jobs list with `crontab -e` and add:
     ```bash
     0 9 * * * /usr/bin/python3 /path/to/send_daily_report.py
     ```

2. **Windows**: Use Task Scheduler.
   - Create a new task that triggers daily at the desired time and runs the Python script.

### Explanation:

- **smtplib.SMTP**: Used to connect to your email server and send emails.
- **MIMEText**: Formats the body of the email.
- **MIMEBase**: Handles file attachments.
- **schedule**: A simple job scheduling library for Python that allows you to schedule tasks.

This setup will ensure your daily reports are sent automatically at the scheduled time without requiring manual intervention.
