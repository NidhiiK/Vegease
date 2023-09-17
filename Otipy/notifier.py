# # notifier.py

# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

# def send_notification(subject, message):
#     from_email = "nidhi22inmas@gmail.com"
#     to_email = "kdhini2807@gmail.com"
#     password = "hhfaizgjcaqpsjwl"

#     msg = MIMEMultipart()
#     msg["From"] = from_email
#     msg["To"] = to_email
#     msg["Subject"] = subject

#     body = message
#     msg.attach(MIMEText(body, "plain"))

#     server = smtplib.SMTP("smtp.gmail.com", 587)
#     server.starttls()
#     server.login(from_email, password)
#     server.sendmail(from_email, to_email, msg.as_string())
#     server.quit()
    
# def send_test_notification():
#     subject = "Test Notification"
#     message = "This is a test notification. If you receive this, your notifier is working correctly!"
#     send_notification(subject, message)



import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_notification(subject, message_html, recipients):
    # Email configuration
    sender_email = 'nidhi22inmas@gmail.com'
    sender_password = 'hhfaizgjcaqpsjwl'
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587  # Port for Gmail SMTP

    # Create a multipart message
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = ', '.join(recipients)

    # Create an HTML message
    message = MIMEText(message_html, 'html')

    # Attach the HTML message to the email
    msg.attach(message)

    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)

        # Send the email
        server.sendmail(sender_email, recipients, msg.as_string())

        # Close the SMTP server
        server.quit()

        print("Email sent successfully.")
    except Exception as e:
        print(f"Email sending failed: {str(e)}")

# Usage example
if __name__ == "__main__":
    subject = "New Products Alert"
    recipients = ['kdhini2807@gmail.com']

    # Example table HTML (replace this with your actual table HTML)
    table_html = """
    <table border="1">
        <tr>
            <th>Product Name</th>
            <th>Original Price</th>
            <th>Discounted Price</th>
            <th>Discount</th>
        </tr>
        <tr>
            <td>Product 1</td>
            <td>$10.00</td>
            <td>$8.00</td>
            <td>20%</td>
        </tr>
        <tr>
            <td>Product 2</td>
            <td>$15.00</td>
            <td>$12.00</td>
            <td>20%</td>
        </tr>
    </table>
    """

    # Your message containing the table HTML
    message_html = f"<p>{table_html}</p>"

    # Send the email
    send_notification(subject, message_html, recipients)
