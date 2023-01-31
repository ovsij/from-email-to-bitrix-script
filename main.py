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
    typ, data = imap.search(None, "UNSEEN", config.from_email)
    for num in data[0].split():
        try:
            result, data = imap.fetch(num, '(RFC822)')
            raw_email = data[0][1]
            raw_email_string = raw_email.decode()
            email_message = email.message_from_string(raw_email_string)
            
            bytes, encoding = email.header.decode_header(email_message['Subject'])[0]
            if bytes.decode(encoding) == 'Поступление на счет':
                if email_message.is_multipart():
                    print('Multipart: Yes')
                    for part in email_message.walk():
                        try:
                            text = part.get_payload(decode=True).decode('utf-8')
                        except:
                            continue
                        
                        #text = str(base64.b64decode(payload).decode('utf8'))
                        #print(text)
                string1 = 'На ваш счет ' + text.split('На ваш счет ')[-1].split(' Остаток')[0].replace('&quot;', '\"')
                string2 = 'Плательщик: ' + text.split('Плательщик: ')[-1].split('Счет:')[0].strip('<br>').replace('<br>', '').replace('&quot;', '\"')
                string3 = 'Назначение платежа: ' + text.split('Назначение платежа: ')[-1].split('С уважением')[0].strip('<br>').replace('<br>', '').replace('&quot;', '\"')
                message = {'DIALOG_ID': config.dialog_id,'MESSAGE': 'От кого: albo-no-reply@alfa-bank.info \n\n' + string1 + '\n\n' + string2 + '\n' + string3}
                request = requests.get(config.webhook + 'im.message.add', message)
                print(message)
                print(request.json())
        except Exception as e:
            print(e)
    imap.close()
    imap.logout()
    

if __name__ == '__main__':
    n = 1
    while n > 0:
        time.sleep(config.interval)
        main()
       