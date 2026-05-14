import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Токен беремо з налаштувань Render (Environment Variables)
TOKEN = os.getenv("TELEGRAM_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# База питань (можна додавати свої з Історії чи Фізики)
QUESTIONS = [
    {
        "question": "У якому місті було засновано перший університет у Наддніпрянській Україні (1805 р.)?",
        "options": ["Київ", "Харків", "Одеса", "Львів"],
        "correct": "Харків"
    },
    {
        "question": "Як називається фізична величина, що характеризує швидкість виконання роботи?",
        "options": ["Енергія", "Сила", "Потужність", "Тиск"],
        "correct": "Потужність"
    }
]

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привіт! Я твій бот-тренажер. Напиши /quiz, щоб почати тест.")

@dp.message(Command("quiz"))
async def send_quiz(message: types.Message):
    # Беремо перше питання (для прикладу)
    q = QUESTIONS[0]
    builder = InlineKeyboardBuilder()
    
    # Створюємо кнопки для відповідей
    for option in q["options"]:
        builder.button(text=option, callback_data=f"answer_{option}")
    
    builder.adjust(2) # Кнопки у два ряди
    await message.answer(q["question"], reply_markup=builder.as_markup())

@dp.callback_query(F.data.startswith("answer_"))
async def check_answer(callback: types.CallbackQuery):
    user_answer = callback.data.split("_")[1]
    # Перевіряємо перше питання (спрощена логіка)
    correct_answer = QUESTIONS[0]["correct"]
    
    if user_answer == correct_answer:
        await callback.message.edit_text(f"✅ Правильно! Це {correct_answer}.")
    else:
        await callback.message.edit_text(f"❌ Неправильно. Правильна відповідь: {correct_answer}.")
    
    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
      
