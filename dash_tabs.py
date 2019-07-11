import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import dash_table
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as ff
import dash_table as dt
import urllib.parse


##preprocessing for Prateek's part. Used in general stats and interactive outlier analysis
newfuel = pd.read_csv('newfuel.csv')
newfuel = newfuel.drop(['Unnamed: 0','Total Days'],axis=1)
by_district=newfuel.groupby('District')
list_of_options = [{'label':i , 'value':i} for i,j in by_district]
list_of_options.append({'label': 'ALL', 'value': 'ALL'})

##preprocessing for Individual PRV analysis
df = pd.read_csv('cleaned_fuel.csv')
df['Txn Date'] = pd.to_datetime(df['Txn Date'])
df['Odometer'] = pd.to_numeric(df['Odometer'],errors='coerce')
df_dup = df
df = df.set_index('Txn Date')
prv = 1
by_no = df.groupby(['PRV NO.'])
#info = {'prv_no':0, 'district':'', 'mileage':0, 'avg_distance':0, 'total_dist':0}
prv_stats = pd.read_csv('prv_stat.csv')


#Preprocessing for Tab4
monfuel = pd.read_csv('monfuel2.csv')
monfuel = monfuel.drop(['Unnamed: 0','PRV'],axis=1)


df_dup = df_dup.drop(['Unnamed: 0','Terminal ID','Month','District'],axis=1)
by_no_dup = df_dup.groupby(['PRV NO.'])

tab1_content = dbc.Card(
    dbc.CardBody(
        [
            html.Div(children=[
                html.H1(children='GENERAL STATISTICS'),
                dcc.Dropdown(
                    id='input',
                    options=[
                        {'label': 'AVERAGE MILEAGE OF ALL PRVs ', 'value': 'mileage'},
                        {'label': 'TOTAL FUEL CONSUMED', 'value': 'totalFUEL'},
                        {'label': 'TOTAL KMS TRAVELLED', 'value': 'totalKMS'},
                        {'label': 'AVERAGE DISTANCE TRAVELLED IN A DAY', 'value': 'KMs per day'}
                    ],
                    value='mileage'
                ),
                dcc.Dropdown(
                    id='input2',
                    options=list_of_options,
                    value='ALL'
                ),
                html.Div(id='output-graph'),

            ])
        ]
    ),
    className="mt-3",
)

tab2_content = dbc.Card(
    dbc.CardBody(
        [
            dbc.Row([
                dbc.Col([
                    html.H5(['Enter PRV Number:']),
                    dcc.Input(id='input-tab2',value='1',type='text')
                ]),
                dbc.Col([
                    html.Div([],id='info'),
                ]), 
            ]),

            dbc.Row([
                dbc.Col([
                    html.H5(['Transaction History'],style={'margin-bottom':'20px'}),
                    html.Div(id='history'),
                    html.A(
                        'Download Data',
                        id='download-link',
                        download="rawdata.csv",
                        href="",
                        target="_blank"
                    )
                ],style={'padding-top':'29px'}),
                dbc.Col([html.Div(id='output-graph-tab2'),])
            ]),

            dbc.Row([
                dbc.Col([
                    html.Div(id='district-mil'),
                ]),
                dbc.Col([
                    html.Div(id='district-av')
                ])
            ]),
        ]
    ),
    className="mt-3",
)

tab3_content = dbc.Card(
    dbc.CardBody(
        [
            dbc.Row([
                dbc.Col([html.H3(children='INTERACTIVE OUTLIERS FINDER(metric)'),]),
            ]),
            dbc.Row([
                dbc.Col([
                    html.H5(['Enter Lower Bound:']),
                    dbc.Input(id='inputt3',value='8',type='number',placeholder='MINIMUM'),
                ]),
                dbc.Col([
                    html.H5(['Enter Upper Bound:']),
                    dbc.Input(id='input1t3',value='18',type='number',placeholder='MAXIMUM'),
                ]),
            ]),
            dbc.Row([
                dbc.Col([
                    html.H5(['Select Metric:']),

                    dcc.Dropdown(
                        id='input3t3',
                        options=[
                            {'label': 'Mileage', 'value': 'mileage'},
                            {'label': 'Avg. Distance Travelled Per Day','value': 'KMs per day'},
                            {'label': 'Avg Daily Fuel Consumption','value': 'FuelperDay'}
                        ],
                        value='mileage'
                    ),
                ]),
                dbc.Col([
                    html.H5(['District:']),

                    dcc.Dropdown(
                        id='input2t3',
                        options=list_of_options,
                        value='ALL'
                    ),
                ]),
            ]),

            dbc.Row([
                dbc.Col([dcc.Graph(id='pie-chart'),]),
            ]),

            dbc.Row([
                dbc.Col([html.H4(['List of outliers']),]),
                dbc.Col([
                     html.A(
                        'Download Data',
                        id='download-link-outlier',
                        download="outliers.csv",
                        href="",
                        target="_blank"
                    )
                ]),
            ],align='center'),

            dbc.Row([
                dbc.Col([html.Div(id='output-table'),]),
            ],align='center'),
        ]
    ),
    className="mt-3",
)

