# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# Script path
from script_dash import run_dash
from init_var import init_var_function
import dash
import dash_bootstrap_components as dbc


if __name__ == '__main__':
    dict_media, dict_media_singular = init_var_function()

    external = [dbc.themes.SLATE]
    app = dash.Dash(__name__, external_stylesheets=external)
    server = app.server

    app = run_dash(dict_media, dict_media_singular, app)
    app.run_server()