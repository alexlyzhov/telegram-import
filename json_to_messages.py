import json
import pickle

data = json.load(open('result.json', 'rb'))

# get list of saved messages
data = [entry for entry in data['chats']['list'] if entry['type'] == 'saved_messages'][0]['messages']

# only interested in these keys at this point:
# date, text, saved_from, forwarded_from, file, photo

orig_converted_msgs = []
for msg in data:
    converted = msg['date'] + '\n'
    if 'saved_from' in msg and msg['saved_from'] is not None:
        converted += 'saved_from ' + msg['saved_from'] + '\n'
    if 'forwarded_from' in msg and msg['forwarded_from'] is not None:
        converted += 'forwarded_from ' + msg['forwarded_from'] + '\n'
        
    if type(msg['text']) == str:
        converted += msg['text']
    elif type(msg['text']) == list:
#         don't care what type of data this is, just concatenate its text and forget about the rest
        for entry in msg['text']:
            if type(entry) == str:
                converted += entry
            elif type(entry) == dict:
                converted += entry['text']
            else:
                print('Unknown text entry type')
    else:
        print('Invalid msg text type')
        break
        
    converted_entry = {'text': converted}
    if 'photo' in msg:
        converted_entry['photo'] = msg['photo']
    if 'file' in msg:
        converted_entry['file'] = msg['file']
    orig_converted_msgs.append((msg, converted_entry))

pickle.dump(orig_converted_msgs, open('orig_converted_msgs.pickle', 'wb'))