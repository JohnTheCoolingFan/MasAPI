import discord
import time
import datetime


def embed_help(client, args):
    footer_images = {
        'help': client.user.avater_url,
        'idk': 'https://cdn.discordapp.com/avatars/545261364550041611/5fb559e880d866a5bc345c067e2f35c5.png',
        'r34': 'https://cdn.discordapp.com/avatars/545261364550041611/5fb559e880d866a5bc345c067e2f35c5.png',
        # https://rule34.xxx/favicon.ico',
        'e621': 'https://e621.net/favicon.ico',
        'neko': 'https://nekos.life/static/icons/favicon-32x32.png'
    }

    command = 'help'

    help_help = ".help [command] - shows that message or shows help about command\n" \
                ".e621 [tags] - shows image from e621.net\n" \
                ".r34 [tags] - shows image from rule34.xxx\n" \
                ".neko [tag] - show image from nekos.life"

    help_e621 = ".621 [tags] - shows image from e621.net.\n" \
                "The number of tags should be no more than 5.\n" \
                "Tags must be separated by spaces."

    help_r34 = ".r34 [tags] - shows image from rule34.xxx.\n" \
               "The number of tags should be no more than 5.\n" \
               "Tags must be separated by spaces."

    help_neko = ".neko [tag] - shows image from nekos.life.\n" \
                "ONLY 1 TAG!\n" \
                "Tags: 'tickle', 'classic', 'ngif', 'erofeet', 'meow', 'erok', 'poke', 'les', 'hololewd', 'lewdk'" \
                ", 'keta', 'feetg', 'nsfw_neko_gif', 'eroyuri', 'kiss', '8ball', 'kuni', 'tits', 'pussy_jpg', 'cu" \
                "m_jpg', 'pussy', 'lewdkemo', 'lizard', 'slap', 'lewd', 'cum', 'cuddle', 'spank', 'smallboobs', '" \
                "goose', 'Random_hentai_gif', 'avatar', 'fox_girl', 'nsfw_avatar', 'hug', 'gecg', 'boobs', 'pat'," \
                "'feet', 'smug', 'kemonomimi', 'solog', 'holo', 'wallpaper', 'bj', 'woof', 'yuri', 'trap', 'anal'" \
                ", 'baka', 'blowjob', 'holoero', 'feed', 'neko', 'gasm', 'hentai', 'futanari', 'ero', 'solo', 'wa" \
                "ifu', 'pwankg', 'eron', 'erokemo'"

    help_idk = "This command doesn't exist."

    value = help_help

    if len(args) == 1:
        command = args[0]
        if command == 'help':
            value = help_help
        elif command == 'e621':
            value = help_e621
        elif command == 'r34':
            value = help_r34
        elif command == 'neko':
            value = help_neko
        else:
            command = 'idk'
            value = help_idk
    elif len(args) > 1:
        command = 'idk'
        value = help_idk

    embed = discord.Embed(title="Hi! NekoAPI bot here!", colour=discord.Colour(0x7ed321),
                          timestamp=datetime.datetime.utcfromtimestamp(int(time.time())))

    embed.set_footer(text="Help",
                     icon_url=footer_images[command])

    embed.add_field(name="Commands", value=value)

    return embed
