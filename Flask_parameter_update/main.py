import numpy as np
np.random.seed(0)

from bokeh.io import curdoc
from bokeh.layouts import widgetbox, row, column, gridplot
from bokeh.models import ColumnDataSource, Select, Slider
from bokeh.plotting import figure
from bokeh.palettes import Greys256
from bokeh.models.callbacks import CustomJS

from skimage.feature import blob_doh
from skimage.io import imread
from skimage.color import rgb2gray
from skimage.util import invert


# define some helper functions
def Load_image(path):
    """
    :param path     path to image file

    Function that reads image, takes a patch, converts to gray
    Returns processed image and inverted image
    """
    # read test image
    im = imread(path)
    # take patch of image and convert to grayscale
    im = im[:1024,:1024]
    #im = im[:256,:256]
    im = rgb2gray(im)

    # prepare an inverted image for comparison
    # search for white blobs on black background AND black blobs on white background
    imIn = invert(im)
    return im, imIn

#Real Callback function
def blob_detector(imIn, overlap, threshold, min_sigma, max_sigma, log_scale):
    """

    :param imIn:        Inverted Image grayscale patch
    :param:             Hyper-Parameters for blob detector
        :overlap
        :threshold
        :min_sigma
        :max_sigma
        log_scale
    :return:
    """
    # Initialize and Invoke DoH blob detector
    blobs_doh = blob_doh(imIn, overlap=overlap, threshold=threshold, min_sigma=min_sigma,
                         max_sigma=max_sigma, log_scale=log_scale)
    #blobs_y, blobs_x, blobs_r = [],[],[]
    blobs_y = blobs_doh[:,0]
    blobs_x = blobs_doh[:,1]
    blobs_r = blobs_doh[:,2]
    """for blob in blobs_doh:
        y, x, r = blob # This code can be made better
        blobs_y.append(y)
        blobs_x.append(x)
        blobs_r.append(r)"""
    return blobs_y, blobs_x, blobs_r

# set up more callbacks
def update_blob_detector(attrname, old, new):
    global imIn
    logscale = logscale_select.value
    maxSigma = maxSigma_slider.value
    minSigma = minSigma_slider.value
    threshold = threshold_slider.value
    overlap = overlap_slider.value
    print("Calculating Blobs ..........")
    blobs_y, blobs_x, blobs_r = blob_detector(imIn, overlap, threshold, minSigma, maxSigma, logscale)
    source.data = dict(x=blobs_x, y= blobs_y, r=blobs_r)
    print("blobs updated")

def save_params(attrname, old, new):
    logscale = logscale_select.value
    maxSigma = maxSigma_slider.value
    minSigma = minSigma_slider.value
    threshold = threshold_slider.value
    overlap = overlap_slider.value
    input = str(logscale) +','+ str(maxSigma) +','+ str(minSigma) +','+ str(threshold) +','+ str(overlap)+'\n'
    if button.value:
        with open('./Flask_parameter_update/output.txt', 'a') as file:
            file.writelines(input)
    print('Params saved')


# set up widgets
logscale_vals=['True', 'False']
logscale_select = Select(value='True',
                          title='Logscale',
                          width=200,
                          options=logscale_vals)
overlap_slider = Slider(title="Overlap Parameter",
                        value=0.5,
                        start=0.0,
                        end=1.0,
                        step=0.1,
                        width=200)

threshold_slider = Slider(title="Filter Threshold",
                         value=0.005,
                         start=0.001,
                         end=0.1,
                         step=0.005,
                         width=200)

minSigma_slider = Slider(title="min_Sigma",
                         value=5,
                         start=0.0,
                         end=500.0,
                         step=2,
                         width=200)

maxSigma_slider = Slider(title="max_Sigma",
                         value=50,
                         start=0.0,
                         end=500.0,
                         step=2,
                         width=200,)

button_vals=['True', 'False']
button = Select(value='False',
                          title='Save Hyperparameters?',
                          width=200,
                          options=button_vals)

# set up plot (styling in theme.yaml)
path = './Flask_parameter_update/static/B4_2_test_500x.tif'
im, imIn = Load_image(path)
blobs_y, blobs_x, blobs_r = blob_detector(imIn, 0.5,0.005,5,50,True)
im_x = im.shape[0]
im_y = im.shape[1]

source = ColumnDataSource(data=dict(x=blobs_x, y= blobs_y, r=blobs_r))

# create a new plot
s2 = figure(plot_width=900, plot_height= 900, title='With Blobs', x_range= (0,im_x), y_range=(0,im_y))
# Superimpose DoH blobs on image
s2.image(image=[imIn], x=[0], y=[0], dw=[im_x], dh=[im_y], palette=list(reversed(Greys256)))
s2.circle( 'x', 'y', size= 'r', line_color='green', fill_color= None, line_width=1, fill_alpha=0.8, source=source)



#Callback Functions
logscale_select.on_change('value', update_blob_detector)
overlap_slider.on_change('value', update_blob_detector)
threshold_slider.on_change('value', update_blob_detector)
minSigma_slider.on_change('value', update_blob_detector)
maxSigma_slider.on_change('value', update_blob_detector)
button.on_change('value', save_params)


# set up layout
selects = row(logscale_select, width=200)
inputs = column(selects, widgetbox(overlap_slider, threshold_slider, minSigma_slider, maxSigma_slider, button))

# add to document
curdoc().add_root(row(inputs,s2))

#Inputs
#wbox = widgetbox(overlap_slider, threshold_slider, minSigma_slider, maxSigma_slider, width=200)
#curdoc().add_root(row(wbox,s1,s2))
curdoc().title = "Bokeh Parameter Search"