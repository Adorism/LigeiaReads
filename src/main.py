import Constants as keys
from telegram.ext import *
import Responses as R
import logging

#from src.recommendation_engine.inference import predict_subgenre, get_similar_books
#from src.recognition_engine.inference import classify_cover

print("It's alive!!!")

# Enable logging
logging.basicConfig(
    #filename= 'telgramBot.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Main interactions
CHOOSING, GET_TEXT, GET_IMAGE = range(3)
# Callback data
CALLBACK1, CALLBACK2 = range(3,5)

reply_keyboard = [
    ['Eerie', 'Mind-Bending'],
    ['Gory', 'Intense'],
]


def start_command(update, context: CallbackContext) -> int:
    user = update.message.from_user
    #logger.ingo(f'{user.first_name}: Start')

    context.user_date['chat_id'] = update.message.chat_id

    update.message.reply_text("Let's find you something absolutely ghastly to read", reply_markup=markup)



def help_command(update, context):
    update.message.reply_text('If you need help')

def handle_message(update, context):
    text = str(update.message.text).lower()
    response = R.sample_responses(text)

    update.message.reply_text(response)

def error(update, context):
    print(f'Update{update} cause error {context.error}')

def main():
    updater = Updater(keys.API_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('help', help_command))

    dp.add_handler(MessageHandler(Filters.text, handle_message))

    dp.add_error_handler(error)

    updater.start_polling(5)
    updater.idle()

if __name__ == '__main__':
    # Execute the parse_args() method
    #args = my_parser.parse_args()
    main()