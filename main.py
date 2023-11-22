# import numpy as np
import os
import pandas as pd
from pandas.io.parsers.readers import fill

# import plotly.express as px
import plotly.graph_objects as go
from collections import OrderedDict
import plotly.io as pio

pio.kaleido.scope.mathjax = None

raw_data = pd.read_csv("data.csv", skipinitialspace=True)
metric_list = list(OrderedDict.fromkeys(list(raw_data["metric"])))
result_data = pd.DataFrame(
    columns=["metric", "label" "unit_label", "open_stack", "value", "perspective"]
)
for metric in metric_list:
    if metric == "internal_throughput_rate" or metric == "external_throughput_rate":
        continue
    metric_df = raw_data[raw_data.metric == metric]
    greater = list(metric_df.open_stack[metric_df.value == metric_df.value.max()])[0]
    lower = list(metric_df.open_stack[metric_df.value == metric_df.value.min()])[0]
    unit_label = (
        list(metric_df.label)[0]
        + " ("
        + str(metric_df.value.max())
        + " "
        + list(metric_df.unit)[0]
        + ")"
    )
    perspective = list(metric_df.perspective)[0]

    uniform_data = pd.DataFrame(
        {
            "metric": metric,
            "label": list(metric_df.label)[0],
            "unit_label": unit_label,
            "open_stack": [greater, lower],
            "value": [1, metric_df.value.min() / metric_df.value.max()],
            "perspective": perspective,
        }
    )

    result_data = pd.concat([result_data, uniform_data])

print(result_data)

# fig = px.line_polar(result_data, r="value", theta="metric", line_close=True)
# fig.update_traces(fill="toself")
# fig.show()

pdf_layout = go.Layout(
    autosize=False,
    width=1080,
    height=720,
)
fig = go.Figure(layout=pdf_layout)

fig.add_trace(
    go.Scatterpolar(
        r=result_data.value[result_data.open_stack == "KA"],
        theta=result_data.unit_label[result_data.open_stack == "KA"],
        fill="toself",
        name="KA",
        legendgroup="default",
        legendgrouptitle_text="KA vs. StarlingX",
    )
)

fig.add_trace(
    go.Scatterpolar(
        r=result_data.value[result_data.open_stack == "StarlingX"],
        theta=result_data.unit_label[result_data.open_stack == "StarlingX"],
        fill="toself",
        name="StarlingX",
        legendgroup="default",
    )
)

for metric in metric_list:
    if metric == "internal_throughput_rate" or metric == "external_throughput_rate":
        continue

    perspective = list(result_data.perspective[result_data.metric == metric])[0]
    legend_title = "Provider Metrics"

    if perspective == "user":
        legend_title = "User Metrics"

    fig.add_trace(
        go.Scatterpolar(
            r=result_data.value[result_data.metric == metric],
            theta=result_data.label[result_data.metric == metric],
            visible="legendonly",
            name=list(result_data.label[result_data.metric == metric])[0],
            legendgroup=perspective,
            legendgrouptitle_text=legend_title,
            line=dict(color="black"),
        )
    )


fig.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
    showlegend=True,
)

fig.show()

if not os.path.exists("plots"):
    os.mkdir("plots")

fig.write_image(format="pdf", file="plots/radar.pdf")
