import asyncio
import aiohttp
import random
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ContentType, BotCommand, FSInputFile
from config import TOKEN
from pathlib import Path
from googletrans import Translator

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()
translator = Translator()

# Путь для сохранения изображений
IMG_PATH = Path("img")
IMG_PATH.mkdir(exist_ok=True)

async def start_handler(message: Message):
    await message.answer("Привет, Используй команду /help, чтобы узнать список доступных команд.")

async def help_handler(message: Message):
    await message.answer("Этот бот умеет выполнять команды:\n/start\n/help\n/photo\n/voice\n/trans")

# Функция для сохранения всех фото, отправленных пользователем
@dp.message(F.photo)
async def photo_handler(message: Message):
    responses = ['Ого!', 'Вау!', 'Фу!']
    rand_answ = random.choice(responses)
    await message.answer(rand_answ)

    photo = message.photo[-1]  # Берем изображение с наибольшим разрешением
    file = await bot.get_file(photo.file_id)
    file_path = IMG_PATH / f"{photo.file_id}.jpg"
    await bot.download_file(file.file_path, destination=file_path)
    print(f"Фото сохранено: {file_path}")

async def voice_handler(message: Message):
    # Укажите путь к вашему готовому файлу
    voice_path = Path("voice.ogg")

    # Проверяем, существует ли файл
    if not voice_path.exists():
        await message.answer("Ошибка: файл 'voice.ogg' не найден в корне проекта.")
        return

    # Отправляем голосовое сообщение
    await bot.send_voice(chat_id=message.chat.id, voice=FSInputFile(str(voice_path)))
    await message.answer("Голосовое сообщение отправлено!")

# Функция для перевода текста на английский
async def trans_handler(message: Message):
    if message.text:
        # Ожидаем выполнения корутины translate
        translated = await translator.translate(message.text, dest='en')
        # Отправляем перевод пользователю
        await message.answer(f"Перевод: {translated.text}")

async def main():
    # Регистрация команд
    dp.message.register(start_handler, CommandStart())
    dp.message.register(help_handler, Command("help"))
    dp.message.register(photo_handler, F.content_type == ContentType.PHOTO)
    dp.message.register(voice_handler, Command("voice"))
    dp.message.register(trans_handler, Command("trans"))

    # Установка списка команд для бота
    await bot.set_my_commands([
        BotCommand(command="start", description="Начало работы"),
        BotCommand(command="help", description="Справка"),
        BotCommand(command="photo", description="Сохранить фото"),
        BotCommand(command="voice", description="Отправить голосовое сообщение"),
        BotCommand(command="trans", description="Перевод")
    ])

    # Запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())