import numpy as np
import pandas as pd
import plotly.express as plt
from collections import OrderedDict

raw_data = pd.read_csv("data.csv", skipinitialspace=True)
metric_list = list(OrderedDict.fromkeys(list(raw_data["metric"])))
result_data = pd.DataFrame(columns=["metric", "open_stack", "value"])
for metric in metric_list:
    metric_df = raw_data[raw_data.metric == metric]
    # gt_value = metric_df.value.max()

    uniform_data = pd.DataFrame(
        {
            "metric": metric,
            "open_stack": [
                list(metric_df.open_stack[metric_df.value == metric_df.value.max()])[0],
                list(metric_df.open_stack[metric_df.value == metric_df.value.min()])[0],
            ],
            "value": [1, metric_df.value.min() / metric_df.value.max()],
        }
    )

    result_data = pd.concat([result_data, uniform_data])

print(result_data)
