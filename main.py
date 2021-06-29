# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# Script path
from script_dash import run_dash
from init_var import init_var_function
# Dash
import dash
import dash_core_components as dcc
import dash_html_components as html


if __name__ == '__main__':
    dict_media, dict_media_singular = init_var_function()
    app = run_dash(dict_media, dict_media_singular)
    server = app.server
    app.run_server()
