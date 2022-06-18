import discord

FULL = '▓'
EMPTY = '░'

class Chart:

  def __init__(self, counts_map, source_message_id, do_sort=False):
    self.counts_map = counts_map
    self.target = source_message_id
    self.do_sort = do_sort
  
  def to_str(self, width=12):
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
    embed = discord.Embed(title=':fire: Chartizard Chart', color=0xEEBB01)
    embed.add_field(name='Results', value=self.to_str(width), inline=True)
    return embed
  
  def __str__(self):
    return self.to_str()    
