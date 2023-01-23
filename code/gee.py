import ee
import json
from tkinter import messagebox
import os.path
import datetime

def get_bands(selected):
    if len(selected) ==0:
        messagebox.showerror("ERROR", 'Please select at least one band.')

    ref = ['VV', 'VH', 'HV', 'HH']
    bands = []

    for i in range(0,4):
        if selected[i] == 1:
            bands.append(ref[i])

    return bands

def validate_dates(start, end):
    try:
        datetime.datetime.strptime(start, '%Y-%m-%d')
        datetime.datetime.strptime(end, '%Y-%m-%d')
    except:
        messagebox.showerror('ERROR',"Incorrect date format, it should be YYYY-MM-DD.")
        return False

    return True

def verify_directory(output):
    out = os.path.isfile(output)
    
    if (out == False):
        messagebox.showerror("ERROR", "Output file directories is invalid.")
        return False

    return True

def fetch_gee(start_date, end_date, gjson, orbit, selected_bands, folder):
    if verify_directory(gjson) == False:
        return

    if validate_dates(start_date, end_date) == False:
        return

    try:
        with open(gjson) as f:
            geojson = json.load(f)
            coords = geojson['features'][0]['geometry']['coordinates']
    except:
        messagebox.showerror("ERROR", "GeoJson file is not correct.")
        return

    bands = get_bands(selected_bands)
    ee.Initialize()
    ee.Authenticate()
    
    aoi = ee.Geometry.Polygon(coords)

    images = ee.ImageCollection('COPERNICUS/S1_GRD')\
            .filterDate(start_date, end_date)\
            .filterBounds(aoi)\
            .filter(ee.Filter.eq('orbitProperties_pass', orbit))\
            .select(bands)\
            .filter(ee.Filter.contains('.geo', aoi))\
            

    size = images.size().getInfo()
    if size == 0:
        messagebox.showinfo("MESSAGE", "No images where found with the given filters.")
        return
    else:
        image = images.first().clip(aoi)
        date = image.date().format('yyyy-MM-dd').getInfo()
        messagebox.showinfo("MESSAGE", f"A total of {size} images were retrieved. The image to be downloaded is the first from the collection, from {date}.")

    filename = f'Sentinel1_{date}'

    task = ee.batch.Export.image.toDrive(**{
        'image': image,
        'description': filename,
        'scale': 30,
        'folder': folder,
        'region': aoi.getInfo()['coordinates']}
        )

    task.start()
    messagebox.showinfo("MESSAGE", "Download started, it may take a little while.")

