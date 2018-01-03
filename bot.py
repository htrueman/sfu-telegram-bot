import telepot
from telepot.loop import MessageLoop
import zipfile
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

import time
import os
from shutil import rmtree
from contextlib import suppress

bot = telepot.Bot('526746468:AAEiRiGQdtNV0NsMru72kNETPyv7j4sqajw')
BASE_IMGS_PATH = 'files/imgs/'
BASE_DOCS_PATH = 'files/docs/'


def zipdir(path, ziph, files_type):
    # ziph is zipfile handle
    abs_src = os.path.abspath(path)
    for root, dirs, files in os.walk(path):
        for file in files:
            absname = os.path.abspath(os.path.join(root, file))
            arcname = files_type + '/' + absname[len(abs_src) + 1:]
            ziph.write(absname, arcname)


def rename_files_with_modified_time(path):
    for root, dirs, files in os.walk(path):
        for filename in files:
            modified_time = os.path.getmtime(path + '/' + filename)  # get file modification timestamp
            file_ext = filename.split('.')[-1]
            new_name = str(modified_time).split('.')[0] + str(modified_time).split('.')[1]
            os.rename(path + '/' + filename, path + '/' + new_name + '.' + file_ext)


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type in ['photo', 'document']:
        path_to_save = BASE_IMGS_PATH if content_type == 'photo' else BASE_DOCS_PATH
        user_files_dir = path_to_save + msg['from']['username'] + '/'
        if not os.path.exists(user_files_dir):
            os.makedirs(user_files_dir)

        if content_type == 'photo':
            max_size_file_id = msg['photo'][-1]['file_id']
            max_size_file_dict = bot.getFile(max_size_file_id)
            bot.download_file(
                max_size_file_id,
                user_files_dir +
                max_size_file_dict['file_id'] +
                '.' + max_size_file_dict['file_path'].split('.')[-1])

        elif content_type == 'document':
            document_id = msg['document']['file_id']
            document_name = msg['document']['file_name']
            bot.download_file(document_id, user_files_dir + document_name)

    elif content_type == 'text' and msg['text'] == '/zip':
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Yes'.format('?'), callback_data='save ' + msg['from']['username'])],
            [InlineKeyboardButton(
                text="Nope, remove the files above", callback_data='discard ' + msg['from']['username'])]
        ])

        bot.sendMessage(
            chat_id,
            'Zip and save these files?',
            reply_markup=keyboard)
    else:
        bot.sendMessage(
            chat_id,
            "Send me the files and I'll zip them for you. Type /zip after the files are uploaded.")


def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')

    action, username = query_data.split()[0], query_data.split()[1]
    if action == 'save':
        rename_files_with_modified_time(os.getcwd() + '/' + BASE_IMGS_PATH + username)

        zipf = zipfile.ZipFile(username + '.zip', 'w', zipfile.ZIP_DEFLATED)
        zipdir(BASE_IMGS_PATH + username, zipf, 'imgs')
        zipdir(BASE_DOCS_PATH + username, zipf, 'docs')
        zipf.close()
        bot.sendDocument(from_id, open(username + '.zip', 'rb'))
        os.remove(username + '.zip')
        with suppress(OSError):
            rmtree(os.getcwd() + '/' + BASE_IMGS_PATH + username)
            rmtree(os.getcwd() + '/' + BASE_DOCS_PATH + username)
    elif action == 'discard':
        with suppress(OSError):
            rmtree(os.getcwd() + '/' + BASE_IMGS_PATH + username)
            rmtree(os.getcwd() + '/' + BASE_DOCS_PATH + username)

    bot.answerCallbackQuery(query_id, text='Got it')

MessageLoop(bot, {'chat': on_chat_message,
                  'callback_query': on_callback_query}).run_as_thread()

print('Listening ...')
while True:
    time.sleep(10)
