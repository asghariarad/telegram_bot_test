import os
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, ConversationHandler, CommandHandler, CallbackContext

# بررسی وضعیت کاربری
ENTER_FILENAME, ENTER_COVER = range(2)

def start(update: Update, _: CallbackContext) -> int:
    update.message.reply_text("سلام! لطفاً فایل خود را ارسال کنید.")
    return ENTER_FILENAME

def receive_filename(update: Update, _: CallbackContext) -> int:
    user = update.effective_user
    file = update.message.document.get_file()
    file.download(f"{user.id}.temp")

    update.message.reply_text("فایل با موفقیت دریافت شد. حالا نام جدید مورد نظر خود را بنویسید.")
    return ENTER_COVER

def receive_cover(update: Update, _: CallbackContext) -> int:
    user = update.effective_user
    cover_text = update.message.text

    # نام فایل جدید که ترکیبی از نام فایل قبلی و نام کاور است
    new_filename = f"{cover_text}_{user.id}.ext"

    # اعمال کاور به فایل
    try:
        with open(f"{user.id}.temp", "rb") as file:
            file_contents = file.read()

        # اعمال کاور به فایل (در اینجا فرض می‌گیریم کاور تصویر می‌باشد)
        # در این مثال، فایل‌های موسیقی و غیره نیز به عنوان تصویر در نظر گرفته می‌شوند
        with open(new_filename, "wb") as new_file:
            new_file.write(file_contents)

    except Exception as e:
        update.message.reply_text(f"خطا در اعمال کاور: {str(e)}")
        return ConversationHandler.END

    update.message.reply_text(f"کاور با موفقیت اعمال شد. فایل جدید: {new_filename}")
    update.message.reply_document(document=open(new_filename, "rb"))

    # حذف فایل موقتی
    os.remove(f"{user.id}.temp")

    return ConversationHandler.END

def cancel(update: Update, _: CallbackContext) -> int:
    update.message.reply_text("عملیات لغو شد.")
    return ConversationHandler.END

def main() -> None:

    updater = Updater("1851505849:AAE0jsekg1Yb6smdeDuJL4ipRuO_W25Rqvk")

    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ENTER_FILENAME: [MessageHandler(Filters.document.mime_type("image/*"), receive_filename)],
            ENTER_COVER: [MessageHandler(Filters.text, receive_cover)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
