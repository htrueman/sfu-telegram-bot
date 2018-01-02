import telepot
from telepot.loop import MessageLoop
import zipfile
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, \
    InlineQueryResultArticle, InputTextMessageContent

import time
import os

bot = telepot.Bot(os.getenv('BOT_SECRET'))
BASE_IMGS_PATH = 'files/imgs/'
BASE_DOCS_PATH = 'files/docs/'


def zipdir(path, ziph):
    # ziph is zipfile handle
    abs_src = os.path.abspath(path)
    for root, dirs, files in os.walk(path):
        for file in files:
            absname = os.path.abspath(os.path.join(root, file))
            arcname = absname[len(abs_src) + 1:]
            ziph.write(absname, arcname)


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

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Yes'.format('?'), callback_data='save ' + msg['from']['username'])],
            [InlineKeyboardButton(text="Nope".format('?'), callback_data='discard ' + msg['from']['username'])]
        ])

        bot.sendMessage(
            chat_id,
            'Zip and save {} images?'.format('?'),
            reply_markup=keyboard)
    else:
        bot.sendMessage(chat_id, "Send me files and I'll zip them for you.")


def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)
    action, username = query_data.split()[0], query_data.split()[1]
    if action == 'save':
        zipf = zipfile.ZipFile(username, 'w', zipfile.ZIP_DEFLATED)
        zipdir('files/imgs/' + username, zipf)
        zipf.close()
        bot.sendDocument(from_id, open('Python.zip', 'rb'))
        os.remove('Python.zip')
    elif action == 'discard':
        pass

    bot.answerCallbackQuery(query_id, text='Got it')

MessageLoop(bot, {'chat': on_chat_message,
                  'callback_query': on_callback_query}).run_as_thread()

print('Listening ...')
while True:
    time.sleep(10)


# def on_chat_message(msg):
#     content_type, chat_type, chat_id = telepot.glance(msg)

#     # print(max_size_files, type(max_size_files))
#     # with max_size_files['file_path'] open as file:
#     #     pass
#     max_size_file_id = msg['photo'][-1]['file_id']
#     max_size_file_dict = bot.getFile(max_size_file_id)
#     bot.download_file(max_size_file_id, max_size_file_dict['file_path'])

#     keyboard = InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text='Save last n images', callback_data='press')]
#     ])

#     bot.sendMessage(
#         chat_id,
#         'Cick the button to save last n (n ∈ ℕ) images till the first text message in the row '
#         'or type the number of images you want to save.',
#         reply_markup=keyboard)


# def on_callback_query(msg):
#     query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
#     print('Callback Query:', query_id, from_id, query_data)

#     bot.answerCallbackQuery(query_id, text='Got it')


# def on_inline_query(msg):
#     def compute():
#         query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
#         print('Inline Query:', query_id, from_id, query_string)
#         articles = [InlineQueryResultArticle(
#             id='abc',
#             title='Save images',
#             input_message_content=InputTextMessageContent(
#                 message_text=query_string
#             ),
#         )]

#         return articles

#     answerer.answer(msg, compute)


# def on_chosen_inline_result(msg):
#     result_id, from_id, query_string = telepot.glance(msg, flavor='chosen_inline_result')
#     print ('Chosen Inline Result:', result_id, from_id, query_string)
#     number_of_imgs_to_save = query_string.split()[0]
#     directory_folder_to_save_name = query_string.split()[1]


# bot = telepot.Bot(os.getenv('BOT_SECRET'))
# answerer = telepot.helper.Answerer(bot)

# MessageLoop(bot, {'chat': on_chat_message,
#                   'callback_query': on_callback_query,
#                   'inline_query': on_inline_query,
#                   'chosen_inline_result': on_chosen_inline_result}).run_as_thread()
# print('Listening ...')
# while True:
#     time.sleep(10)
