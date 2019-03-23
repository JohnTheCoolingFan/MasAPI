from .nekowrapper import NekoWrapper


def setup(bot):
    bot.add_cog(NekoWrapper(bot))
