import os
import json
import discord
from discord.ext import commands

from functions.embed_help import embed_help
from functions.server import get_server, edit_server, remove_server
from functions.setup import setup_server

client = commands.Bot(command_prefix='.')
client.remove_command('help')

with open(os.path.abspath('config/config.json'), 'r') as f:
    config = json.load(f)


@client.event
async def on_ready():
    print('Connected', client.user.name, client.user.id)


@client.command(pass_context=True)
async def bye(ctx, *args):
    if ctx.message.author.id == config['owner_id']:
        await client.logout()
        await client.close()


@client.command(pass_context=True)
@commands.cooldown(5, 1)
async def help(ctx, *args):
    server = get_server(ctx.message.server)
    if server['configured']:
        await client.send_message(discord.Object(id=ctx.message.channel.id), embed=embed_help(client, args))
    else:
        await client.send_message(discord.Object(id=ctx.message.channel.id),
                                  'You need to setup bot, send !setup in nsfw channel')


@client.command(pass_context=True)
@commands.cooldown(2, 1)
async def setup(ctx, *args):
    await setup_server(client, config['owner_id'], ctx, args)


@client.command(pass_context=True)
@commands.cooldown(15, 1)
async def save(ctx, *args):
    server = get_server(ctx.message.server)
    if not server['configured']:
        get_server(ctx.message.server)
        await client.add_reaction(ctx.message, '✅')
    elif ctx.message.author.id in [get_server(ctx.message.server)['owner_id'], config['owner_id']]:
        await client.send_message(discord.Object(id=ctx.message.channel.id),
                                  "You didn't need to save your server")


@client.event
async def on_error(event, *args):
    print(event, args)


@client.event
async def on_server_join(server):
    edit_server(server)


@client.event
async def on_server_remove(server):
    remove_server(server)


if __name__ == "__main__":
    path = os.path.abspath('users_scripts')

    for package in os.listdir(path):
        package_path = os.path.abspath('users_scripts/' + package)
        package_init = os.path.abspath('users_scripts/' + package + '/init.py')
        if os.path.isdir(package_path) and os.path.exists(package_init):
            try:
                client.load_extension("users_scripts." + package + ".init")
                print('The package ' + package + ' added')
            except Exception as e:
                if type(e) == discord.errors.ClientException:
                    print('The package ' + package + ' is not added. Check the syntax')
                else:
                    print('Unknown error while adding package ' + package)

    client.run(config['token'])
