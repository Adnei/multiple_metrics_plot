# import numpy as np
import pandas as pd

# import plotly.express as px
import plotly.graph_objects as go
from collections import OrderedDict

raw_data = pd.read_csv("data.csv", skipinitialspace=True)
metric_list = list(OrderedDict.fromkeys(list(raw_data["metric"])))
result_data = pd.DataFrame(columns=["metric", "open_stack", "value"])
for metric in metric_list:
    if metric == "internal_throughput_rate" or metric == "external_throughput_rate":
        continue
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

# fig = px.line_polar(result_data, r="value", theta="metric", line_close=True)
# fig.update_traces(fill="toself")
# fig.show()

fig = go.Figure()

fig.add_trace(
    go.Scatterpolar(
        r=list(result_data.value[result_data.open_stack == "KA"]),
        theta=list(result_data.metric[result_data.open_stack == "KA"]),
        fill="toself",
        name="KA",
    )
)

fig.add_trace(
    go.Scatterpolar(
        r=list(result_data.value[result_data.open_stack == "StarlingX"]),
        theta=list(result_data.metric[result_data.open_stack == "StarlingX"]),
        fill="toself",
        name="StarlingX",
    )
)


fig.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 1])), showlegend=True
)

fig.show()
