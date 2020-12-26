import math

import pandas as pd
import flask
import dash
import dash_core_components as dcc
import dash_html_components as html
import dateutil.parser

millnames = ["", " K", " M", " B", " T"]  # used to convert numbers

# return html Table with dataframe values
def df_to_table(df):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in df.columns])] +

        # Body
        [
            html.Tr(
                [
                    html.Td(df.iloc[i][col])
                    for col in df.columns
                ]
            )
            for i in range(len(df))
        ]
    )


# returns most significant part of a number
def millify(n):
    n = float(n)
    millidx = max(
        0,
        min(
            len(millnames) - 1, int(math.floor(0 if n == 0 else math.log10(abs(n)) / 3))
        ),
    )

    return "{:.0f}{}".format(n / 10 ** (3 * millidx), millnames[millidx])

def thousands(n):
  return ("{:,}".format(n))

# returns top indicator div

def indicator(color, text, id_value):
    return html.Div(
        [

            html.P(
                text,
                className="mini_container"

            ),
            html.P(
                id=id_value,
                className="mini_container"
            ),
        ],
        className="tripleContainer",

    )