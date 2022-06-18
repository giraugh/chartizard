FULL = '▓'
EMPTY = '░'

def chart_from_map(counts_map, width=12, do_sort=False):
  total = sum(counts_map.values())
  largest = max(counts_map.values())
  normalized = [(k, round((v/largest)*width)) for k, v in counts_map.items()]

  # Sort rows?
  if do_sort:
    normalized = sorted(normalized, key=lambda p: p[1], reverse=True)

  # Create chart text from data
  lines = [f'{key} {FULL*size}{EMPTY*(width-size)} {round(100 * size/(total*width))}%' for (key, size) in normalized]
  return '\n'.join(lines)
