import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np


def main():
    X, Y, Z = np.mgrid[-8:8:40j, -8:8:40j, -8:8:40j]
    # values = np.sin(X*Y*Z) / (X*Y*Z)
    values = np.ones(X.shape) * 0.5

    fig = go.Figure(data=go.Volume(
        x=X.flatten(),
        y=Y.flatten(),
        z=Z.flatten(),
        value=values.flatten(),
        isomin=0.1,
        isomax=0.8,
        opacity=0.9, # needs to be small to see through all surfaces
        surface_count=8, # needs to be a large number for good volume rendering
        ))
    # fig.show()

    app = dash.Dash()
    app.layout = html.Div([dcc.Graph(figure=fig)])
    app.run_server(debug=True, use_reloader=True)


if __name__ == "__main__":
    main()
