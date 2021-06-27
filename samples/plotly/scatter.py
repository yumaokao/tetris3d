import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html


def main():
    # x and y given as array_like objects
    fig = px.scatter(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16])
    # fig.show()

    app = dash.Dash()
    app.layout = html.Div([dcc.Graph(figure=fig)])
    app.run_server(debug=True, use_reloader=True)


if __name__ == "__main__":
    main()
