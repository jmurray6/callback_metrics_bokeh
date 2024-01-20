import pandas as pd
from bokeh.models import Select
from bokeh.layouts import column, row
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.transform import factor_cmap

df = pd.read_csv('mt_metrics_float.csv')
df['accuracy_list'] = df['accuracy_list'].apply(lambda x: list(map(float, x.split(','))))
df['loss_list'] = df['loss_list'].apply(lambda x: list(map(float, x.split(','))))

TOOLTIPS=[
    ("Model Name", "@model_name"),
    ("Model Type", "@model_type"),
    ("Accuracy", "@accuracy"),
    ("Training Duration", "@training_duration"),
    ("Learning Rate", "@learning_rate"),
    ("Loss", "@loss")
]
axis_map = {
    "# of Epochs": "epochs",
    "Accuracy": "accuracy",
    "Training Duration": "training_duration",
    "Learning Rate": "learning_rate",
    "Loss": "loss"
}

x_axis = Select(title="X Axis", options=sorted(axis_map.keys()), value="# of Epochs")
y_axis = Select(title="Y Axis", options=sorted(axis_map.keys()), value="Accuracy")
source = ColumnDataSource(
    data=dict(
        x=[], 
        y=[], 
        model_name=[], 
        model_type=[], 
        training_duration=[], 
        epochs=[], 
        learning_rate=[], 
        accuracy=[], 
        loss=[]
    )
)

model_names= sorted(df["model_name"].unique())
TOOLS="pan,wheel_zoom,reset,hover,tap"
p = figure(height=600, title="Model Training Metrics", tools=TOOLS, tooltips=TOOLTIPS)
p.scatter(x="x", y="y", size=10, source=source, color=factor_cmap("model_name", "Category10_10", model_names))

def update():
    x_name = axis_map[x_axis.value]
    y_name = axis_map[y_axis.value]

    p.xaxis.axis_label = x_axis.value
    p.yaxis.axis_label = y_axis.value
    source.data = dict(
        x=df[x_name],
        y=df[y_name],
        model_name=df["model_name"], 
        model_type=df["model_type"], 
        training_duration=df["training_duration"], 
        epochs=df["epochs"], 
        learning_rate=df["learning_rate"], 
        accuracy=df["accuracy"], 
        loss=df["loss"]
    )

controls = [x_axis, y_axis]
for control in controls:
    control.on_change("value", lambda attr, old, new: update())

inputs = column(*controls, width=320, height=800)
supp_col = column(height=800)
layout = column(row(inputs, p, supp_col), height=800)

def select(attr, old, new):
    plot = figure(height=600, x_axis_label="Epoch", y_axis_label="Accuracy/Loss")
    if len(new) > 0:
        plot.line(x=list(range(1, df.iloc[[new[0]][0]]["epochs"] + 1)), y=df.iloc[[new[0]][0]]["accuracy_list"], legend_label=str("accuracy_list"), color="green", line_width=5)
        plot.line(x=list(range(1, df.iloc[[new[0]][0]]["epochs"] + 1)), y=df.iloc[[new[0]][0]]["loss_list"], legend_label=str("loss_list"), color="red", line_width=5)
    supp_col.children = [plot]

source.selected.on_change("indices", select)

update()

curdoc().add_root(layout)
