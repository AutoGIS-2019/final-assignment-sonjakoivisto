
#%%

#import modules
import pandas as pd
import geopandas as gpd
import numpy as np
import mapclassify
import matplotlib.pyplot as plt

#initialise variables,define filepaths
fps = ["/Users/sonjakoivisto/Downloads/HelsinkiTravelTimeMatrix2018/data/travel_times_to_ 5931308.txt",
"/Users/sonjakoivisto/Downloads/HelsinkiTravelTimeMatrix2018/data/travel_times_to_ 5949389.txt",
"/Users/sonjakoivisto/Downloads/HelsinkiTravelTimeMatrix2018/data/travel_times_to_ 5960104.txt",
"/Users/sonjakoivisto/Downloads/HelsinkiTravelTimeMatrix2018/data/travel_times_to_ 5975376.txt",
"/Users/sonjakoivisto/Downloads/HelsinkiTravelTimeMatrix2018/data/travel_times_to_ 5972102.txt",
"/Users/sonjakoivisto/Downloads/HelsinkiTravelTimeMatrix2018/data/travel_times_to_ 5961860.txt"]

#table joiner
def TableJoiner(filepaths):
    """
    Gets the YKR grid and merges the grid with accessibility data from chosen grid cells
    """
    i=0

    fpgrid = "/Users/sonjakoivisto/Downloads/HelsinkiTravelTimeMatrix2018/data/MetropAccess_YKR_grid_EurefFIN.shp"
    grid = gpd.read_file(fpgrid)

    #iterate over filepaths
    for fp in filepaths:

        #read in the file
        data = pd.read_csv(fp, sep=";", usecols=["from_id", "bike_f_t", "pt_r_t", "car_r_t"])
        #get the cell number and add it to all travel time columns to distinguish them
        cell_ID = fp.split("_")[-1][:-4]
        new_names = {"from_id": "YKR_ID", "pt_r_t": "pt_r_t_" + cell_ID, "bike_f_t": "bike_f_t_" + cell_ID,
        "car_r_t": "car_r_t_" + cell_ID}
        data= data.rename(columns=new_names)
    
        #merge file with grid on the id of cells and remove no data values
        grid = grid.merge(data, on="YKR_ID")
        grid.replace(to_replace=-1, value=np.nan, inplace=True)
        grid = grid.dropna()

        i+=1

        return grid
    
geodata = TableJoiner(fps)

#visualiser
def visualiser(geodata, column_name): 
    """
    Takes a travel times to a grid cell and visualises them on a map 
    """
    #plot
    fig, ax = plt.subplots(figsize=(10,10))

    #define class breaks to array seen below (upper limits), apply this classification to pt and car travel times
    bins = [5,10,15,20,25,30,35,40,50,55,60]
    classifier = mapclassify.UserDefined(geodata[column_name], bins)
    
    #make new columns with class values
    geodata["classified"] = geodata[[column_name]].apply(classifier)

    #plot the travel times with fast bike
    geodata.plot(ax= ax, column="classified", cmap="RdYlBu")    

    ax.set_title("Travel times")

    plt.tight_layout()
    fig.show()

    output_fig = "traveltimes.png"
    return output_fig


visualiser(geodata,"bike_f_t")

# %%
