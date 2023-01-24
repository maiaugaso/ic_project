from tkinter import *
from tkinter import ttk
from filters import run_filter, run_wavelet
from wecs import run_wecs
from ecs import run_ecs
from taad import run_taad
from asf import fetch_asf
from gee import fetch_gee

window = Tk()

#----------------------------------------------------------------------------
#----------------------------filter execution windows------------------------
#----------------------------------------------------------------------------

def wavelet_filter_execution_window():
    filter_exec= Toplevel(window)
    filter_exec.title(f"{filter} Filter")
    filter_exec['background']='#b6cec7'

    lbl = Label(filter_exec, justify='left', anchor='w', wraplengt=600, text="Fill in the empty spaces. The image in which the filter will be applied must be of ypes png or tif. If it is a multichannel tif the Euclidian Norm will be applied to yield a single channel image.", 
                font=('Verdana 11'), background='#b6cec7')
    lbl.grid(columnspan=2, row=0, sticky = W)

    lbl_J = Label(filter_exec, justify='left', anchor='e',text="Decomposition levels (J):", font=('Verdana 11 bold'), background='#b6cec7')
    lbl_J.grid(column=0, row=2, sticky=E)
    J = Entry(filter_exec, justify='left', width=50)
    J.grid(column=1, row=2, sticky=W)

    lbl_w = Label(filter_exec, justify='left', anchor='e',text="Wavelet:", font=('Verdana 11 bold'), background='#b6cec7')
    lbl_w.grid(column=0, row=3, sticky=E)
    w = ttk.Combobox(filter_exec, state="readonly",values=["db1", "db2", "haar", "sym2", "sym4", "coif1"], width=47)
    w.grid(column=1, row=3, sticky=W)

    lbl_thresh = Label(filter_exec, justify='left', anchor='e',text="Threshold:", font=('Verdana 11 bold'), background='#b6cec7')
    lbl_thresh.grid(column=0, row=4, sticky=E)
    thresh = ttk.Combobox(filter_exec, state="readonly",values=["hard", "soft"], width=47)
    thresh.grid(column=1, row=4, sticky=W)

    lbl_imgdir = Label(filter_exec, justify='left', anchor='e',text="Image path (png or tif):", font=('Verdana 11 bold'), background='#b6cec7')
    lbl_imgdir.grid(column=0, row=5, sticky=E)
    imgdir = Entry(filter_exec, justify='left', width=50)
    imgdir.grid(column=1, row=5, sticky=W)

    lbl_img = Label(filter_exec, justify='left', anchor='e',text="Image Type:", font=('Verdana 11 bold'), background='#b6cec7')
    lbl_img.grid(column=0, row=6, sticky=E)
    img_type = ttk.Combobox(filter_exec, state="readonly",values=["png", "tif"], width=47)
    img_type.grid(column=1, row=6, sticky=W)

    lbl_out = Label(filter_exec, justify='left', anchor='e',text="Output directory:", font=('Verdana 11 bold'), background='#b6cec7')
    lbl_out.grid(column=0, row=7, sticky=E)
    out = Entry(filter_exec, justify='left', width=50)
    out.grid(column=1, row=7, sticky=W)

    b_run =  Button(filter_exec, text="Run", bg = '#86a3c3', width=25, font=('Verdana 10'), 
                    command=lambda: run_wavelet(img_type.get(), w.get(), thresh.get(), int(J.get()), imgdir.get(), out.get()))
    b_run.grid(column=1, row=8, pady=5, padx=8)

