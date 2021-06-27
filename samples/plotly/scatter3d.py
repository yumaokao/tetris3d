# import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html


def main():
    '''
    df = px.data.iris()
    fig = px.scatter_3d(
        df, x='sepal_length', y='sepal_width', z='petal_width', color='species',
        size_max=40, size='petal_length')
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
    '''
	# Helix equation
    t = np.linspace(0, 20, 100)
    x, y, z = np.cos(t), np.sin(t), t
    x1, y1, z1 = np.sin(t), np.cos(t), t

    fig = go.Figure(data=[
        go.Scatter3d(
	        x=x, y=y, z=z, mode='markers',
            marker=dict(
                size=16, color='purple', opacity=0.6, symbol='circle')),
        go.Scatter3d(
	        x=x1, y=y1, z=z1, mode='markers',
            marker=dict(
                size=16, color='blue', opacity=0.6, symbol='circle')),
    ])
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))

    app = dash.Dash()
    app.layout = html.Div([dcc.Graph(figure=fig)])
    app.run_server(debug=True, use_reloader=True)


if __name__ == "__main__":
    main()
