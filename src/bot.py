import discord
import os
import dotenv

dotenv.load_dotenv()

class Bot(discord.Bot):
    def __init__(self):
        ...
    
    def load_extensions(self):
        self.load_extensions("cogs.record")

    def run():
        bot.load_extensions()
        super().run(os.getenv("TOKEN"))

if __name__ == "__main__":
    bot = Bot()
    bot.run()