def filter_execution_window(filter):
    filter_exec= Toplevel(window)
    filter_exec.title(f"{filter} Filter")
    filter_exec['background']='#b6cec7'

    lbl = Label(filter_exec, justify='left', anchor='w', wraplengt=600, text="Fill in the empty spaces. The image in which the filter will be applied must be saved in the folder IMAGES and with the name \'img.*' where * corresponds to the file type. It may take a little while to run, be patient.", 
                font=('Verdana 11'), background='#b6cec7')
    lbl.grid(columnspan=2, row=0, sticky = W)

    lbl_k = Label(filter_exec,justify='left', anchor='e', text="Kernel size MUST be an ODD number.", font=('Verdana 10'), background='#b6cec7')
    lbl_k.grid(column=0, row=1, sticky=E)
    lbl_k2 = Label(filter_exec, justify='left', anchor='e',text="Kernel Size:", font=('Verdana 11 bold'), background='#b6cec7')
    lbl_k2.grid(column=0, row=2, sticky=E)
    kernel = Entry(filter_exec, justify='left', width=50)
    kernel.grid(column=1, row=2, sticky=W)

    lbl_imgdir = Label(filter_exec, justify='left', anchor='e',text="Image path (png or tif):", font=('Verdana 11 bold'), background='#b6cec7')
    lbl_imgdir.grid(column=0, row=3, sticky=E)
    imgdir = Entry(filter_exec, justify='left', width=50)
    imgdir.grid(column=1, row=3, sticky=W)


    if filter == 'Frost':
        lbl_df2 = Label(filter_exec, justify='left', anchor='e',text="Damp Factor:", font=('Verdana 11 bold'), background='#b6cec7')
        lbl_df2.grid(column=0, row=4, sticky=E)
        damp_factor = Entry(filter_exec, justify='left', width=50)
        damp_factor.grid(column=1, row=4, sticky=W)

    if filter == 'Gaussian':
        lbl_sigma = Label(filter_exec, justify='left', anchor='e',text="Sigma:", font=('Verdana 11 bold'), background='#b6cec7')
        lbl_sigma.grid(column=0, row=4, sticky=E)
        sigma = Entry(filter_exec, justify='left', width=50)
        sigma.grid(column=1, row=4, sticky=W)
    
    lbl_img = Label(filter_exec, justify='left', anchor='e',text="Image Type:", font=('Verdana 11 bold'), background='#b6cec7')
    lbl_img.grid(column=0, row=5, sticky=E)
    img_type = ttk.Combobox(filter_exec, state="readonly",values=["png", "tif"], width=47)
    img_type.grid(column=1, row=5, sticky=W)

    lbl_out = Label(filter_exec, justify='left', anchor='e',text="Output directory:", font=('Verdana 11 bold'), background='#b6cec7')
    lbl_out.grid(column=0, row=6, sticky=E)
    out = Entry(filter_exec, justify='left', width=50)
    out.grid(column=1, row=6, sticky=W)

    if filter == 'Frost':
        b_run =  Button(filter_exec, text="Run", bg = '#86a3c3', width=25, font=('Verdana 10'), 
                    command=lambda: run_filter(filter, int(kernel.get()), img_type.get(), imgdir.get(), out.get(), damp_factor = int(damp_factor.get())))
        b_run.grid(column=1, row=7, pady=5, padx=8)
    elif filter == "Gaussian":
        b_run =  Button(filter_exec, text="Run", bg = '#86a3c3', width=25, font=('Verdana 10'), 
                    command=lambda: run_filter(filter, int(kernel.get()), img_type.get(), imgdir.get(), out.get(), sigma = int(sigma.get())))
        b_run.grid(column=1, row=7, pady=5, padx=8)
    else:
        b_run =  Button(filter_exec, text="Run", bg = '#86a3c3', width=25, font=('Verdana 10'), 
                    command=lambda: run_filter(filter, int(kernel.get()), img_type.get(), imgdir.get(), out.get()))
        b_run.grid(column=1, row=7, pady=5, padx=8)



