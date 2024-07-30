from copy import deepcopy

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery

from Bookbot.database.database import user_dict_template, users_db
from Bookbot.filters.filters import IsDigitCallbackData, IsDelBookmarkCallbackData
from Bookbot.keyboards import bookmarks_kb, pagination_kb
from Bookbot.lexicon.lexicon import LEXICON
from Bookbot.services.file_handling import book

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    if message.from_user.id not in users_db.keys():
        users_db.setdefault(deepcopy(message.from_user.id), user_dict_template)
    await message.answer(text=LEXICON['/start'],
                         parse_mode=ParseMode.MARKDOWN)


@router.message(Command(commands='help'))
async def help_handler(message: Message):
    await message.answer(text=LEXICON['/help'])


@router.message(Command(commands='beginning'))
async def beginning_handler(message: Message):
    text = book[users_db[message.from_user.id]['page']]
    await message.answer(text=text,
                         reply_markup=pagination_kb.create_pagination_keyboard(
                             LEXICON['backward'],
                             f'{users_db[message.from_user.id]["page"]} / {len(book)}',
                             LEXICON['forward']
                         ))


@router.message(Command(commands='continue'))
async def continue_handler(message: Message):
    text = book[users_db[message.from_user.id]['page']]
    await message.answer(text=text,
                         reply_markup=pagination_kb.create_pagination_keyboard(
                             LEXICON['backward'],
                             f'{users_db[message.from_user.id]["page"]} / {len(book)}',
                             LEXICON['forward']
                         ))


@router.message(Command(commands='bookmarks'))
async def bookmarks_handler(message: Message):
    if users_db[message.from_user.id]['bookmarks']:
        await message.answer(text=LEXICON[message.text],
                             reply_markup=bookmarks_kb.create_bookmarks_keyboard(
                                 *users_db[message.from_user.id]['bookmarks']
                             ))
    else:
        await message.answer(text=LEXICON['no_bookmarks'])


@router.callback_query(F.data == LEXICON['forward'])
async def forward_handler(callback_query: CallbackQuery):

    if users_db[callback_query.from_user.id]['page'] < len(book):
        users_db[callback_query.from_user.id]['page'] += 1
    else:
        await callback_query.answer(text='Это конец книги')
    text = book[users_db[callback_query.from_user.id]['page']]

    await callback_query.message.edit_text(text=text,
                                reply_markup=pagination_kb.create_pagination_keyboard(
                                    LEXICON['backward'],
                                    f'{users_db[callback_query.from_user.id]["page"]} / {len(book)}',
                                    LEXICON['forward']
                                ))
    await callback_query.answer()


@router.callback_query(F.data == LEXICON['backward'])
async def forward_handler(callbak_query: CallbackQuery):
    if users_db[callbak_query.from_user.id]['page'] > 1:
        users_db[callbak_query.from_user.id]['page'] -= 1

    text = book[users_db[callbak_query.from_user.id]['page']]
    await callbak_query.message.edit_text(text=text,
                               reply_markup=pagination_kb.create_pagination_keyboard(
                                   LEXICON['backward'],
                                   f'{users_db[callbak_query.from_user.id]["page"]} / {len(book)}',
                                   LEXICON['forward']
                               ))


@router.callback_query(lambda x: '/' in x.data and x.data.replace(' / ', '').isdigit())
async def add_bookmarks(callback_query: CallbackQuery):
    users_db[callback_query.from_user.id]['bookmarks'].add(users_db[callback_query.from_user.id]['page'])

    await callback_query.answer(text='Страница добавлена')


@router.callback_query(IsDigitCallbackData())
async def get_bookmark(callback_query: CallbackQuery):
    users_db[callback_query.from_user.id]['page'] = int(callback_query.data)
    text = book[users_db[callback_query.from_user.id]['page']]
    await callback_query.message.edit_text(text=text,
                                reply_markup=pagination_kb.create_pagination_keyboard(
                                    LEXICON['backward'],
                                    f'{users_db[callback_query.from_user.id]["page"]} / {len(book)}',
                                    LEXICON['forward']
                                ))


@router.callback_query(F.data == 'edit_bookmarks')
async def edit_bookmarks(callback_query: CallbackQuery):
    await callback_query.message.edit_text(text=LEXICON[callback_query.data],
                                   reply_markup=bookmarks_kb.create_edit_keyboard(
                                       *users_db[callback_query.from_user.id]['bookmarks']
                                   ))


@router.callback_query(IsDelBookmarkCallbackData())
async def del_bookmarks(callback: CallbackQuery):
    users_db[callback.from_user.id]['bookmarks'].remove(
        int(callback.data[:-3])
    )
    if users_db[callback.from_user.id]['bookmarks']:
        await callback.message.edit_text(
            text=LEXICON['/bookmarks'],
            reply_markup=bookmarks_kb.create_edit_keyboard(
                *users_db[callback.from_user.id]["bookmarks"]
            )
        )
    else:
        await callback.message.edit_text(text=LEXICON['no_bookmarks'])


@router.callback_query(F.data == 'cancel')
async def cancel_bookmarks(callback_query: CallbackQuery):
    await callback_query.message.edit_text(text=LEXICON[callback_query.data])
