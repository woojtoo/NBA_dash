from dash import dcc, html, Dash, Input, Output
import plotly
import random
import plotly.graph_objs as go
from collections import deque

X= deque(maxlen=20)
Y= deque(maxlen=20)
X.append(1)
Y.append(1)

app = Dash(__name__)
app.layout = html.Div([dcc.Graph(id = 'live-graf', animate = True),
                       dcc.Interval(id='graf-update', interval=1000, n_intervals=0)])

@app.callback(Output('live-graf', 'figure'),
              [Input('graf-update', 'n_intervals')])
def update_graf(n):
    global X
    global Y
    X.append(X[-1] + 1)
    Y.append(Y[-1] + (Y[-1] * random.uniform(-0.1, 0.1)))

    data = go.Scatter(x=list(X),
                      y=list(Y),
                      name='Scatter',
                      mode='lines+markers')

    return {'data': [data], 'layout': go.Layout(xaxis=dict(range=[min(X), max(X)]),
                                                yaxis=dict(range=[min(Y), max(Y)]))}


if __name__ == '__main__':
    app.run_server(debug=True)