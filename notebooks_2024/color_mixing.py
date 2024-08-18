import matplotlib.pyplot as plt
import numpy as np
from sympy import *


from bokeh.layouts import gridplot
from bokeh.models import ColumnDataSource, CustomJS, Slider
from bokeh.plotting import figure, output_file, show, curdoc, output_notebook
from bokeh.models import LinearAxis, Range1d

init_printing(use_latex='mathjax')

def color_mixer(A, img, width=8, height=12):

    A = np.array(A).astype(float)

    if img.dtype == 'uint8':
        img = img.astype(float)/255

    new_img = np.transpose(np.dot(A, np.transpose(img, axes = (0, 2, 1))), axes = (1, 2, 0))
    new_img[new_img < 0] = 0
    new_img[new_img > 1] = 1
    new_img = (255*new_img).astype('uint8')
    plt.figure(figsize=(width,height))
    plt.imshow(new_img)
    plt.show()


def color_sample(*rgb):
    if np.min(rgb) < 0 or np.max(rgb) > 255:
        print("ERROR: RGB coordinates must be intergers in the range 0-255.")
        return None
    rgb = np.array(rgb).astype('uint8')
    sample = np.ones((10,10, 3), dtype='uint8')*rgb
    plt.figure(figsize = (2.5,2.5))
    ax = plt.gca()
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("R {}    G {}    B {}".format(rgb[0], rgb[1], rgb[2]))
    ax.imshow(sample)
    plt.show()




def rgb_sliders():
    """
    Displays an interactive plot showing colors defined by given RGB values.
    """

    # diplay the image in a Jupyter notebook
    output_notebook()

    # initial values of sliders
    vr, vg, vb = 127, 127, 127

    # convert RGB tuple to hexadecimal code
    def rgb_to_hex(rgb):
        return '#%02x%02x%02x' % rgb

    # convert RGB tuple to a string
    def rgb_to_str(*rgb):
        return "R: {}  G: {}  B: {}".format(*rgb)


    # convert hexadecimal to RGB tuple
    def hex_to_dec(hex):
        red = ''.join(hex.strip('#')[0:2])
        green = ''.join(hex.strip('#')[2:4])
        blue = ''.join(hex.strip('#')[4:6])
        return (int(red, 16), int(green, 16), int(blue,16))


    hex_color = rgb_to_hex((vr, vg, vb))

    # initialise the text color as black. This will be switched to white if the block color gets dark enough
    text_color = '#ffffff'

    # create a data source to enable refreshing of fill & text color
    source = ColumnDataSource(data=dict(color=[hex_color], text_color=[text_color], text=[rgb_to_str(vr, vg, vb)]))

    # create plot, as a rect() glyph and centered text label, with fill and text color taken from source
    p1 = figure(x_range=(-8, 8), y_range=(-4, 4),
                width=350, height=200,
                title='move sliders to change color', tools='')

    # added just to get a black frame arund the plot
    p1.extra_x_ranges = {"foox": Range1d(start=-100, end=200)}
    p1.extra_y_ranges = {"fooy": Range1d(start=-100, end=200)}
    p1.add_layout(LinearAxis(x_range_name="foox"), 'above')
    p1.add_layout(LinearAxis(y_range_name="fooy"), 'right')

    p1.xaxis.major_tick_line_color = None  # turn off x-axis major ticks
    p1.xaxis.minor_tick_line_color = None  # turn off x-axis minor ticks
    p1.yaxis.major_tick_line_color = None  # turn off y-axis major ticks
    p1.yaxis.minor_tick_line_color = None  # turn off y-axis minor ticks
    p1.xaxis.major_label_text_font_size = '0pt'  # preferred method for removing tick labels
    p1.yaxis.major_label_text_font_size = '0pt'  # preferred method for removing tick labels


    p1.rect(0, 0, width=18, height=10, fill_color='color',
            line_color = 'black', source=source)

    p1.text(0, 0, text='text', text_color='text_color',
            alpha=0.6667, text_font_size='20pt', text_baseline='middle',
            text_align='center', source=source)

    red_slider = Slider(title="R", start=0, end=255, value=vr, step=1)
    green_slider = Slider(title="G", start=0, end=255, value=vg, step=1)
    blue_slider = Slider(title="B", start=0, end=255, value=vb, step=1)

    # the callback function to update the color of the block and associated label text
    callback = CustomJS(args=dict(source=source, red=red_slider, blue=blue_slider, green=green_slider), code="""
        function componentToHex(c) {
            var hex = c.toString(16)
            return hex.length == 1 ? "0" + hex : hex
        }
        function rgbToHex(r, g, b) {
            return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b)
        }
        function rgbToStr(r, g, b) {
            return "R: " + r.toString() + "  G: " + g.toString() + "  B: " + b.toString()
        }
        function toInt(v) {
           return v | 0
        }
        const color = source.data['color']
        const text_color = source.data['text_color']
        const text = source.data['text']
        const R = toInt(red.value)
        const G = toInt(green.value)
        const B = toInt(blue.value)
        color[0] = rgbToHex(R, G, B)
        text_color[0] = '#ffffff'
        text[0] = rgbToStr(R, G, B)
        if ((R + B  + G > 350)) {
            text_color[0] = '#000000'
        }
        source.change.emit()
    """)

    red_slider.js_on_change('value', callback)
    blue_slider.js_on_change('value', callback)
    green_slider.js_on_change('value', callback)

    show(gridplot([p1, red_slider, green_slider, blue_slider], ncols =1, toolbar_options={"logo":None}))
