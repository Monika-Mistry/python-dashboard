import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash_data_table as ddt

sites_2016 = pd.read_csv("data/sites_2016.csv")
sites_2017 = pd.read_csv("data/sites_2017.csv")
sites_2018 = pd.read_csv("data/sites_2018.csv")
top_2018 = pd.read_csv(
    "data/top_2018.csv",
    thousands=",",
    dtype={"fb_engagement": int},
    parse_dates=['published_date']) \
    .dropna(axis="index", subset=['url']) \
    .sort_values('fb_engagement', ascending=False)

app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY])

app.layout = html.Div([
    dcc.Location(id="url"),
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Fake News Sites", href="/")),
            dbc.NavItem(dbc.NavLink("Facebook Engagement", href="/facebook"))
        ],
        brand="Buzzfeed Dashboard",
        brand_href="https://github.com/BuzzFeedNews/2018-12-fake-news-top-50",
        color="primary",
        dark=True
    ),
    html.Div(id="page-content")
])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.P("This is the content of the home page!")
    elif pathname == "/facebook":
        return html.P("This is content for facebook")
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__ == '__main__':
    app.run_server()
