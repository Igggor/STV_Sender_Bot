from modules.dependencies import *


async def launch_web_ui(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if not db.user_exists(user_id):
        await update.message.reply_text("Привет! Пожалуйста, введите вашу фамилию для регистрации:")
        logger.info(f"User {user_id} started registration")
        return ENTER_LAST_NAME
    else:
        await update.message.reply_text("Приветствую, я Бот СТВ для отправки отчетов", reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True))
        return ConversationHandler.END


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


async def web_app_data(update: Update, context: CallbackContext):
    data = loads(update.message.web_app_data.data)
    fam = data["lines"][0]["value"]
    name_ot = data["lines"][1]["value"]
    address = data["lines"][2]["value"]
    date = check_date(data["lines"][3]["value"])
    name, otch = check_name(name_ot)
    worker = db.get_family_name(update.message.from_user.id)
    req = [fam, worker, address, date]
    if "" in req:
        await update.message.reply_text("Не были введены обязательные данные. Заполните форму заново")
        return ConversationHandler.END
    report = f"""
    📃Новый отчет от {worker}📃
🟢ФИО заказчика {fam} {name} {otch}
🟢Адрес выполнения: {address}
🟢Дата выполнения {date}
    """
    context.user_data['report'] = report
    context.user_data['media_files'] = []
    context.user_data['form_data'] = {
        "family": fam,
        "address": address,
        "sender_name": worker
    }

    await update.message.reply_text(report)
    url = "http://192.168.1.34:8088/send_mount"
    params = {
        "sender_name": worker,
        "complete_date": date,
        "family": fam,
        "name": name,
        "address": address,
        "otch": otch
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        logger.info("Данные успешно отправлены")
    else:
        print(f"Ошибка при отправке данных: {response.status_code}")
        logger.error(f"Text data wasn`t sent.\n Statuscode response {response.status_code}")

    kb = [[KeyboardButton("/done")]]
    await update.message.reply_text("Теперь загрузите медиафайлы (фото/видео). Отправьте файлы по одному и нажмите /done для завершения.\n\n⚠⚠⚠Убедитесь в том, что файлы загрузились полностью⚠⚠⚠", reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True))
    return REQUEST_MEDIA


async def register_last_name(update: Update, context: CallbackContext):
    last_name = update.message.text
    user_id = update.message.from_user.id
    logger.info(f"Registering user: {user_id} with last name: {last_name}")
    db.add_user(user_id, last_name)
    await update.message.reply_text("Регистрация успешна! Вы можете начать пользоваться ботом.", reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True))
    return ConversationHandler.END


async def register_last_name(update: Update, context: CallbackContext):
    last_name = update.message.text
    user_id = update.message.from_user.id
    logger.info(f"Registering user: {user_id} with last name: {last_name}")
    db.add_user(user_id, last_name)
    await update.message.reply_text("Регистрация успешна! Вы можете начать пользоваться ботом.", reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True))
    return ConversationHandler.END


async def change_last_name(update: Update, context: CallbackContext):
    await update.message.reply_text("Введите новую фамилию:")
    logger.info("Family changing...")
    return CHANGE_LAST_NAME


async def update_last_name(update: Update, context: CallbackContext):
    new_last_name = update.message.text
    user_id = update.message.from_user.id
    logger.info(f"Updating last name for user: {user_id} to: {new_last_name}")  # Логирование изменения фамилии
    db.update_family_name(user_id, new_last_name)
    await update.message.reply_text("Фамилия успешно обновлена!", reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True))
    return ConversationHandler.END


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
            sleep(1)
            await context.bot.send_media_group(chat_id=TARGET_CHAT_ID, media=media_group_objects)
        await update.message.reply_text("Отчет отправлен", reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True))
    else:
        await update.message.reply_text("Нет загруженных медиафайлов.", reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True))

    context.user_data.clear()
    return ConversationHandler.END

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', launch_web_ui),
            MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data),
            CommandHandler('change_last_name', change_last_name)  # Add this line
        ],
        states={
            REQUEST_MEDIA: [
                MessageHandler(filters.PHOTO | filters.VIDEO, handle_media),
                CommandHandler('done', done)
            ],
            ENTER_LAST_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, register_last_name)
            ],
            CHANGE_LAST_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, update_last_name)
            ],
        },
        fallbacks=[CommandHandler('done', done)]
    )

    application.add_handler(conv_handler)

    print(f"Your bot is listening! Navigate to http://t.me/{BOT_USERNAME} to interact with it!")
    application.run_polling()
