import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, \
    InlineQueryResultArticle, InputTextMessageContent

import time


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Save last n images', callback_data='press')]
    ])

    bot.sendMessage(
        chat_id,
        'Cick the button to save last n (n ∈ ℕ) images till the first text message in the row '
        'or type the number of images you want to save.',
        reply_markup=keyboard)


def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)

    bot.answerCallbackQuery(query_id, text='Got it')


def on_inline_query(msg):
    def compute():
        query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
        print('Inline Query:', query_id, from_id, query_string)

        articles = [InlineQueryResultArticle(
            id='abc',
            title='Save images',
            input_message_content=InputTextMessageContent(
                message_text=query_string
            ),
        )]

        return articles

    answerer.answer(msg, compute)


def on_chosen_inline_result(msg):
    result_id, from_id, query_string = telepot.glance(msg, flavor='chosen_inline_result')
    print ('Chosen Inline Result:', result_id, from_id, query_string)
    number_of_imgs_to_save = query_string.split()[0]
    directory_folder_to_save_name = query_string.split()[1]
    print(number_of_imgs_to_save, directory_folder_to_save_name)
    print(999)


bot = telepot.Bot('526746468:AAEiRiGQdtNV0NsMru72kNETPyv7j4sqajw')
answerer = telepot.helper.Answerer(bot)

MessageLoop(bot, {'chat': on_chat_message,
                  'callback_query': on_callback_query,
                  'inline_query': on_inline_query,
                  'chosen_inline_result': on_chosen_inline_result}).run_as_thread()
print('Listening ...')
while True:
    time.sleep(10)
