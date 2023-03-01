import discord
import typing
import datetime

if typing.TYPE_CHECKING:
    from ..bot import Bot

class Record(discord.Cog):
    def __init__(self, bot: "Bot") -> None:
        self.bot = bot
        super().__init__()
    
    async def after_recording(self, sink: discord.sinks.WaveSink, channel: discord.VoiceChannel):
        file = [discord.File(audio.file, f"{user_id}.{sink.encoding}") for user_id, audio in sink.audio_data.items()]
        await channel.send("Here is your recording.", files=file)


    @discord.command()
    async def record(self, ctx: discord.ApplicationContext):
        voice = ctx.author.voice

        if not voice:
            return await ctx.respond("You are not in a voice channel. Please connect to one and try again.")
        
        vc = await voice.channel.connect()
        self.bot.connections.update({ctx.guild.id: {"vc": vc, "time": datetime.datetime.now()}})

        vc.start_recording(
            discord.sinks.WaveSink(
            filters={"max_size": 25000000}
            ),
            self.after_recording,
            vc.channel
        )

        await ctx.respond("Recording started. Use `/stop` to stop recording.")

    @discord.command()
    async def stop(self, ctx: discord.ApplicationContext):
        if ctx.guild.id not in self.bot.connections:
            return await ctx.respond("There is no recording in progress.")
        
        vc = self.bot.connections[ctx.guild.id]["vc"]
        vc.stop_recording()
        await ctx.respond("Recording stopped. Use `/play` to play the recording.")




def setup(bot: "Bot"):
    bot.add_cog(Record(bot))