#----------------------------------------------------------------------------
#----------------------------filter selection window-------------------------
#----------------------------------------------------------------------------
def open_filters_window():
    filters= Toplevel(window)
    filters.title("Filters")
    filters['background']='#b6cec7'

    lbl = Label(filters, text="Choose the filter you want to use.", font=('Verdana 11'), background='#b6cec7')
    lbl.grid(column=0, row=0)

    lbl_simple = Label(filters, text="Simple", font=('Verdana 10 bold'), background='#b6cec7')
    lbl_simple.grid(column=0, row=1, pady=5, padx=8)

    lbl_adap = Label(filters, text="Adaptative", font=('Verdana 10 bold'), background='#b6cec7')
    lbl_adap.grid(column=1, row=1, pady=5, padx=8)

    lbl_wvt = Label(filters, text="Wavelet", font=('Verdana 10 bold'), background='#b6cec7')
    lbl_wvt.grid(column=2, row=1, pady=5, padx=8)

    #simple filters
    b_mean = Button(filters, text="Mean Filter", bg = '#86a3c3', width=25, font=('Verdana 10'), command=lambda: filter_execution_window('Mean'))
    b_mean.grid(column=0, row=2, pady=5, padx=8)

    b_median = Button(filters, text="Median Filter", bg = '#86a3c3', width=25, font=('Verdana 10'), command=lambda: filter_execution_window('Median'))
    b_median.grid(column=0, row=3, pady=5, padx=8)

    b_gauss = Button(filters, text="Gaussian Filter", bg = '#86a3c3', width=25, font=('Verdana 10'), command=lambda: filter_execution_window('Gaussian'))
    b_gauss.grid(column=0, row=4, pady=5, padx=8)

    #adaptative filters
    b_lee = Button(filters, text="Lee Filter", bg = '#86a3c3', width=25, font=('Verdana 10'), command=lambda: filter_execution_window('Lee'))
    b_lee.grid(column=1, row=2, pady=5, padx=8)

    b_kuan = Button(filters, text="Kuan Filter", bg = '#86a3c3', width=25, font=('Verdana 10'), command=lambda: filter_execution_window('Kuan'))
    b_kuan.grid(column=1, row=3, pady=5, padx=8)

    b_frost = Button(filters, text="Frost Filter", bg = '#86a3c3', width=25, font=('Verdana 10'), command=lambda: filter_execution_window('Frost'))
    b_frost.grid(column=1, row=4, pady=5, padx=8)

    #wavelet filter
    b_wvt = Button(filters, text="Wavelet Filter", bg = '#86a3c3', width=25, font=('Verdana 10'), command=wavelet_filter_execution_window)
    b_wvt.grid(column=2, row=2, pady=5, padx=8)

#----------------------------------------------------------------------------
#-----------------------change detection execution window--------------------
#----------------------------------------------------------------------------

def open_change_execution_window(method):
    change= Toplevel(window)
    change.title(method)
    change['background']='#b6cec7'

    lbl = Label(change, justify='left', anchor='w', wraplengt=500, 
                text="The image time series will be retrieved from the folder identified in the \'Image series path:\' space, which must be a folder containing ONLY the desired time series. They all must be from the same exact area and dimension. The method works significantly better for a 10+ image time series.\nEach image must be an individual .tif file with the bands you would like to execute the method on. The bands are combined as the Euclidian Norm, yielding single-channel images. The output directory is where the change maps will be stored.\n ", 
                font=("Verdana 10"), background='#b6cec7')
    lbl.grid(columnspan=2, row=0, sticky=W)

    lbl2 = Label(change, wraplengt=500, text="It may take a while to finish running, please be patient.", 
                font=("Verdana 10 bold"), background='#b6cec7')
    lbl2.grid(columnspan=2, row=1, pady=5)

    lbl3 = Label(change, wraplengt=500, text="Make sure all conditions are met.", 
                font=("Verdana 11 bold"), background='#b6cec7', fg='red')
    lbl3.grid(columnspan=2, row=2, pady=5)

    lbl_seriesdir = Label(change, justify='left', anchor='e',text="Image series path:", font=('Verdana 11 bold'), background='#b6cec7')
    lbl_seriesdir.grid(column=0, row=3, sticky=E)
    seriesdir = Entry(change, justify='left', width=50)
    seriesdir.grid(column=1, row=3, sticky=W)

    lbl_out = Label(change, justify='left', anchor='e',text="Output directory:", font=('Verdana 11 bold'), background='#b6cec7')
    lbl_out.grid(column=0, row=4, sticky=E)
    out = Entry(change, justify='left', width=50)
    out.grid(column=1, row=4, sticky=W)

    if method == 'WECS':
        b_run = Button(change, text="Run", bg = '#86a3c3', width=20, font=('Verdana 10'), command=lambda: run_wecs(seriesdir.get(), out.get()))
        b_run.grid(column=1, row=5, pady=10)
    if method == 'ECS':
        b_run = Button(change, text="Run", bg = '#86a3c3', width=20, font=('Verdana 10'), command=lambda: run_ecs(seriesdir.get(), out.get()))
        b_run.grid(column=1, row=5, pady=10)
    if method == 'TAAD':
        b_run = Button(change, text="Run", bg = '#86a3c3', width=20, font=('Verdana 10'), command=lambda: run_taad(seriesdir.get(), out.get()))
        b_run.grid(column=1, row=5, pady=10)


