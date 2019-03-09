import discord
from discord.ext import commands
import requests
from lxml import etree
from random import randint

from get_token import get_token
from functions.server import get_server
from functions.get_channel import get_channel
from functions.xml_to_dict import etree_to_dict
from functions.message_maker import send_warn_message, send_pic_massage

wrapper_icon = 'https://cdn.discordapp.com/avatars/545261364550041611/5fb559e880d866a5bc345c067e2f35c5.png'


class Rule34Wrapper:
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    @commands.cooldown(3, 1)
    async def r34(self, ctx, *args):
        server = get_server(ctx.message.server)
        nsfw = get_channel(get_token(), ctx.message.channel.id)['nsfw']
        if ((not server['sfw']) and nsfw) or ctx.message.channel.id in server['nsfw_channels']:
            await self.client.send_typing(discord.Object(id=ctx.message.channel.id))
            await self.r34_wrap(ctx, args)
        else:
            await self.client.add_reaction(ctx.message, '❌')

    async def r34_wrap(self, ctx, args):
        limit = 1
        args = list(args)
        for i in range(len(args)):
            if args[i].find('limit=') != -1:
                limit = int(args[i].replace('limit=', ''))
                args.pop(i)
                break

        if len(args) > 5:
            error_message = 'The number of the tag should be no more than 5'
            await send_warn_message(self.client, ctx.message.channel, ctx.message.author, 'Rule34.xxx',
                                    error=error_message,
                                    wrapper_icon=wrapper_icon)
        elif limit > 5 or limit <= 0:
            error_message = 'The limit must be between 1 and 5'
            await send_warn_message(self.client, ctx.message.channel, ctx.message.author, 'Rule34.xxx',
                                    error=error_message,
                                    wrapper_icon=wrapper_icon)
        else:
            embed_tags = ' '.join(args)
            url_tags = '+'.join(args)

            try:
                url = 'https://rule34.xxx/index.php?page=dapi&s=post&q=index&limit={}&pid={}&tags={}'

                url_r = requests.get(url.format(limit, 0, url_tags))

                if url_r.status_code == 200:
                    posts = etree_to_dict(etree.fromstring(url_r.content))
                    pid = randint(0, int(posts['posts']['@count']) // limit - 1) % 100000
                    url_r = requests.get(url.format(limit, pid, url_tags))
                    posts = etree_to_dict(etree.fromstring(url_r.content))

                    if url_r.status_code == 200 and int(posts['posts']['@count']) != 0:
                        if str(type(posts['posts']['post'])) == "<class 'dict'>":
                            post = posts['posts']['post']
                            picture_url = [post['@sample_url']]
                            if (post['@file_url'] + ' ')[-4:-1] in ['swf', 'ebm']:
                                picture_url = ''
                            post_id = [post['@id']]
                            post_url = ['https://rule34.xxx/index.php?page=post&s=view&id=' + post_id[0]]
                            score = post['@score']
                            tags_url = 'https://rule34.xxx/index.php?page=post&s=list&tags=' + url_tags
                            await send_pic_massage(self.client, ctx.message.channel, ctx.message.author, 'Rule34.xxx',
                                                   collage=False, url_pic=picture_url,
                                                   post_id=post_id, post_link=post_url,
                                                   score=score, tags=embed_tags, tags_url=tags_url,
                                                   wrapper_icon=wrapper_icon, color=0xAAE6A6)
                        else:
                            posts = posts['posts']['post']
                            picture_urls = []
                            post_ids = []
                            post_urls = []
                            tags_url = 'https://rule34.xxx/index.php?page=post&s=list&tags=' + url_tags

                            for post in posts:
                                picture_urls.append(post['@sample_url'])
                                post_ids.append(post['@id'])
                                post_urls.append('https://rule34.xxx/index.php?page=post&s=view&id=' + post['@id'])

                            await send_pic_massage(self.client, ctx.message.channel, ctx.message.author, 'Rule34.xxx',
                                                   collage=True, url_pic=picture_urls,
                                                   post_id=post_ids, post_link=post_urls,
                                                   tags=embed_tags, tags_url=tags_url,
                                                   wrapper_icon=wrapper_icon, color=0xAAE6A6)
                    else:
                        tags_url = 'https://rule34.xxx/index.php?page=post&s=list&tags={}'.format(url_tags)
                        error_message = r"¯\_(ツ)_/¯ [Nothing to show]({})"
                        await send_warn_message(self.client, ctx.message.channel, ctx.message.author, 'Rule34.xxx',
                                                error=error_message,
                                                help_link=tags_url,
                                                wrapper_icon=wrapper_icon)
                else:
                    await self.client.send_file(discord.Object(id=ctx.message.channel.id), open('chrome_YLl4Pxeywc.png',
                                                                                           'rb'))
            except Exception as e:
                print(e)
                await self.client.send_file(discord.Object(id=ctx.message.channel.id), open('chrome_YLl4Pxeywc.png', 'rb'))
