import discord
from discord.ext import commands
import json
import requests

from get_token import get_token
from functions.get_channel import get_channel
from functions.server import get_server
from functions.message_maker import send_warn_message, send_pic_massage

wrapper_icon = 'https://e621.net/favicon.ico'


class E621Wrapper:
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    @commands.cooldown(3, 1)
    async def e621(self, ctx, *args):
        server = get_server(ctx.message.server)
        nsfw = get_channel(get_token(), ctx.message.channel.id)['nsfw']
        if ((not server['sfw']) and nsfw) or ctx.message.channel.id in server['nsfw_channels']:
            await self.client.send_typing(discord.Object(id=ctx.message.channel.id))
            await self.e6_wrap(ctx, args)
        else:
            await self.client.add_reaction(ctx.message, '❌')

    async def e6_wrap(self, ctx, args):
        limit = 1
        args = list(args)
        for i in range(len(args)):
            if args[i].find('limit=') != -1:
                limit = int(args[i].replace('limit=', ''))
                args.pop(i)
                break

        # here must be limits

        if len(args) > 5:
            error_message = 'The number of the tag shouldn\'t be more than 5'
            await send_warn_message(self.client, ctx.message.channel, ctx.message.author, 'e621.net',
                                    error=error_message,
                                    wrapper_icon=wrapper_icon)
        elif limit > 5 or limit <= 0:
            error_message = 'The limit must be between 1 and 5'
            await send_warn_message(self.client, ctx.message.channel, ctx.message.author, 'e621.net',
                                    error=error_message,
                                    wrapper_icon=wrapper_icon)
        else:
            embed_tags = ' '.join(args)
            if len(args) == 0:
                args.append('score:>30')
                args.append('female')
            url_tags = '+'.join((['order:random'] + args)[:6])
            tags_url = '+'.join(args[:6])
            header = {
                'User-Agent': 'PechTestBot/0.1 (by bsa0 on e621)'
            }

            try:
                url_r = requests.get('https://e621.net/post/index.json?tags={}&limit={}&page=1'.format(url_tags, limit),
                                     headers=header)

                if url_r.status_code == 200:
                    if len(json.loads(url_r.text)) != 0:
                        if len(json.loads(url_r.text)) == 1:
                            post = json.loads(url_r.text)[0]
                            picture_url = [post['sample_url']]
                            if post['file_ext'] in ['swf', 'webm']:
                                picture_url = ''
                            post_id = [str(post['id'])]
                            post_url = ['https://e621.net/post/show/' + str(post['id'])]
                            artist_name = ' '.join(post['artist'])
                            artist_url = 'https://e621.net/post/index/1/' + '%20'.join(post['artist'])
                            score = str(post['score'])
                            tags_url = 'https://e621.net/post?tags={}'.format(tags_url)
                            await send_pic_massage(self.client, ctx.message.channel, ctx.message.author, 'e621.net',
                                                   collage=False, url_pic=picture_url,
                                                   author=artist_name, author_link=artist_url, post_id=post_id,
                                                   post_link=post_url, score=score, tags=embed_tags, tags_url=tags_url,
                                                   wrapper_icon=wrapper_icon, color=0x223055)
                        else:
                            posts = json.loads(url_r.text)
                            picture_urls = []
                            post_ids = []
                            post_urls = []
                            tags_url = 'https://e621.net/post?tags={}'.format(tags_url)

                            for post in posts:
                                picture_urls.append(post['sample_url'])
                                post_ids.append(str(post['id']))
                                post_urls.append('https://e621.net/post/show/' + str(post['id']))

                            await send_pic_massage(self.client, ctx.message.channel, ctx.message.author, 'e621.net',
                                                   collage=True, url_pic=picture_urls,
                                                   post_id=post_ids, post_link=post_urls,
                                                   tags=embed_tags, tags_url=tags_url,
                                                   wrapper_icon=wrapper_icon, color=0x223055)
                    else:
                        tags_url = 'https://e621.net/post?tags={}'.format(tags_url)
                        error_message = r"¯\_(ツ)_/¯ [Nothing to show]({})"
                        await send_warn_message(self.client, ctx.message.channel, ctx.message.author, 'e621.net',
                                                error=error_message,
                                                help_link=tags_url,
                                                wrapper_icon=wrapper_icon)
                else:
                    await self.client.send_file(discord.Object(id=ctx.message.channel.id), open('chrome_YLl4Pxeywc.png',
                                                                                                'rb'))
            except Exception as e:
                print(e)
                await self.client.send_file(discord.Object(id=ctx.message.channel.id), open('chrome_YLl4Pxeywc.png',
                                                                                            'rb'))
