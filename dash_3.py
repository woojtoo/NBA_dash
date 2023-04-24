from dash import dcc, html, Dash
from dash.dependencies import Input, Output
# import pandas_datareader.data as web
import datetime

# start = datetime.datetime(2015, 1, 1)
# end = datetime.datetime(2018, 2, 8)
# stock = 'TSLA'
# df = web.DataReader(stock, 'stooq', start, end)
# print(df.head())
input_data=''

app =  Dash()

app.layout = html.Div(children=[html.H1('Stock {}'.format(input_data)),
                                dcc.Input(id='input', value='', type='text'),
                                html.Div(id='output-graf'),
                                # dcc.Graph(id='example',
                                #           figure={'data': [{'x': df.index, 'y': df['Close'], 'type': 'line', 'name': stock}],
                                #                   'layout': {'title': stock}
                                #                   }
                                #           ),
                                ]
                      )


@app.callback(Output(component_id='output-graf', component_property='children'),
              [Input(component_id='input', component_property='value')])
def update_graf(input_data):
    start = datetime.datetime(2015, 1, 1)
    end = datetime.datetime(2018, 2, 8)
    df = web.DataReader(input_data, 'stooq', start, end)


    return dcc.Graph(id='example',
                     figure={'data': [{'x': df.index, 'y': df['Close'], 'type': 'line', 'name': input_data}],
                             'layout': {'title': input_data}
                             }
                     )

if __name__ == '__main__':
    app.run_server(debug=True)
