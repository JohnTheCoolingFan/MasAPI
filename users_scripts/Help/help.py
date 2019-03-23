import discord
import datetime
import time
from discord.ext import commands

from functions.message_maker import send_help_message
from functions.message_maker import send_warn_message


class Help:
    def __init__(self, client):
        client.remove_command('help')
        self.client = client

    @commands.command(pass_context=True)
    @commands.cooldown(2, 1)
    async def help(self, ctx, *args):
        """
        .help [command] - shows this message or shows help about [command]
        """
        if len(args) == 0:
            command = []
            docs = []
            for name in self.client.commands:
                command.append(name)
                if self.client.commands[name].short_doc != '':
                    docs.append(self.client.commands[name].short_doc)
                else:
                    docs.append("This commands doesn't have help")
            await send_help_message(self.client, discord.Object(id=ctx.message.channel.id), ctx.message.author, 'Help',
                                    command, docs, wrapper_icon=self.client.user.avatar_url)
        elif len(args) == 1:
            if args[0] in self.client.commands:
                embed = discord.Embed(colour=discord.Colour(0xff8000),
                                      timestamp=datetime.datetime.utcfromtimestamp(int(time.time())))

                embed.set_footer(text='Help', icon_url=self.client.user.avatar_url)
                embed.add_field(name=r"❓️  | " + ctx.message.author.name, value='Hi there!')

                embed.add_field(name=args[0], value=self.client.commands[args[0]].help)

                await send_help_message(self.client, ctx.message.author, ctx.message.author, 'Help',
                                        embed=embed, wrapper_icon=self.client.user.avatar_url)
            else:
                error_message = "This command doesn't exist."
                await send_warn_message(self.client, discord.Object(id=ctx.message.channel.id),
                                        ctx.message.author, 'Help',
                                        error=error_message,
                                        wrapper_icon=self.client.user.avatar_url)
        else:
            error_message = 'You must choose one command'
            await send_warn_message(self.client, discord.Object(id=ctx.message.channel.id),
                                    ctx.message.author, 'Help',
                                    error=error_message,
                                    wrapper_icon=self.client.user.avatar_url)
