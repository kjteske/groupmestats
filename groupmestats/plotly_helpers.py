import plotly

def try_saving_plotly_figure(figure, filename):
    try:
        plotly.plotly.image.save_as(figure, filename)
    except plotly.exceptions.PlotlyError as e:
        if 'The response from plotly could not be translated.'in str(e):
            print("Failed to save plotly figure. <home>/.plotly/.credentials"
                  " probably not configured correctly?")
        else:
            raise

# A green bar with slightly darker green line
marker = dict(
    color='#4BB541',
    line=dict(
        color='#3A9931',
        width=1.5,
    )
)
