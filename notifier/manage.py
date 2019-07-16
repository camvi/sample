from Camvi import Camvi
from Notify import Notify
from config import twilio_options, email_options, camvi_options

#TODO: specify options in config file first

def main():
    camvi = Camvi(timeout=1)
    notify = Notify()
    # start listener
    camvi.listen()
    # retrieve camvi token
    camvi_tok = camvi.retrieve_auth_token()
    while True:
        # enable
        msg = camvi.event()
        print(msg)
        if msg['type'] != 'ADD':
            continue;
        persons = msg.get('persons')
        if persons is not None:
            for person in persons:
                onBlackList = False
                groups = person['groups']
                if groups is not None:
                    for group in groups:
                        if group['name'] == 'blacklist':
                            onBlackList = True

                if onBlackList:
                    print('Person on black list found!')
                    image_url = 'http://' + camvi_options['ip'] + ':' + camvi_options['port'] + '/log/image/' + str(person['log'])
                    # msg_to_send = "Person found, name: {}".format(str(person['name']))
                    # email
                    if email_options['enabled']:
                        msg_to_send = "<html><body>Black list person found, name {}, time {}, camera {}, <a href=\"{}\">picture</a></body></html>".format(str(person['name']), msg['time'], msg['camera'], image_url)
                        print (msg_to_send)
                        notify.send_email(subj="Black List Person Found", html=msg_to_send)
                    # text
                    if twilio_options['enabled']:
                        msg_to_send = "black list person found: {}, {}".format(str(person['name']), image_url)
                        print (msg_to_send)
                        notify.send_text(msg=msg_to_send)

if __name__ == '__main__':
    main()