tab4_content = dbc.Card(
    dbc.CardBody([
        dbc.Row([
            dbc.Col([html.H4('Monthwise Fuel Consumption Report')]),
        ]),
        dbc.Row([
            dbc.Col([html.H5('Select the Lower Bound:'),]),
            dbc.Col([dbc.Input(id='input1t4',value='200',type='number',placeholder='MAX LIMIT OF FUEL/Amount')]),
            #dbc.Col([]),
            dbc.Col([html.H5('Select Metric:')]),
            dbc.Col([dcc.Dropdown(
                        id='input2t4',
                        options=[
                            {'label': 'TOTAL AMOUNT', 'value': 'Amount'},
                            {'label': 'TOTAL FUEL', 'value': 'totalFUEL'},
                        ],value='totalFUEL'),
            ]),

        ]),
        dbc.Row([
            dbc.Col([html.H5('Select Month:')]),
            dbc.Col([
                dcc.Dropdown(
                id='input3t4',
                options=[
                    {'label': 'october', 'value': 'Oct-18'},
                    {'label': 'november', 'value': 'Nov-18'},
                    {'label': 'decemeber', 'value': 'Dec-18'},
                    {'label': 'january', 'value': 'Jan-19'},
                ],value='Jan-19'),
            ]),
            dbc.Col([html.H5('Select District:')]),
            dbc.Col([
                dcc.Dropdown(
                        id='input4t4',
                        options=list_of_options,
                        value='ALL'
                    ),
            ]),
        ]),

        #Next Row is for the output Graph
        dbc.Row([
            dbc.Col([
                html.Div(id='tab4graph'),
            ])
        ]),
        #Last row is for the table
        dbc.Row([
            dbc.Col([
                html.H5('Details:')
            ]),
            dbc.Col([
                html.A(
                        'Download Data',
                        id='download-link-fuelreport',
                        download="fuel_report.csv",
                        href="",
                        target="_blank"
                    )
            ]),
        ]),
        dbc.Row([
            dbc.Col([
                html.Div(id='Tab4Table'),
            ]),
        ]),  
    ]),
    className="mt-3"
)
tabs = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(label="General Statistics", tab_id="tab-1"),
                dbc.Tab(label="PRV Analysis", tab_id="tab-2"),
                dbc.Tab(label="Interactive Outlier Finder",tab_id="tab-3"),
                dbc.Tab(label="Monthly Fuel Report",tab_id="tab-4")
            ],
            id="tabs",
            active_tab="tab-1",
        ),
        html.Div(id="content"),
    ]
)

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Link", href="#"))
    ],
    brand="Fuel Management",
    brand_href="#",
    sticky="top",
)

body = dbc.Container([
    dbc.Row(children = [
        dbc.Col([tabs]),
    ],style={'margin-top':'15px'}),
])

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.config['suppress_callback_exceptions']=True

app.layout = html.Div([navbar,body])

## callback for general statistics
@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='input', component_property='value'),Input(component_id='input2', component_property='value')]
)
def update_value(val1,val2):
    #prv = int(input_data)
   #frame = by_no.get_group(prv)
    con=val1
    con1=val2
    strr="ALL"
    if(con1==strr):
        df1=newfuel
    else:
        df1=newfuel[newfuel['District']==con1]

    return dcc.Graph(
        id='example',
        figure={
            'data':[
                {'x':df1.PRV,'y':df1[con], 'type':'line'}
              ],
            'layout':{
               # 'title':'PRV Number:"{}"'.format(prv)
               'xaxis':{'title':'PRV Numbers'},
               'yaxis':{'title':'{}'.format(con)}
            }
        }
    )

##Callbacks for TAB-2, Individual PRV analysis
@app.callback(
    Output(component_id='output-graph-tab2', component_property='children'),
    [Input(component_id='input-tab2', component_property='value')]
)
def update_value(input_data):
    prv = int(input_data)
    frame = by_no.get_group(prv)

    return dcc.Graph(
        id='example',
        figure={
            'data':[
                {'x':frame.index,'y':frame.Odometer, 'type':'line'}
              ],
            'layout':{
                'title':'PRV Number:"{}"'.format(prv),
                'yaxis':{'title':'Odometer Reading'},
                'xaxis':{'title':'Date'}
            }
        }
    )

