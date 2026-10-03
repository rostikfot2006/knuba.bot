import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, FSInputFile
from aiogram.exceptions import TelegramBadRequest

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
    "A5": ["ПО-26", "ПО-25", "ПО-24", "ПО-23", "ПО-22", "ПО-21", "ПО(ск)-25", "ПО(ск)-24", "ПОм-26", "ПОм-25"],
    "F2": ["ІПЗ-26", "ІПЗ-25", "ІПЗ-24", "ІПЗ-23", "ІПЗ-22", "ІПЗ-21", "ІПЗ(ск)-25", "ІПЗ(ск)-24", "ІПЗм-26", "ІПЗм-25"],
    "F3": ["КН-26", "КН-25", "КН-24", "КН-23", "КН-22", "КН-21", "КН(ск)-25", "КН(ск)-24", "КНм-26", "КНм-25"],
    "F5": ["КБ-26", "КБ-25", "КБ-24", "КБ-23", "КБ-22", "КБ-21", "КБ(ск)-25", "КБм-26", "КБм-25"],
    "F6": ["ІСТ-26", "ІСТ-25", "ІСТ-24", "ІСТ-23", "ІСТ-22", "ІСТ-21", "ІСТ(ск)-25", "ІСТм-26", "ІСТм-25"],
    "F7": ["КСМ-26", "КСМ-25", "КСМ-24", "КСМ-23", "КСМ-22", "КСМ-21", "КСМ(ск)-25", "КСМ(ск)-24", "КСМм-26", "КСМм-25"],
    "G3": ["ЕЛ-26", "ЕЛ-25", "ЕЛ-24", "ЕЛ-23", "ЕЛ-22", "ЕЛ-21", "ЕЛ(ск)-25", "ЕЛм-26", "ЕЛм-25"],
    "G4": ["ВДЕ-26", "ВДЕ-25", "ВДЕ-24", "ВДЕ-23", "ВДЕ-22", "ВДЕ-21", "ВДЕм-26", "ВДЕм-25"],
    "G7": ["АКТ-26", "АКТ-25", "АКТ-24", "АКТ-23", "АКТ-22", "АКТ-21", "АКТм-26", "АКТм-25"],
    "G9": ["ПМ-26", "ПМ-25", "ПМ-24", "ПМ-23", "ПМ-22", "ПМ-21", "ПМм-26", "ПМм-25"],
    "G11": ["МШ-26", "МШ-25", "МШ-24", "МШ-23", "МШ-22", "МШ-21", "МШм-26", "МШм-25"],
    "D8": ["БМП-26", "БМП-25", "БМП-24", "БМП-23", "БМПм-26", "БМПм-25"],
    "D4": ["ДП-26", "ДП-25", "ДП-24", "ДП-23", "ДПм-26", "ДПм-25"],
    "B2": ["ДІЗ-26", "ДІЗ-25", "ДІЗ-24", "ДІЗ-23", "ДІЗ-22", "ДІЗ-21", "ДІЗм-26", "ДІЗм-25"],
    "G17": ["АРХ-26", "АРХ-25", "АРХ-24", "АРХ-23", "АРХ-22", "АРХ-21", "АРХ(ск)-25", "АРХм-26", "АРХм-25"],
    "C1": ["ЕК-26", "ЕК-25", "ЕК-24", "ЕК-23", "ЕК-22", "ЕК-21", "ЕКм-26", "ЕКм-25"],
    "D1": ["ОО-26", "ОО-25", "ОО-24", "ОО-23", "ОО-22", "ОО-21", "ООм-26", "ООм-25"],
    "D3": ["МН-26", "МН-25", "МН-24", "МН-23", "МН-22", "МН-21", "МНм-26", "МНм-25"],
    "G19": ["ЦБ-26", "ПЦБ-26", "ЦБ-25", "ПЦБ-25", "ЦБ-24", "ПЦБ-24", "ЦБ-23", "ПЦБ-23", "ЦБ-22", "ПЦБ-22", "ЦБ-21", "ПЦБ-21", "ПЦБ(ск)-25", "ЦБм-26", "ПЦБм-26"],
    "D5": ["МРК-26", "МРК-25", "МРК-24", "МРК-23", "МРК-22", "МРК-21", "МРКм-26", "МРКм-25"],
    "D7": ["ТОР-26", "ТОР-25", "ТОР-24", "ТОР-23", "ТОР-22", "ТОР-21", "ТОРм-26", "ТОРм-25"],
    "G1": ["ХТ-26", "ХТ-25", "ХТ-24", "ХТ-23", "ХТ-22", "ХТ-21", "ХТм-26", "ХТм-25"],
    "A7": ["ФКС-26", "ФКС-25", "ФКС-24", "ФКС-23", "ФКС-22", "ФКС-21", "ФКСм-26", "ФКСм-25"],
    "G18.1": ["ГД-26", "ГД-25", "ГД-24", "ГД-23", "ГД-22", "ГД-21", "ГД(ск)-25", "ГДм-26", "ГДм-25"],
    "G18.2": ["ГІС-26", "ГІС-25", "ГІС-24", "ГІС-23", "ГІСм-26", "ГІСм-25"],
    "E2": ["ЕКЛ-26", "ЕКЛ-25", "ЕКЛ-24", "ЕКЛ-23", "ЕКЛ-22", "ЕКЛ-21", "ЕКЛм-26", "ЕКЛм-25"],
    "G2": ["ТЗНС-26", "ТЗНС-25", "ТЗНС-24", "ТЗНС-23", "ТЗНС-22", "ТЗНС-21", "ТЗНСм-26", "ТЗНСм-25"],
    "G4.02": ["ТПЕ-26", "ТПЕ-25", "ТПЕ-24", "ТПЕ-23", "ТПЕ-22", "ТПЕ-21", "ТПЕм-26", "ТПЕм-25"],
    "G16": ["НГІ-26", "НГІ-25", "НГІ-24", "НГІ-23", "НГІ-22", "НГІ-21", "НГІм-26", "НГІм-25"],
}

