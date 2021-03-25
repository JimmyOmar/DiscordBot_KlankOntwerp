import discord
import random
import os
from discord.ext import commands, tasks
from itertools import cycle
import json
import argparse
import random
import time

from pythonosc import udp_client

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1",
        help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=5005,
        help="The port the OSC server is listening on")
    args = parser.parse_args()

    intents = discord.Intents.default()
    intents.members = True
    client = commands.Bot(command_prefix = '.')
    client2 = udp_client.SimpleUDPClient(args.ip, args.port)
    status = cycle(['Status 1', 'Status 2'])

    #Startup Status
    @client.event
    async def on_ready():
            await client.change_presence(status=discord.Status.idle, activity=discord.Game('Mick Broer'))
            change_status.start()
            print('Bot is online.')

    #Load Cogs
    @client.command()
    async def load(ctx, extension):
        client.load_extension(f'cogs.{extension}')

    #Unload Cogs
    @client.command()
    async def unload(ctx, extension):
        client.unload_extension(f'cogs.{extension}')

    #Reload Cogs
    @client.command()
    async def reload(ctx, extension):
        client.unload_extension(f'cogs.{extension}')
        client.load_extension(f'cogs.{extension}')

    @client.command()
    async def rate(ctx, *, oscMessage):
        client2.send_message("/rate", oscMessage)
        await ctx.send(oscMessage)

    @client.command()
    async def buf(ctx, *, oscMessage):
        client2.send_message("/buf", oscMessage)
        await ctx.send(oscMessage)

    @client.command()
    async def AM(ctx, *, oscMessage):
        client2.send_message("/AM", oscMessage)
        await ctx.send(oscMessage)

    # Clear messages
    @client.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(ctx, amount=5):
        await ctx.channel.purge(limit=amount + 1)

    # Kick a user
    @client.command()
    @commands.has_permissions(manage_messages=True)
    async def kick(ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'Kicked {member.mention}.')

    # Ban a user
    @client.command()
    @commands.has_permissions(manage_messages=True)
    async def ban(ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'Kicked {member.mention}.')

    def is_it_me(ctx):
        return ctx.author.id == 392753785098731520

    @client.command()
    @commands.check(is_it_me)
    async def itis(ctx):
        await ctx.send(f'Hi im {ctx.author}')

    # Unban a user
    @client.command()
    async def unban(ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.mention}')
                return

    #Change status
    @tasks.loop(seconds=10)
    async def change_status():
        await client.change_presence(activity=discord.Game(next(status)))

    #Error message
    @client.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send('Invalid command used.')

    # Close the bot
    @client.command(aliases=["quit"])
    @commands.has_permissions(administrator=False)
    async def close(ctx):
        await ctx.send(f'Bot is offline')  # This is optional, but it is there to tell you.
        await client.close()

    client.run('ODA4MDA5MDU3MzA1NzU1NjY4.YCATEw.X6ebRWMYGkdncS9F8ougsl9o8FE')
