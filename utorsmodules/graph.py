import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt
import numpy as np

"""
    This module contains control for all of the graphing
    the program performs.
    
    Its flow is controlled from the graph() method, which
    calls upon barChart() and pieChart() depending on the
    chosen graph type, and makeTitle() as a helper to 
    determine whether to count the time in the title in
    hours or days.
"""

def graph(config, performance, ticks, hours, label, check):
    makeTitle(hours, label)
    if config["graphType"] == "barH":
        barChart(performance, ticks, hours, label, "y", check)
    elif config["graphType"] == "barV":
        barChart(performance, ticks, hours, label, "x", check, rotation=85)
    else:
        pieChart(performance, ticks, hours)

def barChart(performance, ticks, hours, label, axis, check, rotation=0):
    
    y_pos = np.arange(len(ticks))
    
    plt.barh(y_pos, performance, align='center', alpha=0.5) if axis == "y" else plt.bar(y_pos, performance, align='center', alpha=0.5)
    
    plt.yticks(y_pos, ticks) if axis == "y" else plt.xticks(y_pos, ticks, rotation=rotation)
    plt.xlabel(label)
    plt.title(makeTitle(hours, check=check))
    plt.tight_layout()

    plt.show()

def pieChart(performance, ticks, hours, ):
    ticks = tuple(ticks)
    plt.figure(facecolor='#D8D8D8')  
    plt.pie(performance, labels=ticks, autopct='%1.1f%%', shadow=True)
    plt.title(makeTitle(hours))
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

def makeTitle(hours, check="t"):
    if check == "t": return f"Transcriptions completed for various subreddits within the last {hours} hours" if hours <= 24 else f"Transcriptions completed for various subreddits within the last {hours / 24} days"
    elif check == "g": return f"Gamma gained by various volunteers within the last {hours} hours" if hours <= 24 else f"Gamma gained by various volunteers within the last {hours / 24} days"
