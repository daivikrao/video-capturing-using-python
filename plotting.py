from video_processing import df
from bokeh.plotting import figure,output_file,show
from bokeh.models import HoverTool,ColumnDataSource

df["Start_string"] = df["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
df["End_string"] = df["End"].dt.strftime("%Y-%m-%d %H:%M:%S")
cds = ColumnDataSource(df)
p = figure(x_axis_type = "datetime",height=50,width=500,sizing_mode="scale_both",title="Motion graph",toolbar_location="below")

p.quad(left="Start",right="End",bottom=0,top=1,color="red",source=cds)
p.yaxis.minor_tick_line_color = None
p.yaxis[0].ticker.desired_num_ticks = 1

hover = HoverTool(tooltips = [("Start","@Start_string"),("End","@End_string")])
p.add_tools(hover)
output_file("motion_graph.html")
show(p)