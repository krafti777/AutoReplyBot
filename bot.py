import asyncio

import aiogram.types.inline_keyboard_markup
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
API_TOKEN = ''

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
is_admin = False

button_list = []

awaiting_id = 0
awaiting = False
new_text = ""
old_text = ""

wait_for_name = False
wait_for_opis = False
@dp.message(Command("edit"))
async def edit_handler(message:Message):
    print(message.from_user.id)
    if message.from_user.id == 1140762480 or message.from_user.id == 1140762480 or message.from_user.id == 1629184963:
        global button_list
        str_list = "id | triger | text "
        with open("triger_database.txt", "r") as fl:
            trigers = fl.read().split("\n")
            for i in range(len(trigers)):
                key, val = trigers[i].strip().split(":::")
                str_list += f"\n{i} | {key} | {val[:20]}..."
                button_list.append(i)

            inline_keyboard = []
            for i in range(0, len(button_list), 7):
                row = [types.InlineKeyboardButton(text=str(text), callback_data=str(text)) for text in
                       button_list[i:i + 7]]
                inline_keyboard.append(row)

            inline_keyboard.append([types.InlineKeyboardButton(text="Create", callback_data="Create")])
            kb = types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

            button_list.clear()


            fl.close()

            await message.reply(str_list,reply_markup=kb)

    else:
        await message.reply("You don't have acess")


@dp.callback_query()
async def handle_callback_query(callback_query: types.CallbackQuery):
    global button_list,awaiting,new_text,awaiting_id,old_text,wait_for_name,wait_for_opis
    button_id = callback_query.data

    if "Change" in callback_query.data:
        id = int(callback_query.data.replace("Change",""))
        kb = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text="Delele Triger", callback_data=f"Del{id}"),types.InlineKeyboardButton(text="Change text", callback_data=f"TextReWork{id}")]])
        await callback_query.message.answer("What to u want to change?",reply_markup=kb)

    elif "Del" in callback_query.data:
        id = int(callback_query.data.replace("Del", ""))
        with open("triger_database.txt", "r+") as fl:
            trigers = fl.readlines()
            del trigers[id]
            # fl.truncate()

        with open("triger_database.txt", "w") as flt:
            flt.writelines(trigers)
            await callback_query.message.answer("Deleted successfully")

        with open("triger_database.txt", "r+") as fls:
            cont = fls.read()
            if cont.endswith("\n"):
                cont = cont[:-1]

        with open("triger_database.txt", "w") as fld:
            fld.write(cont)

    elif "TextReWork" in callback_query.data:
        awaiting_id = int(callback_query.data.replace("TextReWork", ""))
        await callback_query.message.answer("Enter here your text:")
        awaiting = True

        with open("triger_database.txt", "r") as fl:
            trigers = fl.read().split("\n")
            fl.close()
        for i in range(len(trigers)):
            if int(awaiting_id) == i:
                key, val = str(trigers[i]).split(":::")
                old_text = val


    elif "Create" == callback_query.data:
        await callback_query.message.answer("Enter triger")
        wait_for_name = True

    else:
        with open("triger_database.txt", "r") as fl:
            trigers = fl.read().split("\n")
            fl.close()

        key = "";val="";kb=""
        for i in range(len(trigers)):
            if int(button_id) == i:
                key,val = str(trigers[i]).split(":::")
                kb = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text="Change", callback_data=f"Change{i}")]])

        await callback_query.message.answer(f"triger: {key}\nfull text: {val.replace('_',' ')}",reply_markup=kb)






triger_name = "";triger_text = ""
@dp.message()
async def handle_message(message: Message):
    global is_admin,awaiting,new_text,awaiting_id,old_text,wait_for_name,wait_for_opis,triger_text,triger_name
    if awaiting:
        new_text = message.text.replace("\n", "").replace(" ", "_")
        with open("triger_database.txt", "r+") as fl:
            trigers = fl.read()
            t = (trigers.replace(old_text,new_text))

        with open("triger_database.txt", "w") as fls:
            fls.write(t)
        awaiting = False

    elif wait_for_name:
        triger_name = (message.text).replace(" ","_").lower()
        wait_for_opis = True
        await message.answer("Enter triger answer")

        wait_for_name = False

    elif wait_for_opis:
        triger_text = message.text.replace(" ","_").replace("\n",r"\n")
        print(triger_text)
        await message.answer("Succesfully added")
        wait_for_opis = False

        with open("triger_database.txt", "a",encoding="utf-8") as fl:
            new_element = f"\n{triger_name}:::{triger_text}"
            fl.write(new_element)

    else:
        with open("triger_database.txt", "r",encoding="utf-8") as fl:
            trigers = fl.read().split("\n")
            for el in trigers:
                key,val = el.split(":::")

                if str(key).replace("_"," ") in message.text.lower():
                    await message.reply(str(val).replace("_"," ").replace(r"\n","\n"))


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
