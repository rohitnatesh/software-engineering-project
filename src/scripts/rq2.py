# Research question 2.

# Which programming languages do developers ask ChatGPT for
# help with, and how does this pattern change over time?

import os
import json
import pandas as pd

CURRENT_DIRECTORY = os.getcwd()

raw_data = json.loads(f'{CURRENT_DIRECTORY}/src/datasets/snapshot_20231012/20231012_230826_commit_sharings.json')
pd.json_normalize(raw_data)
print(raw_data)


# time | language