import email
import smtplib
import imaplib
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart


class EmailClient:
    def __init__(self, smtp, imap):
        self.smtp = smtp
        self.imap = imap

    def login(self, _login, _password):
        ms = smtplib.SMTP(self.smtp, 587)
        ms.ehlo()
        ms.starttls()
        ms.ehlo()
        ms.login(_login, _password)
        return ms

    def send_email(self, _from, _recipients, _subject, _message, _password):
        msg = MIMEMultipart()
        msg['From'] = _from
        msg['To'] = ', '.join(_recipients)
        msg['Subject'] = _subject
        msg.attach(MIMEText(_message))

        ms = self.login(_from, _password)
        ms.sendmail(_from, ms, _message.as_string())
        ms.quit()

    def receive_email(self, _login, _password, _folder, header=None):
        mail = imaplib.IMAP4_SSL(self.imap)
        mail.login(_login, _password)

        mail.list()
        mail.select(_folder)
        criterion = '(HEADER Subject "%s")' % header if header else 'ALL'
        result, data = mail.uid('search', None, criterion)
        assert data[0], 'There are no letters with current header'

        latest_email_uid = data[0].split()[-1]
        result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_string(raw_email)
        mail.logout()
        return email_message


if __name__ == '__main__':
    gmail_client = EmailClient('smtp.gmail.com', 'imap.gmail.com')
    gmail_client.send_email('login@gmail.com', ['vasya@email.com', 'petya@email.com'], 'Subject', 'qwerty')
    new_emails = gmail_client.receive_email('login@gmail.com', 'qwerty', 'inbox')
