import discord

from chart import chart_from_map

class ChartizardClient(discord.Client):
  async def on_ready(self):
    print(f'Logged on as {self.user}!')

  async def on_message(self, message):
    # Check if we were mentioned
    if not self.user.mentioned_in(message):
      return

    # Check is a reply
    if not message.reference or message.is_system():
      return

    # Get reacts from original message
    original_message = await message.channel.fetch_message(id=message.reference.message_id)
    react_names = [r.emoji if type(r.emoji) is str else r.emoji.name for r in original_message.reactions]
    react_counts_map = dict(zip(react_names, [r.count for r in original_message.reactions]))

    # Options
    do_sort = 'sort' in message.content

    # Create chart embed
    chart_text = chart_from_map(react_counts_map, do_sort=do_sort)
    embed = discord.Embed(title=':fire: Chartizard Chart', color=0xEEBB01)
    embed.add_field(name='Results', value=chart_text, inline=True)

    # Send embed
    await message.channel.send(embed=embed)
