from users_scripts.E621Wrapper.e621wrapper import E621Wrapper


def setup(bot):
    bot.add_cog(E621Wrapper(bot))
