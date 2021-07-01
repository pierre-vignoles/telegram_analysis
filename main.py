# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


from script_dash import run_dash
from init_var import init_var_function
import dash
import dash_bootstrap_components as dbc
import dash_auth

if __name__ == '__main__':
    dict_media, dict_media_singular = init_var_function()

    external = [dbc.themes.SLATE]
    app = dash.Dash(__name__, external_stylesheets=external)
    server = app.server

    USERNAME_PASSWORD_PAIRS = [['username', 'password'], ['admin', 'admin']]
    auth = dash_auth.BasicAuth(app, USERNAME_PASSWORD_PAIRS)
    # app.config['suppress_callback_exceptions'] = True

    app = run_dash(dict_media, dict_media_singular, app)

    app.run_server()