KSM_24_SCHEDULE = """📅 Розклад для групи КСМ-24 (Жовтень 2026):

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

KSM_25_SCHEDULE = """📅 Розклад для групи КСМ-25 (Жовтень 2026):

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
        [InlineKeyboardButton(text="ФАІТ", callback_data="fac_ФАІТ"),
         InlineKeyboardButton(text="ФУПП", callback_data="fac_ФУПП")],
        [InlineKeyboardButton(text="АРХ", callback_data="fac_АРХ"),
         InlineKeyboardButton(text="БФ", callback_data="fac_БФ")],
        [InlineKeyboardButton(text="БТФ", callback_data="fac_БТФ"),
         InlineKeyboardButton(text="ГІСУТ", callback_data="fac_ГІСУТ")],
        [InlineKeyboardButton(text="ФІСЕ", callback_data="fac_ФІСЕ")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_specialties_kb(faculty):
    keyboard = []
    for code, name in FACULTIES[faculty].items():
        keyboard.append([InlineKeyboardButton(text=f"{code} — {name}", callback_data=f"spec_{faculty}_{code}")])
    keyboard.append([InlineKeyboardButton(text="⬅️ Назад до факультетів", callback_data="back_fac")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_courses_kb(faculty, spec_code):
    keyboard = [
        [InlineKeyboardButton(text="1 курс", callback_data=f"course_{faculty}_{spec_code}_1"),
         InlineKeyboardButton(text="2 курс", callback_data=f"course_{faculty}_{spec_code}_2")],
        [InlineKeyboardButton(text="3 курс", callback_data=f"course_{faculty}_{spec_code}_3"),
         InlineKeyboardButton(text="4 курс", callback_data=f"course_{faculty}_{spec_code}_4")],
        [InlineKeyboardButton(text="5 курс (Магістратура)", callback_data=f"course_{faculty}_{spec_code}_5"),
         InlineKeyboardButton(text="6 курс (Магістратура)", callback_data=f"course_{faculty}_{spec_code}_6")],
        [InlineKeyboardButton(text="⬅️ Назад до спеціальностей", callback_data=f"back_spec_{faculty}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_groups_kb(spec_code, faculty, course):
    all_groups = GROUPS.get(spec_code, [])
    filtered_groups = []
    for grp in all_groups:
        if course in ["5", "6"]:
            if "м" in grp.lower():
                filtered_groups.append(grp)
        else:
            if "м" not in grp.lower():
                filtered_groups.append(grp)

    if not filtered_groups:
        filtered_groups = all_groups

    keyboard = []
    row = []
    for grp in filtered_groups:
        row.append(InlineKeyboardButton(text=grp, callback_data=f"grp_{faculty}_{spec_code}_{course}_{grp}"))
        if len(row) == 3:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    keyboard.append([InlineKeyboardButton(text="⬅ Назад до курсів", callback_data=f"spec_{faculty}_{spec_code}")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_menu_kb(faculty, spec_code, course):
    keyboard = [
        [InlineKeyboardButton(text="🔄 Глянути інший розклад", callback_data=f"course_{faculty}_{spec_code}_{course}")],
        [InlineKeyboardButton(text="🟢 Вільні аудиторії", callback_data="menu_free_rooms"),
         InlineKeyboardButton(text="🗺 Карта корпусів", callback_data="menu_map")],
        [InlineKeyboardButton(text="📚 Навчальна програма", callback_data="menu_program"),
         InlineKeyboardButton(text="⚙ Налаштування", callback_data="menu_settings")],
        [InlineKeyboardButton(text="📊 Розрахунковий комплекс", callback_data="menu_complex")],
        [InlineKeyboardButton(text="💬 Зворотний зв'язок", callback_data="menu_feedback")],
        [InlineKeyboardButton(text="🔙 Назад до груп", callback_data=f"course_{faculty}_{spec_code}_{course}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# ============================================================
# ОБРОБНИКИ
# ============================================================
@dp.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer(
        "Вітаю в боті розкладу КНУБА!\n\nКрок 1. Оберіть факультет:",
        reply_markup=get_faculties_kb()
    )

@dp.callback_query(F.data.startswith("fac_"))
async def faculty_callback(callback: CallbackQuery):
    faculty = callback.data.split("_")[1]
    try:
        await callback.message.edit_text(
            f"🏛 Факультет: <b>{faculty}</b>\n\nКрок 2. Оберіть спеціальність:",
            reply_markup=get_specialties_kb(faculty),
            parse_mode="HTML"
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
            parse_mode="HTML"
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
            parse_mode="HTML"
        )
    except TelegramBadRequest:
        pass
    await callback.answer()

@dp.callback_query(F.data.startswith("grp_"))
async def group_callback(callback: CallbackQuery):
    parts = callback.data.split("_")
    faculty = parts[1]
    spec_code = parts[2]
    course = parts[3]
    group = parts[4]

    if group == "КСМ-24":
        text = f"✅ Ви успішно обрали: 👥 Група: <b>{group}</b>\n\n{KSM_24_SCHEDULE}"
    elif group == "КСМ-25":
        text = f"✅ Ви успішно обрали: 👥 Група: <b>{group}</b>\n\n{KSM_25_SCHEDULE}"
    else:
        text = f"✅ Ви успішно обрали: 👥 Група: <b>{group}</b>\n\n📅 Розклад для цієї групи буде підвантажено найближчим часом!"

    if callback.message.photo:
        await callback.message.delete()
        await callback.message.answer(
            text,
            reply_markup=get_menu_kb(faculty, spec_code, course),
            parse_mode="HTML"
        )
    else:
        try:
            await callback.message.edit_text(
                text,
                reply_markup=get_menu_kb(faculty, spec_code, course),
                parse_mode="HTML"
            )
        except TelegramBadRequest as e:
            print(f"Помилка редагування: {e}")
    await callback.answer()

@dp.callback_query(F.data == "menu_map")
async def menu_map_callback(callback: CallbackQuery):
    back_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад до меню", callback_data="grp_ФАІТ_F7_3_КСМ-25")]
    ])
    
    filename = "photo_2026-09-30_21-24-41.jpg"
    
    if os.path.exists(filename):
        photo_file = FSInputFile(filename)
        try:
            await callback.message.delete()
            await callback.message.answer_photo(
                photo=photo_file,
                caption=CAMPUS_MAP_CAPTION,
                reply_markup=back_kb,
                parse_mode="HTML"
            )
        except Exception as e:
            print(f"Помилка надсилання фото карти: {e}")
            await callback.message.answer(
                CAMPUS_MAP_CAPTION,
                reply_markup=back_kb,
                parse_mode="HTML"
            )
    else:
        print(f"УВАГА: Файл {filename} не знайдено в папці скрипта!")
        await callback.message.answer(
            "⚠️ Файл зображення карти не знайдено на сервері.\n\n" + CAMPUS_MAP_CAPTION,
            reply_markup=back_kb,
            parse_mode="HTML"
        )
    await callback.answer()

@dp.callback_query(F.data.startswith("menu_"))
async def menu_actions_callback(callback: CallbackQuery):
    action = callback.data.split("_")[1]
    if action == "map":
        return
    texts = {
        "free_rooms": "🟢 Функція пошуку вільних аудиторій у розробці.",
        "program": "📚 Навчальну програму можна переглянути на офіційному сайті університету.",
        "settings": "⚙ Налаштування сповіщень та формату розкладу.",
        "complex": "📊 Розрахунковий комплекс КНУБА.",
        "feedback": "💬 Для зв'язку з адміністратором пишіть у підтримку."
    }
    await callback.answer(texts.get(action, "Розділ у розробці"), show_alert=True)

@dp.callback_query(F.data == "back_fac")
async def back_to_faculties(callback: CallbackQuery):
    if callback.message.photo:
        await callback.message.delete()
        await callback.message.answer(
            "Вітаю в боті розкладу КНУБА!\n\nКрок 1. Оберіть факультет:",
            reply_markup=get_faculties_kb()
        )
    else:
        try:
            await callback.message.edit_text(
                "Вітаю в боті розкладу КНУБА!\n\nКрок 1. Оберіть факультет:",
                reply_markup=get_faculties_kb()
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
            parse_mode="HTML"
        )
    else:
        try:
            await callback.message.edit_text(
                f"🏛 Факультет: <b>{faculty}</b>\n\nКрок 2. Оберіть спеціальність:",
                reply_markup=get_specialties_kb(faculty),
                parse_mode="HTML"
            )
        except TelegramBadRequest:
            pass
    await callback.answer()

# ============================================================
# ЗАПУСК
# ============================================================
async def main():
    bot = Bot(token=TOKEN)
    print("Бот успішно запущено з новим токеном!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
