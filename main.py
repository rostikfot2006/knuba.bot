import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart
from aiogram.types import (
    CallbackQuery,
    FSInputFile,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

TOKEN = "8104227176:AAF2J_B7CrAGnzvtFvFcJ6wAQTjbJJDBDcE"
dp = Dispatcher()

# ============================================================
# СТРУКТУРА ФАКУЛЬТЕТІВ ТА СПЕЦІАЛЬНОСТЕЙ КНУБА
# ============================================================
FACULTIES = {
    "ФАІТ": {
        "A5": "Професійна освіта",
        "F2": "Інженерія програмного забезпечення",
        "F3": "Комп'ютерні науки",
        "F5": "Кібербезпека та захист інформації",
        "F6": "Інформаційні системи та технології",
        "F7": "Комп'ютерна інженерія",
        "G3": "Електрична інженерія",
        "G4": "Енерговиробництво (ВДЕ)",
        "G7": "Автоматизація та робототехніка",
        "G9": "Прикладна механіка",
        "G11": "Машинобудування",
    },
    "ФУПП": {
        "G19": "Міське будівництво та господарство",
        "D8": "Будівельне та містобудівне право",
        "D4": "Державне управління та політологія",
    },
    "АРХ": {
        "B2": "Дизайн",
        "G17": "Архітектура та містобудування",
    },
    "БФ": {
        "C1": "Економіка",
        "D1": "Облік і оподаткування",
        "D3": "Менеджмент",
        "G19": "Будівництво та цивільна інженерія",
    },
    "БТФ": {
        "D5": "Маркетинг",
        "D7": "Торгівля та товарознавство",
        "G1": "Хімічні технології та інженерія",
        "G19": "Технологія будівельних конструкцій і виробів",
    },
    "ГІСУТ": {
        "A7": "Фізична культура і спорт",
        "G18.1": "Геодезія та землеустрій",
        "G18.2": "Геоінформаційні системи і технології",
    },
    "ФІСЕ": {
        "E2": "Екологія",
        "G2": "Технології захисту довкілля",
        "G4.02": "Теплоенергетика",
        "G16": "Нафтогазова інженерія",
        "G19": "Будівництво та цивільна інженерія",
    },
}

GROUPS = {
    "G7": [
        "АТП – 22",
        "АКІТ – 23",
        "АКІТс – 23",
        "АКІТ – 24",
        "АКІТм – 24",
        "АКІТс – 24",
        "АКІТ – 25",
        "АКІТм – 25",
        "АКІТс – 25",
    ],
    "F3": [
        "КН – 22-1",
        "КН – 22-2",
        "КН – 23-1",
        "КН – 23-2",
        "КНс – 23",
        "КН – 24-1",
        "КН – 24-2",
        "КНм – 24",
        "КНс – 25",
        "КН – УПм – 24",
        "МН – УПм – 24",
        "КН – 25",
        "КНм – 25",
        "КНмд – 25",
        "КНд – 25",
        "КН – УПм – 25",
        "КН – УПмд – 25",
        "МН – УПм – 25",
        "МН – УПмд – 25",
    ],
    "G11": [
        "БМО – 22",
        "БМО – 23",
        "БМОс – 23",
        "БМО – 24",
        "БМОм – 24",
        "БМОс – 24",
        "ГМ – 25",
        "ГМс – 25",
        "ГМм – 25",
    ],
    "F7": [
        "КСМ – 22",
        "КСМ – 23",
        "КСМс – 23",
        "КСМ – 24",
        "КСМс – 24",
        "КСМм – 24",
        "КСМ – 25",
        "КСМд – 25",
        "КСМм – 25",
        "КСМс – 25",
    ],
    "G9": [
        "ПС – 22",
        "ПС – 23",
        "ПС – 24",
        "ПС – 25",
        "ПСсм – 24",
        "ПСсм – 25",
    ],
    "F5": [
        "БІКС – 22",
        "БІКС – 23-1",
        "БІКС – 23-2",
        "БІКСс – 23",
        "БІКС – 24-1",
        "БІКС – 24-2",
        "БІКСс – 24",
        "БІКСс – 25",
        "БІКСм – 24",
        "БІКСмд – 25",
        "БІКСм – 25",
        "БІКСд – 25",
        "БІКС – 25",
    ],
    "G4": ["ВДЕ – 23", "ВДЕ – 24", "ВДЕ – 25", "ВДЕс – 25"],
    "F6": [
        "ІСТ – 22",
        "ІСТ – 23",
        "ІСТ – 24",
        "ІСТ – 25",
        "ІСТм – 24",
        "ІСТ-УП – 22",
        "ІСТ-УП – 23",
        "ІПЗм – 24",
        "ШІКТм – 24",
        "ІСТм – 25",
        "ІСТ-ШІд – 25",
        "ІСТд – 25",
        "ШІКТм – 25",
        "ШІКТмд – 25",
        "ІПЗм – 25",
        "ІПЗд – 25",
    ],
    "G3": [
        "ECA – 22",
        "ECA – 23",
        "ECAC – 23",
        "ECA – 24",
        "ECAC – 24",
        "ECA – 25",
        "ECAC – 25",
        "EСАм – 24",
        "EСАм – 25",
    ],
    "A5": [
        "ПНБЗ – 22",
        "ПНБЗ – 23",
        "ПНБЗ – 25",
        "ПНК – 22",
        "ПНК – 23",
        "ПНК – 24",
        "ПНК – 25",
        "ПНКм – 24",
        "ПНМ – 22",
        "ПНМ – 23",
        "ПНМ – 24",
        "ПНМ – 25",
        "ПНМс – 25",
        "ПНКм – 25",
        "ПНКс – 25",
    ],
    "F2": [
        "ІПЗ – 22",
        "ІПЗ – 23",
        "ІПЗ – 24",
        "ІПЗ – 25",
        "ІПЗм – 24",
        "ІПЗм – 25",
    ],
}

KSM_24_SCHEDULE = """📅 Розклад для групи КСМ – 24 (Жовтень 2026):

🟢 Понеділок:
- 2 пара (10:30) — ТестПрогСис [Лк] (Дистанційно, Шабала Є.Є.)

🔵 Вівторок:
- 1 пара (09:00) — ФОКК [Пз] (ауд. 476, Азнаурян І.О.)
- 2 пара (10:30) — ТестПрогСис [Лб] (ауд. 472, Шабала Є.Є.)

🟠 Середа:
- 1 пара (09:00) — СисАналіз [Пз] (ауд. 349, Ізмайлова О.В.)
- 2 пара (10:30) — УП-S-UP [Пз] (ауд. 148, Концевий В.В.)

🟣 Четвер:
- 4 пара (13:50) — АвтСисДіагіКон [Пз] (ауд. 30А, Городжа А.Д.)
- 5 пара (15:20) — ТестПрогСис [Лб] (ауд. 472, Шабала Є.Є.)

🟡 П'ятниця:
- 2 пара (10:30) — ДослідОперацій [Лк/Лб] (Дистанційно, Терентьєв О.О.)
- 3 пара (12:20) — СисАналіз [Лк] (Дистанційно, Ізмайлова О.В.)
- 4 пара (13:50) — Політ [Лк] (Дистанційно, Семко В.Л.)
- 5 пара (15:20) — ФОКК [Лк] (Дистанційно, Азнаурян І.О.)
"""

KSM_25_SCHEDULE = """📅 Розклад для групи КСМ – 25 (Жовтень 2026):

🟢 Понеділок:
- 1 пара (09:00) — ПтаРОбчисл [Лк] (Дистанційно, Маленко М.В.)
- 2 пара (10:30) — ІФтаФД [Лк] (Дистанційно, Лакуша Н.М.)
- 3 пара (12:20) — ЕІТ [Лк] (Дистанційно, Терентьєв О.О.)
- 4 пара (13:50) — ОбОрПрог [Лк] (Дистанційно, Гончаренко Т.А.)
- 5 пара (15:20) — ЦифрОбСигн [Лк] (Дистанційно, Котенко А.М.)

🔵 Вівторок:
- 1 пара (09:00) — ОБД [Лб] (ауд. 349, Бардін Я.О.)
- 2 пара (10:30) — ЕІТ [Пз] (ауд. 146, Терентьєв О.О.)
- 3 пара (12:20) — ЦифрОбСигн [Пз] (ауд. каф., Котенко А.М.)

🟠 Середа:
- 3 пара (12:20) — ФізВих [Пз] / ІПЗ [Лб] (ауд. спорт / ауд. 504, Головко О.О. / Маринський К.В.)
- 4 пара (13:50) — ДискретМат [Пз] (ауд. 368/457, Серпінська О.І.)

🟣 Четвер:
- 1 пара (09:00) — ОснАкадПисЦит [Пз] (ауд. 448, Маковій М.Г.)
- 2 пара (10:30) — ОбОрПрог [Лб] (ауд. 604, Долгополов С.Ю.)
- 3 пара (12:20) — ПтаРОбчисл [Пз] (ауд. каф., Маленко М.В.)
- 4 пара (13:50) — ФізВих [Пз] (ауд. спорт, Головко О.О.)

🟡 П'ятниця:
- 1 пара (09:00) — ДискретМат [Лк] (Дистанційно, Серпінська О.І.)
- 2 пара (10:30) — ОБД [Лк] (Дистанційно, Бардін Я.О.)
- 3 пара (12:20) — ІПЗ [Лк] (Дистанційно, Гуменний Д.О.)
"""

CAMPUS_MAP_CAPTION = """🗺 <b>Навігація по корпусах КНУБА:</b>

Лабораторний корпус - всі ауд. що мають чотирьохцифрове значення.
Військовий корпус він же (червоний) - всі ауд. що мають в назві «С».
Геодезичний корпус він же (рожевий) - всі ауд. що мають у назві «З».
Дизайнерський центр («Д») - всі ауд. що мають в назві «Д».
Архітектурний корпус - всі ауд. що мають у назві «А».

<b>Ліве крило:</b>
І поверх - 103-124 ауд.
II поверх - 203-224 ауд.
III поверх - 301-320 ауд.
IV поверх - 401-420 ауд.

<b>Праве крило:</b>
І поверх - 123-152 ауд.
II поверх - 226-254 ауд.; бібліотека.
III поверх - 321-348 ауд.; читальна зала.
IV поверх - 422-440 ауд.

<b>Прибудова:</b>
І поверх - 154-194 ауд.
II поверх - 251-292 ауд.
III поверх - 345-376 ауд.
IV поверх - 439-484 ауд.

<b>Архітектурний (А):</b>
І поверх - 102-110 ауд.
-I поверх - 123-131 ауд.
II поверх - кафедри.
III поверх - 302-319 ауд.; бібліотека.
"""


# ============================================================
# КЛАВІАТУРИ
# ============================================================
def get_faculties_kb():
    keyboard = [
        [
            InlineKeyboardButton(text="ФАІТ", callback_data="fac_ФАІТ"),
            InlineKeyboardButton(text="ФУПП", callback_data="fac_ФУПП"),
        ],
        [
            InlineKeyboardButton(text="АРХ", callback_data="fac_АРХ"),
            InlineKeyboardButton(text="БФ", callback_data="fac_БФ"),
        ],
        [
            InlineKeyboardButton(text="БТФ", callback_data="fac_БТФ"),
            InlineKeyboardButton(text="ГІСУТ", callback_data="fac_ГІСУТ"),
        ],
        [InlineKeyboardButton(text="ФІСЕ", callback_data="fac_ФІСЕ")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_specialties_kb(faculty):
    keyboard = []
    for code, name in FACULTIES[faculty].items():
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"{code} — {name}", callback_data=f"spec_{faculty}_{code}"
                )
            ]
        )
    keyboard.append(
        [
            InlineKeyboardButton(
                text="⬅️ Назад до факультетів", callback_data="back_fac"
            )
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_courses_kb(faculty, spec_code):
    keyboard = [
        [
            InlineKeyboardButton(
                text="1 курс", callback_data=f"course_{faculty}_{spec_code}_1"
            ),
            InlineKeyboardButton(
                text="2 курс", callback_data=f"course_{faculty}_{spec_code}_2"
            ),
        ],
        [
            InlineKeyboardButton(
                text="3 курс", callback_data=f"course_{faculty}_{spec_code}_3"
            ),
            InlineKeyboardButton(
                text="4 курс", callback_data=f"course_{faculty}_{spec_code}_4"
            ),
        ],
        [
            InlineKeyboardButton(
                text="5 курс (Магістратура)",
                callback_data=f"course_{faculty}_{spec_code}_5",
            ),
            InlineKeyboardButton(
                text="6 курс (Магістратура)",
                callback_data=f"course_{faculty}_{spec_code}_6",
            ),
        ],
        [
            InlineKeyboardButton(
                text="⬅ Назад до спеціальностей",
                callback_data=f"back_spec_{faculty}",
            )
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_groups_kb(spec_code, faculty, course):
    all_groups = GROUPS.get(spec_code, [])
    filtered_groups = []
    for grp in all_groups:
        if course in ["5", "6"]:
            if any(m in grp.lower() for m in ["м", "мд"]):
                filtered_groups.append(grp)
        else:
            if not any(m in grp.lower() for m in ["м", "мд"]):
                filtered_groups.append(grp)

    if not filtered_groups:
        filtered_groups = all_groups

    keyboard = []
    row = []
    for grp in filtered_groups:
        row.append(
            InlineKeyboardButton(
                text=grp, callback_data=f"grp_{faculty}_{spec_code}_{course}_{grp}"
            )
        )
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    keyboard.append(
        [
            InlineKeyboardButton(
                text="⬅ Назад до курсів", callback_data=f"spec_{faculty}_{spec_code}"
            )
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_menu_kb(faculty, spec_code, course):
    keyboard = [
        [
            InlineKeyboardButton(
                text="🔄 Глянути інший розклад",
                callback_data=f"course_{faculty}_{spec_code}_{course}",
            )
        ],
        [
            InlineKeyboardButton(
                text="🟢 Вільні аудиторії", callback_data="menu_free_rooms"
            ),
            InlineKeyboardButton(text="🗺 Карта корпусів", callback_data="menu_map"),
        ],
        [
            InlineKeyboardButton(
                text="📚 Навчальна програма", callback_data="menu_program"
            ),
            InlineKeyboardButton(text="⚙ Налаштування", callback_data="menu_settings"),
        ],
        [
            InlineKeyboardButton(
                text="📊 Розрахунковий комплекс", callback_data="menu_complex"
            )
        ],
        [
            InlineKeyboardButton(
                text="💬 Зворотний зв'язок", callback_data="menu_feedback"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔙 Назад до груп",
                callback_data=f"course_{faculty}_{spec_code}_{course}",
            )
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# ============================================================
# ОБРОБНИКИ
# ============================================================
@dp.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer(
        "Вітаю в боті розкладу КНУБА!\n\nКрок 1. Оберіть факультет:",
        reply_markup=get_faculties_kb(),
    )


@dp.callback_query(F.data.startswith("fac_"))
async def faculty_callback(callback: CallbackQuery):
    faculty = callback.data.split("_")[1]
    try:
        await callback.message.edit_text(
            f"🏛 Факультет: <b>{faculty}</b>\n\nКрок 2. Оберіть спеціальність:",
            reply_markup=get_specialties_kb(faculty),
            parse_mode="HTML",
        )
    except TelegramBadRequest:
        pass
    await callback.answer()


@dp.callback_query(F.data.startswith("spec_"))
async def specialty_callback(callback: CallbackQuery):
    _, faculty, code = callback.data.split("_", 2)
    spec_name = FACULTIES[faculty][code]
    try:
        await callback.message.edit_text(
            f"🏛 Факультет: {faculty}\n🎓 Спеціальність: <b>{code} — {spec_name}</b>\n\nКрок 3. Оберіть курс навчання:",
            reply_markup=get_courses_kb(faculty, code),
            parse_mode="HTML",
        )
    except TelegramBadRequest:
        pass
    await callback.answer()


@dp.callback_query(F.data.startswith("course_"))
async def course_callback(callback: CallbackQuery):
    _, faculty, code, course = callback.data.split("_", 3)
    try:
        await callback.message.edit_text(
            f"🏛 Факультет: {faculty}\n🎓 Спеціальність: {code}\n📚 Курс: <b>{course} курс</b>\n\nКрок 4. Оберіть групу:",
            reply_markup=get_groups_kb(code, faculty, course),
            parse_mode="HTML",
        )
    except TelegramBadRequest:
        pass
    await callback.answer()


@dp.callback_query(F.data.startswith("grp_"))
async def group_callback(callback: CallbackQuery):
    data = callback.data[4:]
    parts = data.split("_")
    faculty = parts[0]
    spec_code = parts[1]
    course = parts[2]
    group = parts[3]

    if group == "КСМ – 24":
        text = f"✅ Ви успішно обрали: 👥 Група: <b>{group}</b>\n\n{KSM_24_SCHEDULE}"
    elif group == "КСМ – 25":
        text = f"✅ Ви успішно обрали: 👥 Група: <b>{group}</b>\n\n{KSM_25_SCHEDULE}"
    else:
        text = f"✅ Ви успішно обрали: 👥 Група: <b>{group}</b>\n\n📅 Розклад для цієї групи буде підвантажено найближчим часом!"

    if callback.message.photo:
        await callback.message.delete()
        await callback.message.answer(
            text,
            reply_markup=get_menu_kb(faculty, spec_code, course),
            parse_mode="HTML",
        )
    else:
        try:
            await callback.message.edit_text(
                text,
                reply_markup=get_menu_kb(faculty, spec_code, course),
                parse_mode="HTML",
            )
        except TelegramBadRequest as e:
            print(f"Помилка редагування: {e}")
    await callback.answer()


@dp.callback_query(F.data == "menu_map")
async def menu_map_callback(callback: CallbackQuery):
    back_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔙 Назад до меню", callback_data="grp_ФАІТ_F7_3_КСМ – 25"
                )
            ]
        ]
    )

    # ТОЧНА НАЗВА ВАШОГО ФАЙЛУ ЗІ СКРІНШОТА
    exact_filename = "photo_2026_09_30_21_24_41.jpg"

    # Перевіряємо шлях у папці зі скриптом
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, exact_filename)

    if os.path.exists(file_path):
        photo_file = FSInputFile(file_path)
        try:
            await callback.message.delete()
            await callback.message.answer_photo(
                photo=photo_file,
                caption=CAMPUS_MAP_CAPTION,
                reply_markup=back_kb,
                parse_mode="HTML",
            )
        except Exception as e:
            print(f"Помилка надсилання фото карти: {e}")
            await callback.message.answer(
                CAMPUS_MAP_CAPTION, reply_markup=back_kb, parse_mode="HTML"
            )
    else:
        await callback.message.answer(
            f"⚠ Файл <b>{exact_filename}</b> не знайдено в папці з ботом.\n"
            f"Переконайтеся, що файл лежить у тій самій папці, де й цей скрипт (шлях: {script_dir}).\n\n"
            + CAMPUS_MAP_CAPTION,
            reply_markup=back_kb,
            parse_mode="HTML",
        )
    await callback.answer()


@dp.callback_query(F.data.startswith("menu_"))
async def menu_actions_callback(callback: CallbackQuery):
    action = callback.data.split("_")[1]
    if action == "map":
        return
    texts = {
        "free_rooms": "🟢 Функція пошуку вільних аудиторій у розробці.",
        "program": (
            "📚 Навчальну програму можна переглянути на офіційному сайті"
            " університету."
        ),
        "settings": "⚙ Налаштування сповіщень та формату розкладу.",
        "complex": "📊 Розрахунковий комплекс КНУБА.",
        "feedback": "💬 Для зв'язку з адміністратором пишіть у підтримку.",
    }
    await callback.answer(texts.get(action, "Розділ у розробці"), show_alert=True)


@dp.callback_query(F.data == "back_fac")
async def back_to_faculties(callback: CallbackQuery):
    if callback.message.photo:
        await callback.message.delete()
        await callback.message.answer(
            "Вітаю в боті розкладу КНУБА!\n\nКрок 1. Оберіть факультет:",
            reply_markup=get_faculties_kb(),
        )
    else:
        try:
            await callback.message.edit_text(
                "Вітаю в боті розкладу КНУБА!\n\nКрок 1. Оберіть факультет:",
                reply_markup=get_faculties_kb(),
            )
        except TelegramBadRequest:
            pass
    await callback.answer()


@dp.callback_query(F.data.startswith("back_spec_"))
async def back_to_specialties(callback: CallbackQuery):
    faculty = callback.data.split("_")[2]
    if callback.message.photo:
        await callback.message.delete()
        await callback.message.answer(
            f"🏛 Факультет: <b>{faculty}</b>\n\nКрок 2. Оберіть спеціальність:",
            reply_markup=get_specialties_kb(faculty),
            parse_mode="HTML",
        )
    else:
        try:
            await callback.message.edit_text(
                f"🏛 Факультет: <b>{faculty}</b>\n\nКрок 2. Оберіть спеціальність:",
                reply_markup=get_specialties_kb(faculty),
                parse_mode="HTML",
            )
        except TelegramBadRequest:
            pass
    await callback.answer()


# ============================================================
# ЗАПУСК
# ============================================================
async def main():
    bot = Bot(token=TOKEN)
    print("Бот успішно запущено!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
