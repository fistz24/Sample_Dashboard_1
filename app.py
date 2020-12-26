import plotly.express as px
from dash.dependencies import Input, Output, State, ClientsideFunction
import pandas as pd
import plotly_express as px
import plotly.graph_objects as go
import dash
import dash_html_components as html
import dash_core_components as dcc
from definitions import millify, indicator, thousands
from datetime import datetime as dt
from plotly.subplots import make_subplots
import numpy as np

df = pd.read_excel("Sales.xlsx")
pv = pd.pivot_table(df, index=['Month'], columns=["Item"], values=['Revenue'], aggfunc=sum, fill_value=0)
df2 = pd.read_excel("Costs.xlsx")
pv2 = df2.groupby(['Month', 'Type'])['Costs'].sum().unstack(fill_value=0)

print('Ingredients Costs to Date are:', '$', pv2['Ingredients'].sum())
print('Marketing Costs to Date are:', '$', pv2['Marketing'].sum())
print('Fixed Costs to Date are:', '$', pv2['Fixed Cost'].sum())
print('Total Costs to Date are:', '$', df2['Costs'].sum())

#merged = pd.merge(df, df2, on='Month', how='outer')
#merged['Month2'] = merged['Month'].dt.strftime('%Y-%m')
#merged['Month2'] = merged['Month2'].apply(pd.to_datetime)
#grouped_revenues = merged.groupby(['Month'])['Revenue'].sum().reset_index()


df['Month2'] = pd.to_datetime(df['Month'])
df.set_index('Month2', inplace=True)

df2['Month2'] = pd.to_datetime(df2['Month'])
df2.set_index('Month2', inplace=True)

#merged['Month3'] = pd.to_datetime(merged['Month'])
#merged.set_index('Month3', inplace=True)

opts = [dict(label=t, value=t)
        for t in df['Item'].unique()]

opts2 =[dict(label=t, value=t)
        for t in df2['Type'].unique()]

xz= df['Item'].unique()

tot_rev = df['Revenue'].sum()
rev=(df.groupby(['Item'])['Revenue'].sum())/tot_rev
rev2= rev*100
tot_disc= df['Discount'].sum()
disc=(df.groupby(['Item'])['Discount'].sum())/tot_disc
disc2= disc*100

fig5 = make_subplots(rows=1, cols=2, specs =[[{},{}]],shared_xaxes=True,shared_yaxes=False, vertical_spacing=0.005)

fig5.append_trace(go.Bar(
    x=rev2,
    y=xz,
    marker=dict(
        color='rgba(50,171,96,0.6)',
        line=dict(
            color='rgba(50,171,96,1.0)',
            width=1),
    ),
    name='Revenues Contribution(%) by Products',
    orientation='h',
), 1, 1)
fig5.append_trace(go.Scatter(
    x=disc2,
    y=xz,
    mode='lines+markers',
    name='Discount Distributed Classified by Products (%)',
), 1, 2)

fig5.update_layout(
    title='Product Discount & Revenues (%)',
    yaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=True,
        domain=[0, 0.85],
    ),
    yaxis2=dict(
        showgrid=False,
        showline=True,
        showticklabels=False,
        linecolor='rgba(102, 102, 102, 0.8)',
        linewidth=2,
        domain=[0, 0.85],
    ),
    xaxis=dict(
        zeroline=False,
        showline=False,
        showticklabels=True,
        showgrid=True,
        domain=[0, 0.42],
    ),
    xaxis2=dict(
        zeroline=False,
        showline=False,
        showticklabels=True,
        showgrid=True,
        domain=[0.47, 1],
        side='top',
        #dtick=25000,
    ),
    legend=dict(x=0.029, y=1.038, font_size=10),
    margin=dict(l=100, r=20, t=70, b=70),
    paper_bgcolor='rgb(248, 248, 255)',
    plot_bgcolor='rgb(248, 248, 255)',
)

annotations = []

y_s = np.round(rev2, decimals=2)
y_nw = np.round(disc2)


for ydn, yd, xd in zip(y_nw, y_s, xz):
    annotations.append(dict(xref='x2', yref='y2',
                            y=xd, x=ydn,
                            text=str(ydn) + '%',
                            font=dict(family='Arial', size=12,
                                     color='rgb(128,0,128)'),
                           showarrow=False))
    annotations.append(dict(xref='x1', yref='y1',
                        y=xd, x=yd,
                        text=str(yd) + '%',
                        font=dict(family='Arial', size=12,
                                  color='rgb(50,171,96)'),
                        showarrow=False))

annotations.append(dict(xref='paper', yref='paper',
                        x=-0.2, y=-0.109,
                        text='Based on Dates from the first time launching to YTD',
                        font = dict(family='Arial', size=10, color='rgb(150,150,150)'),
                        showarrow = False))
fig5.update_layout(annotations=annotations)

app = dash.Dash(__name__)
server=app.server

