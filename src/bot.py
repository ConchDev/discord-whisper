import discord
import os
import dotenv

dotenv.load_dotenv()

class Bot(discord.Bot):
    def __init__(self):
        super().__init__(debug_guilds=[733467617804812409])
        self._connections = {}
    
    @property
    def connections(self):
        return self._connections
    
    def load_cogs(self):
        self.load_extension("cogs.record")

    def run(self):
        bot.load_cogs()
        super().run(os.getenv("TOKEN"))

if __name__ == "__main__":
    bot = Bot()
    bot.run()