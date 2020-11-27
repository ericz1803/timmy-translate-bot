from constants import BOT_TOKEN, GOOGLE_APPLICATION_CREDENTIALS
from telegram.ext import Updater, CommandHandler

from google.cloud import translate_v2 as translate
from google.oauth2 import service_account

translate_client = translate.Client(credentials=service_account.Credentials.from_service_account_info(GOOGLE_APPLICATION_CREDENTIALS))

languages = translate_client.get_languages()

# take string that may or may not be a language code and make it a language code
# return none if it doesn't fit
def map_input_to_language_code(language_input):
    #check if already language code
    if any(language["language"] == language_input for language in languages):
        return language_input
    #attempt to convert language name to code and return none if it doesn't work
    else:
        return next((language["language"] for language in languages if language["name"].lower() == language_input.lower()), None)

# map language code to language name
def map_code_to_name(language_code):
    return next((language["name"] for language in languages if language["language"] == language_code), None)

#translate message into language using google translate
def translate(message, language="en"):
    response = translate_client.translate(message, target_language=language, format_="text")
    language_name = map_code_to_name(response["detectedSourceLanguage"])
    return (response["translatedText"], language_name)

def translate_message(update, context):
    message = update.message

    if (message.reply_to_message): # translate response
        #if target language specified else default to english
        target_language = "en"
        if (context.args):
            target_language = map_input_to_language_code(context.args[0])
            if not target_language:
                context.bot.send_message(chat_id=update.effective_chat.id, 
                reply_to_message_id=message.message_id, 
                text=f"{context.args[0]} is not a valid language name or code. Translating to English instead.")
                target_language="en"

        reply_text = message.reply_to_message.text
        translated_text, source_language = translate(reply_text, target_language)

        context.bot.send_message(chat_id=update.effective_chat.id, 
            reply_to_message_id=message.reply_to_message.message_id, 
            text=f"Translated from {source_language} to {map_code_to_name(target_language)}:\n\n{translated_text}")

    else: # error handling for no reply
        context.bot.send_message(chat_id=update.effective_chat.id, 
            reply_to_message_id=message.message_id, 
            text=f"Must be a reply to a message.")


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm Timmy Translate, I translate messages. Try replying to a message with /translate.")

def main():
    updater = Updater(token=BOT_TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("translate", translate_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
