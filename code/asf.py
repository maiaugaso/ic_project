from os import listdir
import asf_search as asf
from datetime import datetime
from tkinter import messagebox


def fetch_asf(token, polygon, start_date, end_date, max, output):

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

    messagebox.showinfo('MESSAGE',f'There were {len(results)} images retrieved. Download may take some time. When it is done a message box will pop up informing you about the completion of download.')

    results.download(
        path = output,
        session = session, 
        processes = 1 
    )

    messagebox.showinfo('MESSAGE', "Download complete")