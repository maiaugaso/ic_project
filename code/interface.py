from tkinter import *
from tkinter import ttk
from filters import run_filter, run_wavelet

window = Tk()

#----------------------------------------------------------------------------
#----------------------------filter execution windows------------------------
#----------------------------------------------------------------------------

def wavelet_filter_execution_window():
    filter_exec= Toplevel(window)
    filter_exec.title(f"{filter} Filter")
    filter_exec['background']='#b6cec7'

    lbl = Label(filter_exec, justify='left', anchor='w', wraplengt=600, text="Fill in the empty spaces. The image in which the filter will be applied must be saved in the folder IMAGES and with the name \'img.*' where * corresponds to the file type. It may take a little while to run, be patient.", 
                font=('Verdana 11'), background='#b6cec7')
    lbl.grid(columnspan=2, row=0, sticky = W)

    lbl_J = Label(filter_exec, justify='left', anchor='e',text="Decomposition levels (J):", font=('Verdana 11 bold'), background='#b6cec7')
    lbl_J.grid(column=0, row=2, sticky=E)
    J = Entry(filter_exec, justify='left')
    J.grid(column=1, row=2, sticky=W)

    lbl_w = Label(filter_exec, justify='left', anchor='e',text="Wavelet:", font=('Verdana 11 bold'), background='#b6cec7')
    lbl_w.grid(column=0, row=3, sticky=E)
    w = ttk.Combobox(filter_exec, state="readonly",values=["db1", "db2", "haar", "sym2", "sym4", "coif1"])
    w.grid(column=1, row=3, sticky=W)

    lbl_thresh = Label(filter_exec, justify='left', anchor='e',text="Threshold:", font=('Verdana 11 bold'), background='#b6cec7')
    lbl_thresh.grid(column=0, row=4, sticky=E)
    thresh = ttk.Combobox(filter_exec, state="readonly",values=["hard", "soft"])
    thresh.grid(column=1, row=4, sticky=W)

    lbl_img = Label(filter_exec, justify='left', anchor='e',text="Image Type:", font=('Verdana 11 bold'), background='#b6cec7')
    lbl_img.grid(column=0, row=5, sticky=E)
    img_type = ttk.Combobox(filter_exec, state="readonly",values=["png", "tif"])
    img_type.grid(column=1, row=5, sticky=W)

    b_run =  Button(filter_exec, text="Run", bg = '#86a3c3', width=25, font=('Verdana 10'), 
                    command=lambda: run_wavelet(img_type.get(), w.get(), thresh.get(), int(J.get())))
    b_run.grid(column=1, row=6, pady=5, padx=8)

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
    kernel = Entry(filter_exec, justify='left')
    kernel.grid(column=1, row=2, sticky=W)

    if filter == 'Frost':
        lbl_df2 = Label(filter_exec, justify='left', anchor='e',text="Damp Factor:", font=('Verdana 11 bold'), background='#b6cec7')
        lbl_df2.grid(column=0, row=4, sticky=E)
        damp_factor = Entry(filter_exec, justify='left')
        damp_factor.grid(column=1, row=4, sticky=W)

    if filter == 'Gaussian':
        lbl_sigma = Label(filter_exec, justify='left', anchor='e',text="Sigma:", font=('Verdana 11 bold'), background='#b6cec7')
        lbl_sigma.grid(column=0, row=4, sticky=E)
        sigma = Entry(filter_exec, justify='left')
        sigma.grid(column=1, row=4, sticky=W)
    
    lbl_img = Label(filter_exec, justify='left', anchor='e',text="Image Type:", font=('Verdana 11 bold'), background='#b6cec7')
    lbl_img.grid(column=0, row=5, sticky=E)
    img_type = ttk.Combobox(filter_exec, state="readonly",values=["png", "tif"])
    img_type.grid(column=1, row=5, sticky=W)

    if filter == 'Frost':
        b_run =  Button(filter_exec, text="Run", bg = '#86a3c3', width=25, font=('Verdana 10'), 
                    command=lambda: run_filter(filter, int(kernel.get()), img_type.get(), damp_factor = int(damp_factor.get())))
        b_run.grid(column=1, row=6, pady=5, padx=8)
    elif filter == "Gaussian":
        b_run =  Button(filter_exec, text="Run", bg = '#86a3c3', width=25, font=('Verdana 10'), 
                    command=lambda: run_filter(filter, int(kernel.get()), img_type.get(), sigma = int(sigma.get())))
        b_run.grid(column=1, row=6, pady=5, padx=8)
    else:
        b_run =  Button(filter_exec, text="Run", bg = '#86a3c3', width=25, font=('Verdana 10'), 
                    command=lambda: run_filter(filter, int(kernel.get()), img_type.get()))
        b_run.grid(column=1, row=6, pady=5, padx=8)



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
#-----------------------change detection selection window--------------------
#----------------------------------------------------------------------------
def open_change_window():
    change_options= Toplevel(window)
    change_options.title("Change Detection Methods")
    change_options['background']='#b6cec7'

    lbl = Label(change_options, justify='left', anchor='w', wraplengt=500, 
                text="Choose which change detection method you would like to execute. The image time series will be retrieved from the folder IMAGE_SERIES. These images must be all from the same exact area and dimension. The method works significantly better for a 10+ image time series. ", 
                font=("Verdana 10"), background='#b6cec7')
    lbl.grid(column=0, row=0, sticky=W)

    #buttons
    b_wecs = Button(change_options, text="WECS", bg = '#86a3c3', width=20, font=('Verdana 10'))
    b_wecs.grid(column=0, row=1, pady=5)

    b_ecs = Button(change_options, text="ECS", bg = '#86a3c3', width=20, font=('Verdana 10'))
    b_ecs.grid(column=0, row=2, pady=5)

    b_taad = Button(change_options, text="TAAD", bg = '#86a3c3', width=20, font=('Verdana 10'))
    b_taad.grid(column=0, row=3, pady=5)




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

b_imgobt = Button(window, text="Image obtention", bg = '#86a3c3', width=20, font=('Verdana 10'))
b_imgobt.grid(column=0, row=3, pady=5)

window.mainloop()