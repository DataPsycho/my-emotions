from etl.dataio import create_balanced_data, parse
from datetime import date as dt

raw_path = "../datalake/raw/reviews_Musical_Instruments_5.json.gz"
processed = "datalake/processed/version_{}.json".format(str(dt.today()))
feed_read = "datalake/processed/version_2020-04-04.json"
feed_write = "datalake/feed/version_{}.csv".format(str(dt.today()))

# === File Parsing and Building Data for ML Model
parse(raw_path, processed)
create_balanced_data(feed_read, feed_write)