app.layout = html.Div(
    [
    html.Div([
        html.Span(" Ini Teh Performance Metrics and Overview", className = 'app-title'),

        html.Div(
            html.Img(src='https://drive.google.com/drive/u/0/search?q=logo'),
            style = {"float":"right","height":"2%"})
        ],
        className="row header"
        ),
    html.Div([
        dcc.Tabs(
            style={"height":"20","verticalAlign":"middle"},
            children=[
            dcc.Tab(label='Overview', children=[
                    dcc.DatePickerRange(
                        id='month_picker',
                        min_date_allowed=dt(2019, 9, 5),
                        max_date_allowed=dt(2030, 12, 12),
                        end_date=dt(2020,5,5),
                        month_format='MMMM, YYYY'
                        ),
            html.Div([
                indicator(
                    "#00cc96",
                    "Total Sales Revenue",
                    "sales_indicator",
                 ),
                indicator(
                    "#119DFF",
                    "Total Costs Incurred",
                    "cost_indicator",
                ),
                indicator(
                    "#EF553B",
                    "Total Cups Sold",
                    "total_cups",
                ),
                indicator(
                    "#EF553B",
                    "Gross Profit",
                    "total_profit",
                ),
            ],
                className="row"
        ),
            html.Div([
                indicator(
                    "#00cc96",
                    "Total Ingredients Costs",
                    "total_ingredients",
            ),
                indicator(
                    "#00cc96",
                    "Total Marketing Costs",
                    "total_marketing",
            ),
                indicator(
                    "#00cc96",
                    "Total Variable Costs",
                    "total_variable",
            ),
                indicator(
                    "#00cc96",
                    "Total Fixed Costs",
                    "total_fixed",
            ),
        ],
                className="row"
        ),
        html.Div(
            dcc.Dropdown(
                id="select_type",
                options=opts,
                multi=True,
                value='Revenue',
                style={"width":"100%"},
            ),
            className="row",
        ),
        html.Div([
            indicator(
                "#00cc96",
                "Revenue by Product",
                "total_product_revenue",
                ),
            indicator(
                "#00cc96",
                "Cups Sold by Product",
                "total_cups_sold",
                ),
            ],
            className="row"
            ),
        html.Div([
            html.P("Total Sales Revenue by Product"),
                dcc.Graph(
                    id="graph1",
                    style={"height": "89%", "width": "98%"},
                    config=dict(displayModeBar=False),
                    className="row",
            ),
        ],
        className="mini_container",
        ),
        html.Div([
            dcc.Dropdown(id='select_cost',
                options=opts2,
                multi=True,
                value='Costs'),
        html.Div([
            html.P("Total Costs by Cost Type"),
                dcc.Graph(
                    id="graph2",
                    style={"height": "89%", "width": "98%"},
                    config=dict(displayModeBar=False),
                    className="row",
            ),
        ],
            className="mini_container",
        )
        ])
        ]),
        # html.Div([
        #     html.P("Total Sales Revenue by Product"),
        #         dcc.Graph(
        #             id="graph1",
        #             style={"height": "90%", "width": "98%"},
        #             config=dict(displayModeBar=False),
        #     ),
        # ]
        # #className="row",
        # ),
        # html.Div([
        #     dcc.Dropdown(id='select_cost',
        #         options=opts2,
        #         multi=True,
        #         value='Costs'),
        # html.Div([
        #     html.P("Total Costs by Cost Type"),
        #         dcc.Graph(
        #             id="graph2",
        #             style={"height": "89%", "width": "98%"},
        #             config=dict(displayModeBar=False),
        #     ),
        # ],
        #     className="row",
        # )
        # ]),
            dcc.Tab(label='Products',children=[
                dcc.Graph(figure=fig5)
                ]
        ),
            dcc.Tab(label='By City', children=[
                dcc.Dropdown(id='select_city',
                             options=opts,
                             style={"width":"75%"},
                             multi=True,
                             ),
                dcc.Graph(
                    id="graph3",
                    style={"height":"87%","width":"95%"},
                    config=dict(displayModeBar=False),
                )
            ])
    ],
colors={
        "border": "gold",
        "primary": "gold",
        "background": "f7a233"}
)
])
])

@app.callback(
    Output("sales_indicator", "children"),
    [Input("month_picker", "start_date"),
     Input("month_picker", "end_date")])

def update_sales(start_date, end_date):
    df3 = df.loc[start_date:end_date]
    sales_revenue = df3['Revenue'].sum()
    return thousands(sales_revenue)


@app.callback(
    Output("cost_indicator", "children"),
    [Input("month_picker", "start_date"),
     Input("month_picker", "end_date")])
def update_cost(start_date, end_date):
    df3 = df2.loc[start_date:end_date]
    total_cost = df3['Costs'].sum()
    return thousands(total_cost)


@app.callback(
    Output("total_cups", "children"),
    [Input("month_picker", "start_date"),
     Input("month_picker", "end_date")])
def update_cups(start_date, end_date):
    df3 = df.loc[start_date:end_date]
    total_cups_sold = df3['Qty'].sum()
    return thousands(total_cups_sold)


