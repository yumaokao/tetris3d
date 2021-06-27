import plotly.graph_objects as go
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html


class Display():
    app = None

    @staticmethod
    def show(all_bricks, opacity=1.0):
        data = []
        axis_max = 0.0
        for brick in all_bricks:
            for x, y, z in brick.points:
                points = np.mgrid[x:x+1:2j, y:y+1:2j, z:z+1:2j]
                axis_max = np.max([points.max(), axis_max])

                values = np.ones(points[0].shape) * 0.5
                data.append(go.Isosurface(
                    x=points[0].flatten(),
                    y=points[1].flatten(),
                    z=points[2].flatten(),
                    value=values.flatten(),
                    colorscale=[[0, brick.color], [1, brick.color]],
                    showscale=False,
                    opacity=opacity))

        plot_range = [0, int(axis_max) + 1]

        fig = go.Figure(data=data)
        fig.update_layout(
            scene = dict(
                xaxis = dict(range=plot_range,),
                yaxis = dict(range=plot_range,),
                zaxis = dict(range=plot_range,),)
        )
        fig.update_layout(margin=dict(l=0, r=0, b=0, t=32))
        fig.update_layout(scene_aspectmode='cube')
        # fig.write_html('tetris3d.html')

        if Display.app is None:
            Display.app = dash.Dash()
        Display.app.layout = html.Div([dcc.Graph(figure=fig)])
        Display.app.run_server(host='0.0.0.0', debug=True, use_reloader=False)
