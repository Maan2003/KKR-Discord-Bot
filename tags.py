import json
from discord.ext import commands


class Tags(commands.Cog):
    def __init__(self):
        with open("Details/tags.json") as f:
            self.data = json.load(f)

    @commands.Cog.listener()
    async def on_message(self, msg):
        name = msg.content
        if msg.author.bot or name not in self.data:
            return
        data = self.data[name]["content"].replace("@", "​@​")

        await msg.channel.send(data)

    @commands.group(name="tags", invoke_without_command=True)
    async def tags(self, ctx):
        """Tags are used to make shortcuts for messages"""
        await ctx.send(f"`{ctx.prefix}tags create` to make new tags")

    @tags.command(name="create")
    async def create(self, ctx, name, *, content):
        """Create a new tag"""
        author = ctx.author.id

        if name in self.data:
            await ctx.send(f"it already exists, use `{ctx.prefix}tags delete` to delete it")
            return

        self.data[name] = {
            "author": author,
            "content": content,
        }
        self.save()
        await ctx.send("It is safe with me now")

    @tags.command(name="delete")
    async def delete(self, ctx, name):
        """Delete the given tag. Only author can delete the tag"""
        if name not in self.data:
            await ctx.send("no such tag")
            return

        old_data = self.data[name]
        if old_data["author"] != ctx.message.author.id:
            await ctx.send("You are not the author :rage:")
            return

        del self.data[name]
        await ctx.send("deleted")
        self.save()

    @tags.command(name="get")
    async def get(self, ctx, name):
        """Get the tag. use this if your tag conflicts with a builtin command"""
        if name not in self.data:
            await ctx.send("no such tags")
            return
        data = self.data[name]

        await ctx.send(data["content"].replace("@", "​@​"))

    def save(self):
        with open("Details/tags.json", 'w') as f:
            json.dump(self.data, f)