import discord
from functions.server import get_server, edit_server


async def setup_server(client, owner_id, ctx, args):
    if ctx.message.author.id in [get_server(ctx.message.server)['owner_id'], owner_id]:
        server = get_server(ctx.message.server)

        if server['configured']:
            if len(args) == 0:
                await client.send_message(discord.Object(id=ctx.message.channel.id),
                                          'This command makes your server not configured, please use ".setup" again')
                server['configured'] = False
                edit_server(ctx.message.server, server)
            else:
                if args[0] == 'favorites':
                    server['sfw'] = True
                    if server['favorites']:
                        await client.send_message(discord.Object(id=ctx.message.channel.id),
                                                  'Your server marked as server without favotites, use ".setup favorite'
                                                  's" to ~~make america great~~ turns it up again')
                        server['favorites'] = False
                    else:
                        await client.send_message(discord.Object(id=ctx.message.channel.id),
                                                  'Your server marked as server with favotites, use ".setup favorites"'
                                                  'to turns it down')
                        server['favorites'] = True
                    edit_server(ctx.message.server, server)
                elif args[0] == 'fav_a' and server['favorites']:
                    server['a_channel_id'] = ctx.message.channel.id
                    if ctx.message.channel.id not in server['nsfw_channels']:
                        server['nsfw_channels'].append(ctx.message.channel.id)
                    edit_server(ctx.message.server, server)
                elif args[0] == 'fav_f' and server['favorites']:
                    server['f_channel_id'] = ctx.message.channel.id
                    if ctx.message.channel.id not in server['nsfw_channels']:
                        server['nsfw_channels'].append(ctx.message.channel.id)
                    edit_server(ctx.message.server, server)
                elif args[0] == 'fav_n' and server['favorites']:
                    server['n_channel_id'] = ctx.message.channel.id
                    if ctx.message.channel.id not in server['nsfw_channels']:
                        server['nsfw_channels'].append(ctx.message.channel.id)
                    edit_server(ctx.message.server, server)
                elif args[0] == 'fav_r34' and server['favorites']:
                    server['r34_channel_id'] = ctx.message.channel.id
                    if ctx.message.channel.id not in server['nsfw_channels']:
                        server['nsfw_channels'].append(ctx.message.channel.id)
                    edit_server(ctx.message.server, server)
                elif args[0] == 'nsfw':
                    if ctx.message.channel.id not in server['nsfw_channels']:
                        server['sfw'] = True
                        server['nsfw_channels'].append(ctx.message.channel.id)
                    else:
                        server['nsfw_channels'].remove(ctx.message.channel.id)
                    edit_server(ctx.message.server, server)
                    await client.add_reaction(ctx.message, '✅')
                else:
                    await client.send_message(discord.Object(id=ctx.message.channel.id), 'Invalid tag, see help')

        else:
            if len(args) == 0:
                await client.send_message(discord.Object(id=ctx.message.channel.id),
                                          'Your server marked as configured, use ".setup favorites" if you need favorit'
                                          'es channels, ".setup fav_a", ".setup fav_f", ".setup fav_n" or ".setup fav_r'
                                          '34" in the relevant channels')
                server['configured'] = True
                edit_server(ctx.message.server, server)
            else:
                await client.send_message(discord.Object(id=ctx.message.channel.id), 'Tags ignored')
                await client.send_message(discord.Object(id=ctx.message.channel.id),
                                          'Your server marked as configured, use "!setup favorites" if you need favorit'
                                          'es channels, ".setup fav_a", "!setup fav_f", ".setup fav_n" or ".setup fav_r'
                                          '34" in the relevant channels')
                server['configured'] = True
                edit_server(ctx.message.server, server)
