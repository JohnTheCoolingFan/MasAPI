import os
import discord
from discord.ext import commands

from get_config import get_config
from functions.server import get_server, edit_server, remove_server
from functions.setup import setup_server

client = commands.Bot(command_prefix='.')

config = get_config()


@client.event
async def on_ready():
    print('Connected', client.user.name, client.user.id)


@client.command(pass_context=True)
async def bye(ctx, *args):
    if ctx.message.author.id == config['owner_id']:
        await client.logout()
        await client.close()


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
                                  "You don't need to save your server")


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
                    print('The package ' + package + ' not added. Check the spelling of the code. Error: ' + str(e))
                else:
                    print('Unknown error adding package ' + package, 'Error:', e)
        else:
            print('The package ' + package + " is not added because it doesn't have init file")

    client.run(config['token'])
