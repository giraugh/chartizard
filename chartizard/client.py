import discord

from chart import Chart

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
    chart = Chart(react_counts_map, message.reference.message_id, do_sort)
    embed = chart.to_embed()

    # Send embed
    await message.channel.send(embed=embed)
