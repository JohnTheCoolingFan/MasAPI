import discord
import time
import datetime


def reformat_string(s):
    s = s.replace('(', '%28')
    s = s.replace(')', '%29')
    return s


async def send_warn_message(client, channel, user, wrapper_name,
                            error='Just warn',
                            help_link='',
                            wrapper_icon=''):

    embed = discord.Embed(colour=discord.Colour(0xffd11a),
                          description='',
                          timestamp=datetime.datetime.utcfromtimestamp(int(time.time())))

    embed.set_footer(text=wrapper_name, icon_url=wrapper_icon)
    embed.add_field(name=r"⚠️  | " + user.name, value=error.format(reformat_string(help_link)))

    await client.send_message(discord.Object(id=channel.id), embed=embed)


async def send_pic_massage(client, channel, user, wrapper_name,
                           collage=False, url_pic=None,
                           author='', author_link='', post_id=None,
                           post_link=None, score=None, tags='',
                           tags_url='', wrapper_icon='', color=0x7ed321):
    if post_link is None:
        post_link = []
    if post_id is None:
        post_id = []
    if url_pic is None:
        url_pic = []  # pycharm ask for it

    desc = ''
    url_to_say = ''

    if author != '' or author_link != '':
        desc += "Artist: [{}]({})\n".format(author, reformat_string(author_link))
    if post_id != '' and post_link != '':
        for i in zip(post_id, post_link):
            desc += "ID: [{}]({})\n".format(i[0], reformat_string(i[1]))
    if score is not None:
        desc += "Score: {}\n".format(score)
    desc += "Tags: [{}]({})\n".format(tags, reformat_string(tags_url))

    if not collage:
        if len(url_pic) == 0:
            desc += "Sorry, I can't embed/show this, because the post is webm/swf, but you still can view it from link"
        else:
            url_to_say = url_pic[0]
    if collage:
        to_say = '\n'.join(url_pic)
        await client.send_message(discord.Object(id=channel.id), to_say)

    embed = discord.Embed(title="About", colour=discord.Colour(color),
                          url=url_to_say,
                          description=desc,
                          timestamp=datetime.datetime.utcfromtimestamp(int(time.time())))

    embed.set_image(url=url_to_say)
    embed.set_author(name=user.name, icon_url=user.avatar_url)
    embed.set_footer(text=wrapper_name, icon_url=wrapper_icon)

    await client.send_message(discord.Object(id=channel.id), embed=embed)


async def send_information_massage():
    pass


async def send_table_message():
    pass
