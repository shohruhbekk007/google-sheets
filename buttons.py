from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

def get_text(language, text_key):
    texts = {
        'uz': {
            'greeting': "Assalomu alaykum {name}\nQaysi tildan foydalanmoqchisiz?",
            'enter_fullname': "Ismingiz va familiyangizni kiriting:",
            'enter_age': "Yoshingizni kiriting:",
            'enter_phone': "Iltimos, telefon raqamingizni yuboring:",
            'enter_photo': "Passport rasmingizni yuboring:",
            'confirm': "Ism: {fullname}\nYosh: {age}\nTelefon: {tel}",
            'only_photo': "Faqat rasm yuboring.",
            'approved': "Tasdiqlandi",
            'retry': "Boshqatdan harakat qiling",
            'confirm_btn': "Tasdiqlash ✅",
            'cancel_btn': "Bekor qilish ❌",
            'contact_btn': "Kontaktni yuborish ☎️",
            'uz_lang': "uz 🇺🇿",
            'ru_lang': "ru 🇷🇺"
        },
        'ru': {
            'greeting': "Здравствуйте {name}\nКакой язык вы хотите использовать?",
            'enter_fullname': "Введите ваше имя и фамилию:",
            'enter_age': "Введите ваш возраст:",
            'enter_phone': "Пожалуйста, отправьте ваш номер телефона:",
            'enter_photo': "Отправьте фото вашего паспорта:",
            'confirm': "Имя: {fullname}\nВозраст: {age}\nТелефон: {tel}",
            'only_photo': "Отправьте только фото.",
            'approved': "Подтверждено",
            'retry': "Попробуйте снова",
            'confirm_btn': "Подтвердить ✅",
            'cancel_btn': "Отменить ❌",
            'contact_btn': "Отправить контакт ☎️",
            'uz_lang': "uz 🇺🇿",
            'ru_lang': "ru 🇷🇺"
        }
    }
    return texts[language].get(text_key, text_key)


def get_confirm_keyboard(language):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=get_text(language, 'confirm_btn'), callback_data="tasdiqlash"),
                InlineKeyboardButton(text=get_text(language, 'cancel_btn'), callback_data="bekor")
            ]
        ]
    )


def get_contact_keyboard(language):
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_text(language, 'contact_btn'), request_contact=True)]
        ],
        resize_keyboard=True
    )



Til = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=get_text('uz', 'uz_lang'), callback_data="uz")],
        [InlineKeyboardButton(text=get_text('ru', 'ru_lang'), callback_data="ru")]
    ]
)
