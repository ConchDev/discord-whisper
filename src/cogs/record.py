import discord
import typing

if typing.TYPE_CHECKING:
    from ..bot import Bot

class Record(discord.Cog):
    def __init__(self, bot: "Bot") -> None:
        self.bot = bot
        super().__init__()

def setup(bot: "Bot"):
    bot.add_cog(Record(bot))