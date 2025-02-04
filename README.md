A piece of code I wrote for myself to transfer all saved messages, files and photos from "Saved messages" chat on my old account to "Saved messages" chat on my new account.

Course of action:
- Install [TDLib](https://github.com/tdlib/td) (the main Telegram API for building clients). There are [binaries floating around](https://github.com/Bannerets/tdlib-binaries) if you don't want to build everything from scratch.
- Install [python-telegram](https://github.com/alexander-akhmetov/python-telegram/tree/2bd2b2782499b63b7a20705b1ec4d7eef12d0e23) (python wrappers).
- Do JSON export of all your personal chats with photos and files if needed (settings -> advanced -> export Telegram data on Telegram 1.9.21). You get `result.json` and `chats`, put them in the script directory and run `json_to_messages.py` to single "saved messages" out and to convert it to a format ready to be sent. Unfortunately, text formatting gets cut, because I just wanted to retrieve plaintext, photos and files.
- Go to [Telegram developer portal](https://my.telegram.org) and register a new app to get `api_id` and `api_hash` (very quick). Enter `api_id`, `api_hash` and your phone number in `send.py`.
- If you use Linux and have TDLib in PATH, remove library_path parameter in `send.py`. If you use Windows, dump TDLib dll binaries in script directory and provide a path to `tdjson.dll` on line 10 in send.py.
- Turn VPN on if Telegram is blocked in your country.
- Run `send.py`, log in with a code and check that the messages are flowing. It may take time for all of them to go because of intentional delay between messages (to protect the flow against API anti-spam delays). I've noticed that TDLib error handlers do not work as I expected them to work, so makes sense to observe terminal error messages too.
