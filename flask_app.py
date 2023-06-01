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
bot.setWebhook(configs['telegram-bot']['webhook'].format(secret), max_connections=1)
marks_finder = MarksFinder(configs['marks']['marks-file'])
template_filler = TemplateFiller(configs['marks']['template-message'])

app = Flask(__name__)

def validate_request(request):
    json_req = request.get_json()
    if "message" not in json_req:
        return "Error", None
    if "text" not in json_req["message"]:
        return "Error", json_req["message"]["chat"]["id"]
    return None, json_req["message"]["chat"]["id"]
    
def validate_student_id(text):
    if not text.isdigit():
        return "Error", messages['enter-student-id']
    if len(text) != 10:
        return "Error", messages['wrong-student-id']
    return None, ""

def start_command(chat_id):
    bot.sendMessage(chat_id, messages['welcome-message'])
    return "OK"

def student_id_command(json_req):
    chat_id = json_req["message"]["chat"]["id"]
    std_id = json_req["message"]["text"]
    err, message = validate_student_id(std_id)
    if err:
        bot.sendMessage(chat_id, message)
        return "OK"
    std_id = unidecode(std_id)
    db = Database(configs['database'])
    is_found, student = marks_finder.find(std_id.strip())
    if not is_found:
        bot.sendMessage(chat_id, messages['ensure-student-id'])
        return "OK"
    is_registered, reg_id = db.check_id(json_req["message"]["from"]["id"])
    if is_registered and reg_id != std_id.strip():
        bot.sendMessage(chat_id, messages['query-your-own-id'])
        return "OK"
    if not is_registered:
        db.insert_student(std_id.strip(), json_req["message"]["from"]["id"])
    json_req['student_name'] = student['name']
    resp = template_filler.fill(student)
    db.insert_log(json.dumps(json_req))
    bot.sendMessage(chat_id, resp)

@app.route('/{}'.format(secret), methods=["POST"])
def telegram_webhook():
    try:
        err, chat_id = validate_request(request)
        if err:
            if chat_id:
                bot.sendMessage(chat_id, messages['unknown-message'])
            return "OK"
        update = request.get_json()
        text = update["message"]["text"]
        if text == '/start': return start_command(chat_id)
        return student_id_command(update)
    except Exception as ex:
        pass
    return "OK"
