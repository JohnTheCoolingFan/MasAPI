import requests
import discord
from discord.ext import commands

from get_config import get_config
from functions.get_channel import get_channel
from functions.server import get_server
from functions.message_maker import send_warn_message, send_pic_massage

wrapper_icon = 'https://cdn.discordapp.com/avatars/545261364550041611/5fb559e880d866a5bc345c067e2f35c5.png'
n_tags = ['tickle', 'classic', 'ngif', 'erofeet', 'meow', 'erok', 'poke', 'les', 'hololewd', 'lewdk', 'keta', 'feetg',
          'nsfw_neko_gif', 'eroyuri', 'kiss', '8ball', 'kuni', 'tits', 'pussy_jpg', 'cum_jpg', 'pussy', 'lewdkemo',
          'lizard', 'slap', 'lewd', 'cum', 'cuddle', 'spank', 'smallboobs', 'goose', 'Random_hentai_gif', 'avatar',
          'fox_girl', 'nsfw_avatar', 'hug', 'gecg', 'boobs', 'pat', 'feet', 'smug', 'kemonomimi', 'solog', 'holo',
          'wallpaper', 'bj', 'woof', 'yuri', 'trap', 'anal', 'baka', 'blowjob', 'holoero', 'feed', 'neko', 'gasm',
          'hentai', 'futanari', 'ero', 'solo', 'waifu', 'pwankg', 'eron', 'erokemo']

# color 0x9900AB


class NekoWrapper:
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    @commands.cooldown(3, 1)
    async def neko(self, ctx, *args):
        """
        .neko [tag] - shows image from nekos.life.
        ONLY 1 TAG!
        Available tags: 'tickle', 'classic', 'ngif', 'erofeet', 'meow', 'erok', 'poke', 'les', 'hololewd', 'lewdk',
        'keta', 'feetg','nsfw_neko_gif', 'eroyuri', 'kiss', '8ball', 'kuni', 'tits', 'pussy_jpg', 'cum_jpg', 'pussy',
        'lewdkemo','lizard', 'slap', 'lewd', 'cum', 'cuddle', 'spank', 'smallboobs', 'goose', 'Random_hentai_gif',
        'avatar','fox_girl', 'nsfw_avatar', 'hug', 'gecg', 'boobs', 'pat', 'feet', 'smug', 'kemonomimi', 'solog',
        'holo', 'wallpaper', 'bj', 'woof', 'yuri', 'trap', 'anal', 'baka', 'blowjob', 'holoero', 'feed', 'neko', 'gasm',
        'hentai', 'futanari', 'ero', 'solo', 'waifu', 'pwankg', 'eron', 'erokemo'
        """
        if ctx.message.server is not None:
            server = get_server(ctx.message.server)
            nsfw = get_channel(get_config()['token'], ctx.message.channel.id)['nsfw']
        else:
            server = {'sfw': False,
                      'nsfw_channels': []}
            nsfw = True
        if ((not server['sfw']) and nsfw) or ctx.message.channel.id in server['nsfw_channels']:
            await self.client.send_typing(discord.Object(id=ctx.message.channel.id))
            await self.neko_wrap(ctx, args)
        else:
            await self.client.add_reaction(ctx.message, '❌')

    async def neko_wrap(self, ctx, args):
        if len(args) > 1:
            error_message = 'Number of tags shouldn\'t be more than 1'
            await send_warn_message(self.client, discord.Object(id=ctx.message.channel.id),
                                    ctx.message.author, 'Nekos.life',
                                    error=error_message,
                                    wrapper_icon=wrapper_icon)
        else:
            tag = 'neko'

            if len(args) == 1:
                tag = args[0]
            if tag not in n_tags:
                error_message = 'The tag must be in the list, check .help neko'
                await send_warn_message(self.client, discord.Object(id=ctx.message.channel.id),
                                        ctx.message.author, 'Nekos.life',
                                        error=error_message,
                                        wrapper_icon=wrapper_icon)

            r = requests.get('https://nekos.life/api/v2/img/{}'.format(tag))
            url = [r.json()['url']]

            await send_pic_massage(self.client, discord.Object(id=ctx.message.channel.id),
                                   ctx.message.author, 'Nekos.life',
                                   collage=False, url_pic=url,
                                   tags=tag,
                                   wrapper_icon=wrapper_icon, color=0x9900AB)
