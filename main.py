import base64
import email
import email.parser
import imaplib
import requests
import time

import config

def main():
    mail_pass = config.mail_pass
    username = config.username
    imap = imaplib.IMAP4_SSL(config.imap_server, 993)
    imap.login(username, mail_pass)
    imap.select('INBOX')
    try:
        typ, data = imap.search(None, "UNSEEN", config.from_email)
        for num in data[0].split():
            result, data = imap.fetch(num, '(RFC822)')
            raw_email = data[0][1]
            raw_email_string = raw_email.decode()
            email_message = email.message_from_string(raw_email_string)
            msg_body = email_message.get_payload()
            text = str(base64.b64decode(msg_body).decode('utf8').replace('>', ''))
            string1 = 'На ваш счет ' + text.split('На ваш счет ')[-1].split(' Остаток')[0]
            string2 = 'Плательщик: ' + text.split('Плательщик: ')[-1].split('Счет:')[0]
            string3 = 'Назначение платежа: ' + text.split('Назначение платежа: ')[-1].split('С уважением')[0]
            message = {'POST_MESSAGE': string1 + '\n\n' + string2 + '\n' + string3, 'POST_TITLE': 'От кого: albo-no-reply@alfa-bank.info'}
            webhook = config.webhook
            request = requests.get(webhook + 'log.blogpost.add', message)
            print(request.json())
            imap.close()
            imap.logout()
    except:
        pass
    

if __name__ == '__main__':
    n = 1
    while n > 0:
        time.sleep(config.interval)
        main()
       