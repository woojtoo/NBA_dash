from dash import dcc, html, Dash

app = Dash()

app.layout = html.Div(children=[html.H1('Dash tutorials'),
                                dcc.Graph(id='example',
                                          figure={'data': [{'x': [1,2,3,4,5], 'y': [5,1,7,8,2], 'type': 'line', 'name': 'blabla'},
                                                           {'x': [1,2,3,4,5], 'y': [1,5,7,6,4], 'type': 'bar', 'name': 'gugugu'}],
                                                  'layout': {'title': 'Basis'}
                                                  }
                                          ),
                                ]
                      )




if __name__ == '__main__':
    app.run_server(debug=True)
