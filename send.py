from telegram.client import Telegram
import os
import pickle
import time

tg = Telegram(
    api_id='your_api_id',
    api_hash='your_hash',
    phone='your_phone',
    library_path='path_to_tdjson',
    database_encryption_key='any_key',
    files_directory='tmp'
)
tg.login()

result = tg.get_me()
result.wait()
chat_id = result.update['id']  # seems like it also serves as saved messages chat id

orig_converted_msgs = pickle.load(open('orig_converted_msgs.pickle', 'rb'))
sleep_time = 1  # in seconds as a precaution against flood prevention delays

def check_request(request):
    request.wait()
    if request.error:
        print(request.error_info)
        time.sleep(2000)
    if 'sending_state' in request.update:
        if request.update['sending_state'] == 'messageSendingStatePending':
            print(msg_i, 'messageSendingStatePending')
            time.sleep(100)
        elif request.update['sending_state'] == 'messageSendingStateFailed':
            print(msg_i, 'messageSendingStateFailed')
            time.sleep(2000)  # precautions against flood_wait
    time.sleep(sleep_time)

requests = []
for msg_i, (orig, converted) in enumerate(orig_converted_msgs[:n]):
    if len(converted['text']) > 20:  # 20 means there is only date and newline
        request = tg.send_message(chat_id, converted['text'])
        requests.append(request)
        check_request(request)
    
    if 'file' in converted:
        data = {
            '@type': 'sendMessage',
            'chat_id': chat_id,
            'input_message_content': {
                '@type': 'inputMessageDocument',
                'document': {'@type': 'inputFileLocal',
                             'path': converted['file']},
            },
        }
        request = tg._send_data(data)
        requests.append(request)
        check_request(request)
    
    if 'photo' in converted:
        data = {
            '@type': 'sendMessage',
            'chat_id': chat_id,
            'input_message_content': {
                '@type': 'inputMessagePhoto',
                'photo': {'@type': 'inputFileLocal',
                          'path': converted['photo']},
            },
        }
        request = tg._send_data(data)
        requests.append(request)
        check_request(request)
