"""
6/30/2022
Author: yash14700@gmail.com

Goal is to create a spike raster plot from the excel file
"""

"""
To do:
- think about introduce multiple groups?
"""

from openpyxl import load_workbook
import numpy as np
import matplotlib.pyplot as plt
# from tkinter import Tk
# from tkinter.filedialog import askopenfilename
import sys

SHOW_COUNT = False
blue_THRESHOLD = 5
RED_THRESHOLD = 10

# Get data from the excel file and then turn into a plot
def run_graphing(input_filename=''):
    filename = input_filename
    # if input_filename == '':
    #     Tk().withdraw()
    #     filetypes = (
    #             ('Excel', '*.xl*'),
    #             ('All files', '*.*')
    #         )
    #     filename = askopenfilename(filetypes=filetypes)

    wb = load_workbook(filename)

    activitysheet_idx =  1
    sleepsheet_idx = 2

    def is_start_time(time_idx):
        return time_idx % 2 == 0

    def is_title(time_idx):
        return time_idx == 0

    def get_raw(sheet):
        raw = list()
        for row in sheet:
            raw_row = []
            for value in row:
                if not value is None:
                    raw_row.append(value)
            if len(raw_row) > 0:
                raw.append(raw_row)
        return raw

    # sleeping times
    # TODO(yash14700@gmail.com): finish this

    sheet = wb.worksheets[sleepsheet_idx].values
    raw = get_raw(sheet)

    num_flies = len(raw[1:])
    data_for_plot = list()

    prev_start = 0

    for fly_idx in range(len(raw[1:])):
        fly = raw[1:][fly_idx]
        fly = fly[1:]
        fly_sleep_times = list()
        for time_idx in range(len(fly)):
            if is_start_time(time_idx):
                prev_start = int(fly[time_idx].seconds / 60)
            else:
                end_time = int(fly[time_idx].seconds / 60)
                if end_time > prev_start:
                    fly_sleep_times.extend(list(range(prev_start, end_time)))
                prev_start = end_time
        
        data_for_plot.append(fly_sleep_times)

    ws = wb.worksheets[activitysheet_idx]
    sheet = ws.values

    raw = get_raw(sheet)

    # proboscis points

    def is_time(time_idx):
        return time_idx % 2 == 1

    def is_str(val):
        return type(val) == type('')

    text_for_plot = list()
    y_labels = []
    raw = np.array(raw)
    y_height = 0.3

    blue_points = []
    red_points = []
    for fly in raw[3:]:
        fly_times = []
        fly_text = []
        prev_val = 0
        per_fly_blue = []
        per_fly_red = []
        for time_idx in range(len(fly)):
            if is_time(time_idx):
                prev_val = fly[time_idx].seconds / 60
            else:
                count = fly[time_idx]
                if is_str(count):
                    fly_title = count
                    y_labels.append(fly_title)
                    continue
                # can asssume its the number of times we want to print the previous value
                text_for_plot.append((prev_val, y_height, count))
                for i in range(count):
                    if count < blue_THRESHOLD:
                        fly_times.append(prev_val)
                    elif count < RED_THRESHOLD:
                        per_fly_blue.append(prev_val)
                    else:
                        per_fly_red.append(prev_val)
                    prev_val += 1.5 / 60
    
        data_for_plot.append(fly_times)
        blue_points.append(per_fly_blue)
        red_points.append(per_fly_red)
        y_height+=1


    # add all blue points across flies
    data_for_plot.extend(blue_points)
    # add all red points across flies
    data_for_plot.extend(red_points)

    # plotting
    fig, ax = plt.subplots()
    # print(data_for_plot)
    colors = np.random.rand(len(data_for_plot), 3)
    colors[:num_flies] = [0.75,0.75,0.75] # sleeping gray
    colors[num_flies:2*num_flies] = [0,0,0] #regular black
    colors[2*num_flies : 3*num_flies] = [0,0,1] # blue
    colors[3*num_flies:] = [1,0,0] # red

    created_offsets = np.random.rand(len(data_for_plot))
    created_offsets[:num_flies] = list(range(num_flies)) # sleeping gray
    created_offsets[num_flies:2*num_flies] = list(range(num_flies)) # regular black
    created_offsets[2*num_flies:3*num_flies] = list(range(num_flies)) # blue threshold
    created_offsets[3*num_flies:] = list(range(num_flies)) # red threshold

    #reverse everything
    # data_for_plot = list(reversed(data_for_plot))
    # colors = list(reversed(colors))
    # created_offsets = list(reversed(created_offsets))
    # y_labels = list(reversed(y_labels))

    ax.eventplot(data_for_plot, color=colors, linelengths=0.4, lineoffsets=created_offsets)
    ax.set_yticks(np.arange(num_flies), labels=y_labels)


    if SHOW_COUNT:
        for x,y,txt in text_for_plot:
            plt.text(x,y,txt)

    def on_close(event):
        sys.exit("Plot closed")

    ax.figure.canvas.mpl_connect('close_event', on_close)

    # Draw plot
    # figure = plt.gcf()
    # figure.set_size_inches(18,18)
    final_file = ''
    try:
        filename_without_extension = filename.split('/')[-1]
        filename_without_extension = filename_without_extension.split('.')[0]
        final_file = 'plot_'+filename_without_extension+'.png'
        plt.savefig(final_file, dpi=300, bbox_inches='tight')
    except:
        final_file = 'plot.png'
        plt.savefig(final_file, dpi=300, bbox_inches='tight')

    # Allow user to draw line
    # while True:
    #     xy = plt.ginput(2)
    #     x = [p[0] for p in xy]
    #     y = [p[1] for p in xy]
    #     line = plt.plot(x,y)
    #     ax.figure.canvas.draw()

    return final_file