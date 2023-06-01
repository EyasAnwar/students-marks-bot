from flask import Flask, request
import telepot
import urllib3
from MarksFinder import MarksFinder
from TemplateFiller import TemplateFiller
from Database import Database
import json
from unidecode import unidecode
import os

my_dir = os.path.dirname(__file__)
messages = json.load(open(os.path.join(my_dir, 'messages-ar.json')))
configs = json.load(open(os.path.join(my_dir, 'configs.json')))

proxy_url = configs['proxy-url']
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

secret = configs['telegram-bot']['secret']
bot = telepot.Bot(configs['telegram-bot']['token'])
print(configs['telegram-bot']['webhook'])
print(configs['telegram-bot']['webhook'].format(secret))
bot.setWebhook(configs['telegram-bot']['webhook'].format(secret), max_connections=1)
marks_finder = MarksFinder(configs['marks']['marks-file'])
template_filler = TemplateFiller(configs['marks']['template-message'])

app = Flask(__name__)


@app.route('/{}'.format(secret), methods=["POST"])
def telegram_webhook():
    try:
        update = request.get_json()
        if "message" in update:
            chat_id = update["message"]["chat"]["id"]
            if "text" in update["message"]:
                text = update["message"]["text"]
                if text == '/start':
                    bot.sendMessage(chat_id, messages['welcome-message'])
                else:
                    if not text.isdigit():
                        bot.sendMessage(chat_id, messages['enter-student-id'])
                        return "OK"
                    if len(text) != 10:
                        bot.sendMessage(chat_id, messages['wrong-student-id'])
                        return "OK"
                    text = unidecode(text)
                    db = Database(configs['database'])
                    is_found, student = marks_finder.find(text.strip())
                    if not is_found:
                        bot.sendMessage(chat_id, messages['ensure-student-id'])
                        return "OK"
                    is_registered, reg_id = db.check_id(update["message"]["from"]["id"])
                    if is_registered and reg_id != text.strip():
                        bot.sendMessage(chat_id, messages['query-your-own-id'])
                        return "OK"
                    if not is_registered:
                        db.insert_student(text.strip(), update["message"]["from"]["id"])
                    update['student_name'] = student['name']
                    resp = template_filler.fill(student)
                    db.insert_log(json.dumps(update))
                    bot.sendMessage(chat_id, resp)
            else:
                bot.sendMessage(chat_id, messages['unknown-message'])
    except Exception as ex:
        pass
    return "OK"
