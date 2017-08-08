import plotly.plotly as py
import plotly.graph_objs as go
py.sign_in("madhavimlb", "tkPtwasJ9oHTuXbTAkRM")

if __name__ == '__main__':

    trace1 = go.Bar(
        x=['Calories', 'Protiens', 'Fats', 'Carbohydrates'],
        y=[20, 14, 23],
        name='Actual'
    )

    trace2 = go.Bar(
        x=['Calories', 'Protiens', 'Fats', 'Carbohydrates'],
        y=[20, 14, 23],
        name='SF Zoo'
    )
    data = [trace1,trace2]
    layout = go.Layout(
        barmode='group'
    )

    fig = go.Figure(data=data, layout=layout)
    py.iplot(fig, filename='grouped-bar')


