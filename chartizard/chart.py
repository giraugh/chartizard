import discord

FULL = '▓'
EMPTY = '░'

class Chart:
  """ A chart being rendered using reacts from the source message.
      Keeps track of sent embed for updating """

  def __init__(self, source_message_id, do_sort=False):
    self.source_message_id = source_message_id
    self.sent_message_id = None
    self.do_sort = do_sort
    self.counts_map = {}
  
  def get_unique_id(self):
    """ Get pair of values unique to this chart. Essentially a primary key """

    return (self.source_message_id, self.sent_message_id)
  
  async def update_counts(self, channel):
    """ Update the counts of each react using up-to-date message from channel """

    # Get reacts from original message
    original_message = await channel.fetch_message(id=self.source_message_id)
    react_names = [r.emoji if type(r.emoji) is str else r.emoji.name for r in original_message.reactions]
    self.counts_map = dict(zip(react_names, [r.count for r in original_message.reactions]))

  
  def to_str(self, width=12):
    """ Create string representation of graph. """

    if len(self.counts_map) == 0:
      return 'No reactions yet :)'

    total = sum(self.counts_map.values())
    largest = max(self.counts_map.values())
    normalized = [(k, round((v/largest)*width)) for k, v in self.counts_map.items()]

    # Sort rows?
    if self.do_sort:
      normalized = sorted(normalized, key=lambda p: p[1], reverse=True)

    # Create chart text from data
    lines = [f'{key} {FULL*size}{EMPTY*(width-size)} {round(100 * size/(total*width))}%' for (key, size) in normalized]
    return '\n'.join(lines)


  def to_embed(self, width=12):
    """ Create discord embed from chart react data """

    embed = discord.Embed(title=':fire: Chartizard Chart', color=0xEEBB01)
    embed.add_field(name='Results', value=self.to_str(width), inline=True)
    return embed
  

  async def send_embed_message(self, channel):
    """ Send embed containing chart on specified channel. Keeps a reference so that it can be updated later. """

    embed = self.to_embed()
    message = await channel.send(embed=embed)
    self.sent_message_id = message.id
  

  async def update_embed_message(self, channel):
    """ Update the last sent embed if applicable using updated reaction counts """

    if self.sent_message_id:
      message = await channel.fetch_message(id=self.sent_message_id)
      await message.edit(embed=self.to_embed())

  
  def __str__(self):
    return self.to_str()    
