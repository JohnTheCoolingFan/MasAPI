from .r34wrapper import Rule34Wrapper


def setup(bot):
    bot.add_cog(Rule34Wrapper(bot))
