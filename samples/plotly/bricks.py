import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np


def main():
    points = [(0, 0, 0), (1, 0, 0), (2, 2, 2)]
    data = []
    for x, y, z in points:
        points = np.mgrid[x:x+1:2j, y:y+1:2j, z:z+1:2j]
        values = np.ones(points[0].shape) * 0.5
        data.append(go.Isosurface(
            x=points[0].flatten(),
            y=points[1].flatten(),
            z=points[2].flatten(),
            value=values.flatten(),
            colorscale=[[0, 'red'], [1, 'red']],
            showscale=False,
            opacity=0.5))

    fig = go.Figure(data=data)
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=32))
    fig.update_layout(scene_aspectmode='cube')

    app = dash.Dash()
    app.layout = html.Div([dcc.Graph(figure=fig)])
    app.run_server(host='0.0.0.0', debug=True, use_reloader=True)


if __name__ == "__main__":
    main()
