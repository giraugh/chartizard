import discord
from chart import Chart
from charts import get_all_charts, upsert_chart

class ChartizardClient(discord.Client):
  
  async def on_ready(self):
    print(f'Logged on as {self.user}!')


  async def on_message(self, message):
    # Check if we were mentioned
    if not self.user.mentioned_in(message):
      return

    # Check that it's a reply
    if not message.reference or message.is_system():
      return

    # Parse Options
    do_sort = 'sort' in message.content

    # Create chart
    chart = Chart(message.reference.message_id, do_sort)

    # Get reacts from original message
    await chart.update_counts(message.channel)

    # Send embed
    await chart.send_embed_message(message.channel)

    # Save chart to disk
    upsert_chart(chart)

  
  async def on_reaction_change(self, payload):
    # Check if any of our charts sources were reacted to
    charts = get_all_charts().values()
    target_charts = (c for c in charts if c.source_message_id == payload.message_id)
    
    # If so, update the associated charts
    for target_chart in target_charts:
      if target_chart:
        channel = self.get_channel(payload.channel_id)
        await target_chart.update_counts(channel)
        await target_chart.update_embed_message(channel)

      # Update this stored chart
      upsert_chart(target_chart)

  
  async def on_raw_reaction_add(self, payload):
    await self.on_reaction_change(payload)


  async def on_raw_reaction_remove(self, payload):
    await self.on_reaction_change(payload)
