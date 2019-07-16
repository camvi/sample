from twilio.rest import Client
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
from config import email_options, twilio_options

class Notify:
    def __init__(self):
        self.email_options = email_options
        self.twilio_options = twilio_options
        pass

    def send_email(self, subj, html, files=None):
        try:
            fromaddr = self.email_options['from_addr']
            fromaddr_password = self.email_options['from_addr_password']
            toaddr = self.email_options['to_addr']
            msg = MIMEMultipart()
            msg['From'] = fromaddr
            msg['To'] = toaddr
            msg['Subject'] = subj
            msg.attach(MIMEText(html.encode('utf-8'), 'html', 'utf-8'))


            if files is not None:
                part = MIMEApplication(open(files).read())
                part.add_header('Content-Disposition','attachment; filename="%s"' % os.path.basename(files))
                msg.attach(part)

            text = msg.as_string()

            if self.email_options['ssl']:
                context = ssl.create_default_context()
                server = smtplib.SMTP_SSL(self.email_options['smtp_server'], self.email_options['smtp_port'], context=context)
            else:
                server = smtplib.SMTP(self.email_options['smtp_server'], self.email_options['smtp_port'])
            server.set_debuglevel(1)
            server.login(fromaddr, fromaddr_password)
            server.sendmail(fromaddr, toaddr, text)

            # server.ehlo()
            # server.starttls()
            # server.quit()
            print('EMAIL SENT!')
        except Exception as e:
            print(e)
            pass

    def send_text(self, msg, image_url=None):
        try:
            client = Client(self.twilio_options['sid'], self.twilio_options['token'])
            message = client.messages.create(
                                          body= msg,
                                          from_= self.twilio_options['phone'],
                                          to="+" + self.twilio_options['to_phone']
                                          # media_url=str(image_url)
                                      )
            print('SMS ' + str(message.status))
        except Exception as e:
            print(e)
            pass
