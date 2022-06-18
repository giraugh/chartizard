import pickle
from os.path import exists

CHARTS_PATH = "charts.pkl"


def get_all_charts():
  if not exists(CHARTS_PATH):
    return {}
  else:
    with open(CHARTS_PATH, 'rb') as f:
      return pickle.load(f)


def update_all_charts(charts={}):
  with open(CHARTS_PATH, 'wb') as f:
    pickle.dump(charts, f) 


def upsert_chart(chart):
  key = chart.get_unique_id()
  charts = get_all_charts()
  update_all_charts({ **charts, key: chart })