@app.callback(
    Output(component_id='info', component_property='children'),
    [Input(component_id='input-tab2', component_property='value')]
)
def show_info(input_data):
    prv = int(input_data)
    district = prv_stats[prv_stats['prv_no']==prv]['district'].values[0]
    mileage = prv_stats[prv_stats['prv_no']==prv]['mileage'].values[0]
    avg_distance = prv_stats[prv_stats['prv_no']==prv]['avg_distance'].values[0]
    total = prv_stats[prv_stats['prv_no']==prv]['total_dist'].values[0]

    row1 = html.Tr([
                html.Td(['PRV Number:']),
                html.Td(['{}'.format(prv)])
            ])
    row2 = html.Tr([
                html.Td(['District:']),
                html.Td(['{}'.format(district)])
            ])
    row3 = html.Tr([
                html.Td(['Mileage:']),
                html.Td(['{}'.format(mileage)])
            ])
    row4 = html.Tr([
                html.Td(['Distance per day(avg):']),
                html.Td(['{}'.format(avg_distance)])
            ])
    row5 = html.Tr([
                html.Td(['Total Distance:']),
                html.Td(['{}'.format(total)])
            ])
    
    table_body = [html.Tbody([row1, row2, row3, row4, row5])]

    table = dbc.Table(table_body, bordered=True)

    return table

@app.callback(
    Output(component_id='history', component_property='children'),
    [Input(component_id='input-tab2', component_property='value')]
)
def gen_history(input_data):
    prv = int(input_data)
    transactions = by_no_dup.get_group(prv)
    transactions = transactions.drop(['PRV NO.'],axis=1)
    return dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in transactions.columns],
        data=transactions.to_dict('records'),
    )

@app.callback(
    Output('download-link', 'href'),
    [Input(component_id='input-tab2', component_property='value')])
def update_download_link(input_data):
    prv = int(input_data)
    transactions = by_no_dup.get_group(prv)
    transactions = transactions.drop(['PRV NO.'],axis=1)
    csv_string = transactions.to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
    return csv_string
## Callbacks for Tab3 
@app.callback(
    Output('download-link-outlier', 'href'),
    [Input(component_id='inputt3', component_property='value'),
    Input(component_id='input1t3', component_property='value'),
    Input(component_id='input2t3', component_property='value'),
    Input(component_id='input3t3', component_property='value'),]

)
def gen_outlier(val,val1,val2,val3):
    val=int(val)
    val1=int(val1)
    con=val2
    strr="ALL"
    metric = val3

    if(con==strr):
        df1=newfuel
        df2 = df1[df1[metric] < val]
        df3 = df1[df1[metric] > val1]
        df4=df2.append(df3)
    else:
        df1=newfuel[newfuel['District']==con]
        df2 = df1[df1[metric] < val]
        df3 = df1[df1[metric] > val1]
        df4=df2.append(df3)
        df4 = df4.drop(['District'],axis = 1)

    csv_string = df4.to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
    return csv_string

@app.callback(
    Output(component_id='output-table', component_property='children'),
    [Input(component_id='inputt3', component_property='value'),
    Input(component_id='input1t3', component_property='value'),
    Input(component_id='input2t3', component_property='value'),
    Input(component_id='input3t3', component_property='value'),]

)
def update_table(val,val1,val2,val3):
    val=int(val)
    val1=int(val1)
    con=val2
    strr="ALL"
    metric = val3

    if(con==strr):
        df1=newfuel
        df2 = df1[df1[metric] < val]
        df3 = df1[df1[metric] > val1]
        df4=df2.append(df3)
    else:
        df1=newfuel[newfuel['District']==con]
        df2 = df1[df1[metric] < val]
        df3 = df1[df1[metric] > val1]
        df4=df2.append(df3)
        df4 = df4.drop(['District'],axis = 1)

    l1=len(df1)
    l2=len(df4)
    l1=l1-l2
    #df1=newfuel.head()
    #new_table_figure = ff.create_table(df1)
    #return new_table_figure

    labels = ['Faulty','Non Faulty']
    values = [l1,l2]

    trace = go.Pie(labels = labels, values=values)

    data = df4.to_dict('rows')
    columns =  [{"name": i, "id": i,} for i in (df4.columns)]
    return dt.DataTable(data=data, columns=columns)

@app.callback(
    Output(component_id='pie-chart', component_property='figure'),
    [Input(component_id='inputt3', component_property='value'),
    Input(component_id='input1t3', component_property='value'),
    Input(component_id='input2t3', component_property='value'),
    Input(component_id='input3t3', component_property='value'),]
)