#----------------------------------------------------------------------------
#-----------------------change detection selection window--------------------
#----------------------------------------------------------------------------
def open_change_window():
    change_options= Toplevel(window)
    change_options.title("Change Detection Methods")
    change_options['background']='#b6cec7'

    lbl = Label(change_options, justify='left', anchor='w', wraplengt=500, 
                text="Choose which change detection method you would like to execute. ", 
                font=("Verdana 10"), background='#b6cec7')
    lbl.grid(column=0, row=0, sticky=W)

    #buttons
    b_wecs = Button(change_options, text="WECS", bg = '#86a3c3', width=20, font=('Verdana 10'), command=lambda: open_change_execution_window("WECS"))
    b_wecs.grid(column=0, row=1, pady=5)

    b_ecs = Button(change_options, text="ECS", bg = '#86a3c3', width=20, font=('Verdana 10'), command=lambda: open_change_execution_window("ECS"))
    b_ecs.grid(column=0, row=2, pady=5)

    b_taad = Button(change_options, text="TAAD", bg = '#86a3c3', width=20, font=('Verdana 10'), command=lambda: open_change_execution_window("TAAD"))
    b_taad.grid(column=0, row=3, pady=5)


#----------------------------------------------------------------------------
#--------------------image obtention execution windows-----------------------
#----------------------------------------------------------------------------

def open_asf():
    asf= Toplevel(window)
    asf.title("ASF Search API")
    asf['background']='#b6cec7'

    asf.geometry('550x450')

    lbl = Label(asf, justify='left', anchor='w', wraplength= 540,
                text="To use this API it is necessary to have an account on NASA's Earth Data (https://urs.earthdata.nasa.gov/). Fill in the empty spaces.\nThis API retrieves an entire scene containing the area of interest, this means files can be very heavy (1-2GB) and download will take a while.\n ", 
                font=("Verdana 10"), background='#b6cec7')
    lbl.grid(columnspan=2, row=0, sticky=W)

    lbl = Label(asf, justify='left',  wraplength=540,
                text="The authentication token can be retrieved from you personal account on the website above.", 
                font=("Verdana 8"), background='#b6cec7')
    lbl.grid(columnspan=2, row=1)
    lbl_token = Label(asf, justify='left', anchor='e',text="Authentication Token:", font=('Verdana 11 bold'), background='#b6cec7')
    lbl_token.grid(column=0, row=2, sticky=E)
    token = Entry(asf, justify='left', width=50)
    token.grid(column=1, row=2, sticky=W)

    lbl_startdate = Label(asf, justify='left', anchor='e',text="Start date (YYYY-MM-DD):", font=('Verdana 11 bold'), background='#b6cec7')
    lbl_startdate.grid(column=0, row=3, sticky=E)
    startdate = Entry(asf, justify='left', width=50)
    startdate.grid(column=1, row=3, sticky=W)

    lbl_enddate = Label(asf, justify='left', anchor='e',text="End date (YYYY-MM-DD):", font=('Verdana 11 bold'), background='#b6cec7')
    lbl_enddate.grid(column=0, row=4, sticky=E)
    enddate = Entry(asf, justify='left', width=50)
    enddate.grid(column=1, row=4, sticky=W)

    lbl2 = Label(asf, justify='left', wraplength=540,
                text="Maximum number of images to retrieve, from 1 to 10. The highest the number, the longer it will take.", 
                font=("Verdana 8"), background='#b6cec7')
    lbl2.grid(columnspan=2, row=5)
    lbl_max = Label(asf, justify='left', anchor='e',text="Max images:", font=('Verdana 11 bold'), background='#b6cec7')
    lbl_max.grid(column=0, row=6, sticky=E)
    max = Entry(asf, justify='left', width=50)
    max.grid(column=1, row=6, sticky=W)

    lbl_out = Label(asf, justify='left', anchor='e',text="Output directory:", font=('Verdana 11 bold'), background='#b6cec7')
    lbl_out.grid(column=0, row=7, sticky=E)
    out = Entry(asf, justify='left', width=50)
    out.grid(column=1, row=7, sticky=W)
    
    lbl2 = Label(asf, justify='left', wraplength=540,
                text="Fill the area of interest as a WKT Polygon. It must be in the following format. The components lat_i and long_i are the coordinates for a vertex in the polygon. It is recommended to follow a rectangle. The last component of the polygon below is the same as the first so that the polygon vertices “close”. \nThis way If you follow a rectangle, there must be 5 components of lat long. Pay attention to the double brackets.\nIt is easy to generate one through the website http://arthur-e.github.io/Wicket/sandbox-gmaps3.html \nExample: POLYGON((lat_1 long_1, lat_2 long_2, …, la_tn long_n, lat_1 long_1))", 
                font=("Verdana 8"), background='#b6cec7')
    lbl2.grid(columnspan=2, row=8)
    lbl_poly = Label(asf, justify='left', anchor='e',text="Area of interest:", font=('Verdana 11 bold'), background='#b6cec7')
    lbl_poly.grid(column=0, row=9, sticky=E)
    poly = Entry(asf, justify='left', width=50)
    poly.grid(column=1, row=9, sticky=W)

    b_run =  Button(asf, text="Run", bg = '#86a3c3', width=25, font=('Verdana 10'), 
                    command=lambda: fetch_asf(token.get(), poly.get(), startdate.get(), enddate.get(), int(max.get()), out.get()))
    b_run.grid(column=1, row=10, pady=5, padx=8)

