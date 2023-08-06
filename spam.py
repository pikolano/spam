from .. import loader, utils
from asyncio import sleep, gather


def register(cb):
    cb(SpamMod())

class SpamMod(loader.Module):
    """Спам-модуль"""
    strings = {'name': 'Spam'}

    async def spamcmd(self, message):
        """<кол-во сообщений> <текст или реплай>."""
        try:
            await message.delete()
            args = utils.get_args(message)
            count = int(args[0].strip())
            reply = await message.get_reply_message()
            if reply:
                if reply.media:
                    for _ in range(count):
                        await message.client.send_file(message.to_id, reply.media)
                    return
                else:
                    for _ in range(count):
                        await message.client.send_message(message.to_id, reply)
            else:
                message.message = " ".join(args[1:])
                for _ in range(count):
                    await gather(*[message.respond(message)])
        except: return await message.client.send_message(message.to_id, '.spam <кол-во:int> <текст или реплай>.')