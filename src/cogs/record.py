import discord
import typing
import datetime
import pydub
import soundfile as sf
import numpy as np

if typing.TYPE_CHECKING:
    from ..bot import Bot

class Record(discord.Cog):
    def __init__(self, bot: "Bot") -> None:
        self.bot = bot
        super().__init__()
    
    async def after_recording(self, sink: discord.sinks.WaveSink, channel: discord.VoiceChannel):

        
        audio_data = []
        for _, audio in sink.audio_data.items:
            audio_data.append(audio)
        audio_data = np.concatenate(audio_data)
        sf.write("recording.wav", audio_data, 48000)

        # Convert the audio segment to a pydub.AudioSegment
        audio_segment = pydub.AudioSegment.from_wav("recording.wav")

        # Send the audio segment to the channel the recording was started in
        await channel.send(file=discord.File(audio_segment.export("recording.mp3", format="mp3")))




    @discord.command()
    async def record(self, ctx: discord.ApplicationContext):
        voice = ctx.author.voice

        if not voice:
            return await ctx.respond("You are not in a voice channel. Please connect to"
                                     " one and try again.")
        
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

    @discord.command()
    async def disconnect(self, ctx: discord.ApplicationContext):
        if self.bot.connections.get(ctx.guild.id, None):
            await ctx.respond(embed=discord.Embed(
                title=":x: You have to stop recording before I can disconnect!",
                description="Please stop recording with the `/stop` command.",
                color=discord.Colors.red()
            ))
        
        elif not ctx.guild.voice_client:
            await ctx.respond(embed=discord.Embed(
                title=":x: I'm not connected to a voice channel!",
                description="I have to be in a voice channel before I can leave it.",
                color=discord.Colors.red()
            ))

        else:
            await ctx.guild.voice_client.disconnect()

            await ctx.respond(embed=discord.Embed(
                title=":white_check_mark: Disconnected!",
                description="Successfully disconnected from the voice channel.",
                color=discord.Colors.green()
            ))



def setup(bot: "Bot"):
    bot.add_cog(Record(bot))