def open_gee():
    gee= Toplevel(window)
    gee.title("Google Earth Engine API")
    gee['background']='#b6cec7'

    lbl = Label(gee, justify='left', anchor='w', wraplength= 540,
                text="To use this API it is necessary to have an account on Google Earth Engine and local computer installation of the API (https://earthengine.google.com/). Fill in the empty spaces.\nThis API retrieves a single tif image of the area specified in the GEOJSON txt file. If this area is too big, the image might not download due to the limit of the file size set by the API. \nIt will be downloaded to a folder in your personal Google Drive, that is, the account in which your GEE is connected to. Download may take a while.\nOnce you click run, a window will appear from the Google Earth Engine Authenticator, where you need to confirm your email. ", 
                font=("Verdana 10"), background='#b6cec7')
    lbl.grid(columnspan=2, row=0, sticky=W)

    lbl_startdate = Label(gee, justify='left', anchor='e',text="Start date (YYYY-MM-DD):", font=('Verdana 11 bold'), background='#b6cec7')
    lbl_startdate.grid(column=0, row=1, sticky=E)
    startdate = Entry(gee, justify='left', width=50)
    startdate.grid(column=1, row=1, sticky=W)

    lbl_enddate = Label(gee, justify='left', anchor='e',text="End date (YYYY-MM-DD):", font=('Verdana 11 bold'), background='#b6cec7')
    lbl_enddate.grid(column=0, row=2, sticky=E)
    enddate = Entry(gee, justify='left', width=50)
    enddate.grid(column=1, row=2, sticky=W)

    lbl_orbit = Label(gee, justify='left', anchor='e',text="Orbit:", font=('Verdana 11 bold'), background='#b6cec7')
    lbl_orbit.grid(column=0, row=3, sticky=E)
    orbit = ttk.Combobox(gee, state="readonly",values=["ASCENDING", "DESCENDING"], width=47)
    orbit.grid(column=1, row=3, sticky=W)

    lbl2 = Label(gee, justify='left',  wraplength=540,
                text="Name of the folder in your Google Drive that the image will be saved. Can be an existing one or a new one, in which it will be created.", 
                font=("Verdana 8"), background='#b6cec7')
    lbl2.grid(columnspan=2, row=4)
    lbl_folder = Label(gee, justify='left', anchor='e',text="Folder name:", font=('Verdana 11 bold'), background='#b6cec7')
    lbl_folder.grid(column=0, row=5, sticky=E)
    folder = Entry(gee, justify='left', width=50)
    folder.grid(column=1, row=5, sticky=W)

    VV = IntVar()
    VH = IntVar()
    HV = IntVar()
    HH = IntVar()
    lbl_bands = Label(gee, justify='left', anchor='e',text="Select bands:", font=('Verdana 11 bold'), background='#b6cec7')
    lbl_bands.grid(column=0, row=6, sticky=E)
    VV_ = Checkbutton(gee, text='VV',variable=VV, onvalue=1, offvalue=0, background='#b6cec7')
    VV_.grid(column=1, row=6, sticky=W)
    VH_ = Checkbutton(gee, text='VH',variable=VH, onvalue=1, offvalue=0, background='#b6cec7')
    VH_.grid(column=1, row=7, sticky=W)
    HV_ = Checkbutton(gee, text='HV',variable=HV, onvalue=1, offvalue=0, background='#b6cec7')
    HV_.grid(column=1, row=8, sticky=W)
    HH_ = Checkbutton(gee, text='HH',variable=HH, onvalue=1, offvalue=0, background='#b6cec7')
    HH_.grid(column=1, row=9, sticky=W)

    lbl3 = Label(gee, justify='left',  wraplength=540,
                text="The area of interest must be a Polygon in GEOJSON format, saved in a .txt file. You will provide the path to this file.\nYou can easily generate one through the website http://geojson.io/#map=2/20.0/0.0 and copy it into a .txt file.", 
                font=("Verdana 8"), background='#b6cec7')
    lbl3.grid(columnspan=2, row=10)
    lbl_aoi = Label(gee, justify='left', anchor='e',text="Area of interest path:", font=('Verdana 11 bold'), background='#b6cec7')
    lbl_aoi.grid(column=0, row=11, sticky=E)
    aoi = Entry(gee, justify='left', width=50)
    aoi.grid(column=1, row=11, sticky=W)

    b_run =  Button(gee, text="Run", bg = '#86a3c3', width=25, font=('Verdana 10'), 
                    command=lambda: fetch_gee(startdate.get(), enddate.get(), aoi.get(), orbit.get(), [VV.get(), VH.get(), HV.get(), HH.get()], folder.get()))
    b_run.grid(column=1, row=12, pady=5, padx=8)


