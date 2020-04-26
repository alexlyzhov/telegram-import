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
sleep_time = 0.5  # as a precaution, seems like 10-min ban after 1000s of requests is happening anyway

requests = []
for msg_i, (orig, converted) in enumerate(orig_converted_msgs[:n]):
    if len(converted['text']) > 20:  # 20 means there is only date and newline
        request = tg.send_message(chat_id, converted['text'])

        requests.append(request)
        request.wait()
        if request.error:
            print(request.error_info)
            break
        time.sleep(sleep_time)
    
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
        request.wait()
        if request.error:
            print(request.error_info)
            break
        time.sleep(sleep_time)
    
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
        request.wait()
        if request.error:
            print(request.error_info)
            break
        time.sleep(sleep_time)