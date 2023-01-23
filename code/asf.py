from os import listdir
import asf_search as asf
from datetime import datetime
from tkinter import messagebox
import os.path
from importlib_metadata import metadata

metadata.__str__

def verify_directory(output):
    out = os.path.isdir(output)

    if (out == False):
        messagebox.showerror("ERROR", "Output file directory is invalid.")
        return False

    return True

def validate_dates(start, end):
    try:
        datetime.datetime.strptime(start, '%Y-%m-%d')
        datetime.datetime.strptime(end, '%Y-%m-%d')
    except:
        messagebox.showerror('ERROR',"Incorrect date format, it should be YYYY-MM-DD.")
        return False

    return True


def fetch_asf(token, polygon, start_date, end_date, max, output):
    if verify_directory(output) == False:
        return

    if validate_dates(start_date, end_date) == False:
        return

    try:
        session = asf.ASFSession().auth_with_token(token)
    except:
        messagebox.showerror('ERROR',"Invalid authentication token!")
        return

    results = asf.geo_search(
    intersectsWith=polygon, 
    platform=asf.PLATFORM.SENTINEL1A,
    processingLevel=[asf.PRODUCT_TYPE.GRD_HD],
    start = start_date, 
    end = end_date,
    maxResults=max
    )

    size = len(results)
    if size == 0:
        messagebox.showinfo("MESSAGE", "No images where found with the given filters.")
        return
    else:
        messagebox.showinfo('MESSAGE',f'There were {size} images retrieved. Download may take some time. When it is done a message box will pop up informing you about the completion of download.')

    results.download(
        path = output,
        session = session, 
        processes = 1 
    )

    messagebox.showinfo('MESSAGE', "Download complete")