@app.callback(
    Output("total_profit", "children"),
    [Input("month_picker", "start_date"),
     Input("month_picker", "end_date")])

def update_profit(start_date, end_date):
    df3 = df.loc[start_date:end_date]
    df4 = df2.loc[start_date:end_date]
    total_profit = (df3['Revenue'].sum() - df4['Costs'].sum())
    return thousands(total_profit)


@app.callback(
    Output("total_ingredients", "children"),
    [Input("month_picker", "start_date"),
     Input("month_picker", "end_date")])
def update_ingredients(start_date, end_date):
    df3 = df2.loc[start_date:end_date]
    filt = (df3['Type'] == 'Ingredients')
    total_ingredients_costs = df3.loc[filt, 'Costs'].sum()
    return thousands(total_ingredients_costs)


@app.callback(
    Output("total_marketing", "children"),
    [Input("month_picker", "start_date"),
     Input("month_picker", "end_date")])
def update_marketing(start_date, end_date):
    df3 = df2.loc[start_date:end_date]
    filt = (df3['Type'] == 'Marketing')
    total_marketing_costs = df3.loc[filt, 'Costs'].sum()
    return thousands(total_marketing_costs)


@app.callback(
    Output("total_variable", "children"),
    [Input("month_picker", "start_date"),
     Input("month_picker", "end_date")])
def update_variable(start_date, end_date):
    df3 = df2.loc[start_date:end_date]
    filt = (df3['Type'] == 'Variable Cost')
    total_variable_costs = df3.loc[filt, 'Costs'].sum()
    return thousands(total_variable_costs)


@app.callback(
    Output("total_fixed", "children"),
    [Input("month_picker", "start_date"),
     Input("month_picker", "end_date")])
def update_fixed(start_date, end_date):
    df3 = df2.loc[start_date:end_date]
    filt = (df3['Type'] == 'Fixed Cost')
    total_fixed_costs = df3.loc[filt, 'Costs'].sum()
    return thousands(total_fixed_costs)


@app.callback(
    Output("total_product_revenue", "children"),
    [Input("month_picker", "start_date"),
     Input("month_picker", "end_date"),
     Input ("select_type", "value")])

def update_total_product_revenues(start_date, end_date, select_type_2):
    select_type_2 = select_type_2 if isinstance(select_type_2, list) else [select_type_2]
    df3 = df.loc[start_date:end_date]
    filt = df3.loc[df3['Item'].isin(select_type_2)]
    sales_revenue = filt['Revenue'].sum()
    #sales_revenue = df3.loc[filt, 'Revenue'].sum()
    #sales_revenue = df3.groupby([df3['Item'].isin(select_type_2)])['Revenue'].sum()
    return thousands(sales_revenue)

@app.callback(
    Output("total_cups_sold", "children"),
    [Input("month_picker", "start_date"),
     Input("month_picker", "end_date"),
     Input ("select_type", "value")])
def update_total_cups_sold(start_date, end_date, select_type_2):
    select_type_2 = select_type_2 if isinstance(select_type_2, list) else [select_type_2]
    df3 = df.loc[start_date:end_date]
    filt = df3.loc[df3['Item'].isin(select_type_2)]
    cups_sold = filt['Qty'].sum()
    #cups_sold = df3.loc[filt, 'Qty'].sum()
    #cups_sold = df3.groupby([df3['Item'].isin(select_type_2)])['Qty'].sum()
    return thousands(cups_sold)

@app.callback(Output('graph1','figure'),
             [Input('select_type','value')])
def make_figure1(select_type_3):
    select_type_3 = select_type_3 if isinstance(select_type_3,list)else [select_type_3]

    fig=px.line(
        df.loc[df['Item'].isin(select_type_3)],
        x='Month',
        y='Revenue',
        color='Item',
        template='presentation',
        category_orders={'Item':['Revenue']},
    )
    return fig.update_traces(mode='lines+markers')

@app.callback(Output('graph2','figure'),
             [Input('select_cost','value')])

def make_figure2(select_types):
    select_types=select_types if isinstance(select_types,list)else [select_types]

    fig=px.scatter(
        df2.loc[df2['Type'].isin(select_types)],
        x='Month',
        y='Costs',
        color='Type',
        #line_dash='Type',
        template='presentation',
        category_orders={'Type':['Costs']},
    )
    return fig.update_traces(mode='lines+markers')

@app.callback(Output('graph3', 'figure'),
    [Input('select_city', 'value')])

def update_graph(select_cities):

    select_cities=select_cities if isinstance(select_cities,list)else [select_cities]
    dff = df.loc[df['Item'].isin(select_cities)]
    fig6 = px.bar(
        dff,
        x='City',
        y='Revenue',
        color='Item',
        hover_data=['Month','Item','Revenue'],
        category_orders={'Item': ['Revenue']},
    )
    return fig6.update_layout(barmode='group')
#)

# app.run_server(port=8081, host ='127.0.0.1')

if __name__ == '__main__':
    app.run_server(port=8080, host ='127.0.0.1')












