from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo, InputMediaPhoto, InputMediaVideo
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler, MessageHandler, filters, ConversationHandler
from Settings_loader import BOT_TOKEN, BOT_USERNAME, TARGET_CHAT_ID, DJANGO_URL
import json
from time import sleep
import requests
from os import makedirs
from os.path import exists, join

REQUEST_MEDIA = 1
MEDIA_FOLDER = 'media_files'
if not exists(MEDIA_FOLDER):
    makedirs(MEDIA_FOLDER)


async def launch_web_ui(update: Update, context: CallbackContext):
    kb = [
        [KeyboardButton(
            "Окрыть форму отчетов",
            web_app=WebAppInfo("https://igggor.github.io")  # obviously, set yours here.
        )]
    ]
    await update.message.reply_text("Приветствую, я Бот СТВ для отправки отчетов", reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True))


async def web_app_data(update: Update, context: CallbackContext):
    data = json.loads(update.message.web_app_data.data)
    Fam = data["lines"][0]["value"]
    name = data["lines"][1]["value"]
    otch = data["lines"][2]["value"]
    worker = data["lines"][3]["value"]
    address = data["lines"][4]["value"]
    date = data["lines"][5]["value"]
    req = [Fam, name, worker, address, date]
    if "" in req:
        await update.message.reply_text("Не были введены обязательные данные. Заполните форму заново")
        return ConversationHandler.END
    report = f"""
    📃Новый отчет от {worker}📃
👨‍💼ФИО заказчика {Fam} {name} {otch}
🏡Адрес выполнения: {address}
📅 Дата выполнения {date}
    """
    context.user_data['report'] = report
    context.user_data['media_files'] = []
    context.user_data['form_data'] = {
        "family": Fam,
        "address": address,
        "sender_name": worker
    }

    await update.message.reply_text(report)
    url = "http://192.168.1.34:8088/send_mount"
    params = {
        "sender_name": worker,
        "complete_date": date,
        "family": Fam,
        "name": name,
        "address": address,
        "otch": otch
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        print("Данные успешно отправлены")
    else:
        print(f"Ошибка при отправке данных: {response.status_code}")
        print(response.text)

    kb = [[KeyboardButton("/done")]]
    await update.message.reply_text("Теперь загрузите медиафайлы (фото/видео). Отправьте файлы по одному и нажмите /done для завершения.\n\n⚠⚠⚠Убедитесь в том, что файлы загрузились полностью⚠⚠⚠", reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True))
    return REQUEST_MEDIA


async def handle_media(update: Update, context: CallbackContext):
    if 'media_files' not in context.user_data:
        context.user_data['media_files'] = []
    form_data = context.user_data.get('form_data', {})

    media_file_id = None
    media_type = None

    if update.message.photo:
        media_file_id = update.message.photo[-1].file_id
        media_type = 'photo'
        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)
        file_path = join(MEDIA_FOLDER, f"buffer.jpg")
        await file.download_to_drive(file_path)
        # Отправка файла на Django сервер
        data = {
            'sender_name': form_data.get('sender_name', 'Имя отправителя'),
            'address': form_data.get('address', 'Адрес'),
            'family': form_data.get('family', 'Фамилия'),
        }

        with open(file_path, 'rb') as f:
            response = requests.post(DJANGO_URL, files={'file': f}, data=data)

    elif update.message.video:
        media_file_id = update.message.video.file_id
        media_type = 'video'

    if media_file_id and media_type:
        context.user_data['media_files'].append({'file_id': media_file_id, 'type': media_type})


async def done(update: Update, context: CallbackContext):
    media_files = context.user_data.get('media_files', [])
    report = context.user_data.get('report', '')
    await context.bot.send_message(chat_id=TARGET_CHAT_ID, text=report)

    if media_files:
        media_groups = [media_files[i:i+10] for i in range(0, len(media_files), 10)]
        for media_group in media_groups:
            media_group_objects = []
            for media in media_group:
                if media['type'] == 'photo':
                    media_group_objects.append(InputMediaPhoto(media=media['file_id']))
                elif media['type'] == 'video':
                    media_group_objects.append(InputMediaVideo(media=media['file_id']))

            # Отправка в другой чат
            sleep(1)
            await context.bot.send_media_group(chat_id=TARGET_CHAT_ID, media=media_group_objects)
        kb = [
            [KeyboardButton(
                "Открыть форму отчета",
                web_app=WebAppInfo("https://igggor.github.io")  # obviously, set yours here.
            )]
        ]
        await update.message.reply_text("Отчет отправлен", reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True))

    else:
        await update.message.reply_text("Нет загруженных медиафайлов.")

    context.user_data.clear()
    return ConversationHandler.END


if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data)],
        states={
            REQUEST_MEDIA: [
                MessageHandler(filters.PHOTO | filters.VIDEO, handle_media),
                CommandHandler('done', done)
            ],
        },
        fallbacks=[CommandHandler('done', done)]
    )

    application.add_handler(CommandHandler('start', launch_web_ui))
    application.add_handler(conv_handler)

    print(f"Your bot is listening! Navigate to http://t.me/{BOT_USERNAME} to interact with it!")
    application.run_polling()