def update_pie(val,val1,val2,val3):
    val=int(val)
    val1=int(val1)
    con=val2
    strr="ALL"
    metric = val3

    if(con==strr):
        df1=newfuel
        df2 = df1[df1[metric] < val]
        df3 = df1[df1[metric] > val1]
        df4=df2.append(df3)
    else:
        df1=newfuel[newfuel['District']==con]
        df2 = df1[df1[metric] < val]
        df3 = df1[df1[metric] > val1]
        df4=df2.append(df3)
        df4 = df4.drop(['District'],axis = 1)
    l1=len(df1)
    l2=len(df4)
    l1=l1-l2
    #df1=newfuel.head()
    #new_table_figure = ff.create_table(df1)
    #return new_table_figure

    labels = ['Faulty','Non Faulty']
    values = [l2,l1]

    trace = go.Pie(labels = labels, values=values)

    data = df4.to_dict('rows')
    columns =  [{"name": i, "id": i,} for i in (df4.columns)]
    return {
        "data": [trace]
    }
    #return generate_table(df1)

#################################################################
#
#
#Callbacks for Tab 4 
#
#
##################################################################
#Callback for generating the Bar Graph
@app.callback(
    Output(component_id='tab4graph', component_property='children'),
    [Input(component_id='input1t4', component_property='value'),
     Input(component_id='input2t4', component_property='value'),
     Input(component_id='input3t4', component_property='value')]
)
def gengraph(x,metric,month):
    by_month = monfuel.groupby('Month')
    month_df = by_month.get_group(month)
    month_df = month_df[month_df[metric] > int(x)]

    month_df = month_df.groupby('District').count()
    freq = month_df.iloc[:,0]
    freq = freq.reset_index()
    freq.columns = ['District','No. Of PRV']

    freq = freq.sort_values(by =['No. Of PRV'],ascending=False).iloc[0:10]

    '''data = freq.to_dict('rows')
    columns =  [{"name": i, "id": i,} for i in (freq.columns)]
    return dt.DataTable(data=data, columns=columns)
    '''
    return dcc.Graph(
        id='report',
        figure={
            'data':[
                {'x':freq['District'],'y':freq['No. Of PRV'], 'type':'bar'}
              ],
            'layout':{
               # 'title':'PRV Number:"{}"'.format(prv)
            }
        }
    )

#callback for Generating the Table. 
@app.callback(
    Output(component_id='Tab4Table', component_property='children'),
    [Input(component_id='input1t4', component_property='value'),
     Input(component_id='input2t4', component_property='value'),
     Input(component_id='input3t4', component_property='value'),
     Input(component_id='input4t4', component_property='value')]
)
def genTablet4(x,metric,month,district):
    
    by_month = monfuel.groupby('Month')
    month_df = by_month.get_group(month)

    if(district == 'ALL'):
        month_df = month_df[month_df[metric] > int(x)]
    else:
        month_df = month_df.groupby('District')
        month_df = month_df.get_group(district)
        month_df = month_df[month_df[metric] > int(x)]
    
    month_df = month_df.drop(['Total Days','Month'],axis=1)
    
    data = month_df.to_dict('rows')
    columns =  [{"name": i, "id": i,} for i in (month_df.columns)]
    return dt.DataTable(data=data, columns=columns)

@app.callback(
    Output(component_id='download-link-fuelreport', component_property='href'),
    [Input(component_id='input1t4', component_property='value'),
     Input(component_id='input2t4', component_property='value'),
     Input(component_id='input3t4', component_property='value'),
     Input(component_id='input4t4', component_property='value')]
)
def genfuelreport(x,metric,month,district):
    by_month = monfuel.groupby('Month')
    month_df = by_month.get_group(month)

    if(district == 'ALL'):
        month_df = month_df[month_df[metric] > int(x)]
    else:
        month_df = month_df.groupby('District')
        month_df = month_df.get_group(district)
        month_df = month_df[month_df[metric] > int(x)]
    
    month_df = month_df.drop(['Total Days','Month'],axis=1)
    
    csv_string = month_df.to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
    return csv_string
    

##callback for tab switching
@app.callback(Output("content", "children"), [Input("tabs", "active_tab")])
def switch_tab(at):
    if at == "tab-1":
        return tab1_content
    elif at == "tab-2":
        return tab2_content
    elif at == "tab-3":
        return tab3_content
    elif at == "tab-4":
        return tab4_content
    return html.P("This shouldn't ever be displayed...")

if __name__ == "__main__":
    app.run_server(debug=True)