#----------------------------------------------------------------------------
#--------------------image obtention selection window------------------------
#----------------------------------------------------------------------------
def open_obtetion_window():
    obtention= Toplevel(window)
    obtention.title("Sentinel-1 Image Obtention")
    obtention['background']='#b6cec7'

    lbl = Label(obtention, justify='left', anchor='w', wraplengt=500, 
                text="Choose which API would like to retrieve an image from. ", 
                font=("Verdana 10"), background='#b6cec7')
    lbl.grid(column=0, row=0, sticky=W)

    #buttons
    b_gee = Button(obtention, text="Google Earth Engine", bg = '#86a3c3', width=20, font=('Verdana 10'), command=open_gee)
    b_gee.grid(column=0, row=1, pady=5)

    b_asf = Button(obtention, text="ASF Search", bg = '#86a3c3', width=20, font=('Verdana 10'), command=open_asf)
    b_asf.grid(column=0, row=2, pady=5)


#----------------------------------------------------------------------------
#----------------------------main window-------------------------------------
#----------------------------------------------------------------------------
window.title("SAR Image Analysis Tools")
window['background']='#b6cec7'
#window.geometry('500x500') 

lbl = Label(window, text="Choose which tool you would like to execute.", font=("Verdana 10"), background='#b6cec7')
lbl.grid(column=0, row=0)

#buttons
b_filters = Button(window, text="Filters", bg = '#86a3c3', width=20, font=('Verdana 10'), command=open_filters_window)
b_filters.grid(column=0, row=1, pady=5)

b_change = Button(window, text="Change Detection", bg = '#86a3c3', width=20, font=('Verdana 10'), command=open_change_window)
b_change.grid(column=0, row=2, pady=5)

b_imgobt = Button(window, text="Image obtention", bg = '#86a3c3', width=20, font=('Verdana 10'), command=open_obtetion_window)
b_imgobt.grid(column=0, row=3, pady=5)

window.mainloop()