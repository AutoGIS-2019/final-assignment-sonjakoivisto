#import modules and dependencies
#If this is giving an error about scalebar, run: "pip install matplotlib-scalebar" in the terminal
import pandas as pd
import geopandas as gpd
import numpy as np
import mapclassify
import matplotlib.pyplot as plt
import folium
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib_scalebar.scalebar import ScaleBar
import contextily as ctx
import os.path 



def CellChecker():
    """
    This function can be called when you want to find out the YKR_ID of certain area before starting your analysis. When you hover over the map it shows the YKR_ID of that cell. This ID is needed as an input for the FileFinder function to start your analysis. You can pan and zoom the map.
    """
    #access the YKR grid and read it in with Pandas
    fpgrid = "data/MetropAccess_YKR_grid_EurefFIN.shp"
    grid = gpd.read_file(fpgrid)
    
    #add a basemap with Folium from OpenStreetMap
    m = folium.Map(location=[60.25, 24.8], tiles = "OpenStreetMap", zoom_start=10, control_scale=True,
                    attribution = "Data: YKR grid")
    
    #add tooltips (info when hovering over) as geoJson
    folium.GeoJson(grid, name="YKR_IDs", smooth_factor=2,
                   style_function=lambda x: {'weight':0.2,'color':'#807e7e', 'fillOpacity':0},
                   highlight_function=lambda x: {'weight':1.5, 'color':'black'},
                  tooltip=folium.GeoJsonTooltip(fields=["YKR_ID"],labels=True, sticky=False)).add_to(m)
    
    #add layer control
    folium.LayerControl().add_to(m)
    
    #save in the outputs folder as html
    outfp = "outputs/YKR_gridmap.html"
    m.save(outfp)
    return m




def FileFinder(YKR_ids):
    """
    Gets the data for certain cell of Helsinki Travel time matrix. Insert a list of YKR ids. 
    """
    filepaths = []
    
    if(type(YKR_ids)!=list):
        print("Please make sure that input is a list")
    
    for num, i in enumerate(YKR_ids):
        
        folder = str(i)[0:4]
        
        fp = r"data/" + folder + "/travel_times_to_ " + str(i) + ".txt"
        print("Processing file " + fp + ". Progress: " + str(num+1) + "/" + str(len(YKR_ids)))
        if(os.path.isfile(fp)==False):
            print("WARNING: FILE DOES NOT EXIST")
        filepaths.append(fp)
    
    return filepaths


def TableJoiner(filepaths):
    """
    Gets the YKR grid and merges the grid with accessibility data from chosen grid cells.
    """

    #access the YKR grid to get the spatial extent and geometry (has to be saved in data folder)
    fpgrid = "data/MetropAccess_YKR_grid_EurefFIN.shp"
    grid = gpd.read_file(fpgrid)

    #iterate over filepaths
    for i, fp in enumerate(filepaths):

        #read in the file
        data = pd.read_csv(fp, sep=";", usecols=["from_id", "bike_f_t", "pt_r_t", "car_r_t"])
        #get the cell number and add it to all travel time columns to distinguish them
        cell_ID = fp.split("_")[-1][:-4]
        new_names = {"from_id": "YKR_ID", "bike_f_t": "bike_f_t_" + str(i), "pt_r_t": "pt_r_t_" + str(i),
                    "car_r_t": "car_r_t_" + str(i)}
        data= data.rename(columns=new_names)
    
        #merge file with grid on the id of cells and remove no data values
        grid = grid.merge(data, on="YKR_ID")
        grid.replace(to_replace=-1, value=np.nan, inplace=True)
        grid = grid.dropna()

    #initialise empty columns for minimum travel times
    grid["min_t_bike"] = None
    grid["min_t_car"] = None
    grid["min_t_pt"] = None

    
    #if there are multiple destination points, count the minimum travel time to closest destination point
    if(len(filepaths)>1):
        
        #first assign all columns starting with "bike" to variable bike_cols (with list comprehension)
        bike_cols = [col for col in grid if col.startswith("bike")]
        #apply minimum function to those columns and save the value to min column. Repeat for others.
        grid["min_t_bike"] = grid[bike_cols].apply(min, axis=1)
        
        car_cols = [col for col in grid if col.startswith("car")]
        grid["min_t_car"] = grid[car_cols].apply(min, axis=1)
        
        pt_cols = [col for col in grid if col.startswith("pt")]
        grid["min_t_pt"] = grid[pt_cols].apply(min, axis=1)
        
    return grid


def BasemapScaleNarrow(ax):
        #add basemap with contextify
        cartodb_url = "https://a.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}.png" 

        ctx.add_basemap(ax, attribution="Source: Helsinki region travel time matrix by UH. Basemap: OSM light", 
                    url=cartodb_url)


        #add scalebar
        scalebar = ScaleBar(1.0, location=4)
        plt.gca().add_artist(scalebar)

        #add north arrow
        x, y, arrow_length = 0.9, 0.2, 0.115
        ax.annotate('N', xy=(x, y), xytext=(x, y-arrow_length),
                arrowprops=dict(facecolor='black', width=5, headwidth=15),
                ha='center', va='center', fontsize=20,
                xycoords=ax.transAxes)
        
    
    
def InteractiveMap(geodata, column_name, transport_method, bins):
    """
    Creates an interactive map of the column that you want to visualise using folium. Takes geodataframe, 
    the column name, transport method as a string and the bins for classification (list of numbers that are 
    the upper limit of each class) as parameters. 
    """
    #add a basemap
    m = folium.Map(location=[60.25, 24.8], tiles = 'cartodbpositron', zoom_start=10, control_scale=True,
                           attribution = "Data: Helsinki Travel Time Matrix")

    #add the choropleth
    folium.Choropleth(
    geo_data=geodata,
    name="Travel times" + transport_method,
    data=geodata,
    columns=["YKR_ID", column_name],
    key_on="feature.properties.YKR_ID",
    bins = bins,
    fill_color="RdYlBu",
    fill_opacity=0.7,
    line_opacity=0.2,
    line_color="white",
    line_weight=0,
    highlight=True,
    legend_name="Travel times by " + transport_method + ", in minutes",
    ).add_to(m)

    #add tooltips (info when hovering over) as geoJson
    folium.GeoJson(geodata, name="travel time", smooth_factor=2,
    style_function=lambda x: {'weight':0.01,'color':'#807e7e', 'fillOpacity':0},
    highlight_function=lambda x: {'weight':1.5, 'color':'black'},
    tooltip=folium.GeoJsonTooltip(fields=["YKR_ID", column_name],labels=True, sticky=False)).add_to(m)

            
    #display layer control
    folium.LayerControl().add_to(m)

    #save and return the map
    outfp= "outputs/traveltimes" + transport_method + ".html"
    m.save(outfp)
    display(m)

    return m
        

        
def StaticMap(geodata, classified_column, transport_method):
    
    #change crs to add basemap later
    geodata = geodata.to_crs(epsg=3857)
            
    #plot
    fig, ax = plt.subplots(figsize=(10,10))

    #plot the travel times according to the classified field
    geodata.plot(ax= ax, column=classified_column, cmap="RdYlBu", legend=True)
    
    BasemapScaleNarrow(ax)
        
    #add title and show map
    ax.set_title("Travel times by " + transport_method, fontsize=24)
    fig.show()

    #save and return fig
    output_fig = "outputs/traveltimes" + transport_method + ".png"
    plt.savefig(output_fig)
    return output_fig
        
def MultipleMaps(geodata, transport_method, ncols, nrows):
    """
    This function visualises travel times with chosen transportation method to different cells in YKR_grid.
    The function produces a map or a collage of maps (subplots) depending on how many YKR cells have been
    chosen with FileFinder function. First parameter is a geodataframe and second is transport. Third and fourth
    input relate to how you want to arrange your subplots: number of rows and columns (len(target_cols) can be
    added to function to see how many subplots are you expecting).
    """
    
    #change crs to add basemap later
    geodata = geodata.to_crs(epsg=3857)
    
    if(transport_method == "bike"):
        target_cols = [col for col in geodata if col.startswith("bike")]
    elif(transport_method == "car"):
        target_cols = [col for col in geodata if col.startswith("car")]
    elif(transport_method == "public transport"):
        target_cols = [col for col in geodata if col.startswith("pt")]
    else:
        print("Transport_method should be bike, car or public transport as a string")

    #initialise the plot
    fig, axes = plt.subplots(ncols= ncols, nrows= nrows, figsize=(15,20))
    
    #flatten the axis to be one dimensional array (ease of plotting with iteration)
    axes = axes.flatten()
    
    for i, col in enumerate(target_cols):
        #plot the travel times according to the classified field
        geodata.plot(ax= axes[i], column=col, cmap="RdYlBu", vmax= 60, legend=True) 
            
        BasemapScaleNarrow(axes[i])
        
    #add title and show map
    fig.suptitle("Travel times comparison by " + transport_method, fontsize=24)
    #plt.tight_layout()
    fig.show()

    #save and return figure
    output_fig = "outputs/traveltimes_comparison_" + transport_method + ".png"
    plt.savefig(output_fig)
    return output_fig
        
    
    
    
def Visualiser(geodata, transport_method, interactive=None, classified=None): 
    """
    This function is meant for visualising the minimum travel time to multiple destinations with 
    a certain transportation method (any of the destiantions).The first argument is a geodataframe 
    containing travel times. Second argument is a transportation method (bike, public transport or car) 
    which you want to visualise. The third agrument is optional and can be added to obtain interactive 
    map as a result. If you want to visualise travel times to a single destination, use multiple maps 
    function.
    """
            
    #make the column name which should be visualised according to user input
    if(transport_method == "bike"):
        column_name = "min_t_bike"
        
    elif(transport_method == "public transport"):
        column_name = "min_t_pt"
        
    elif(transport_method == "car"):
        column_name = "min_t_car"
        
    else:
        print("Transport method should be one of the following: bike, public transport or car. Please insert a string")
            
    
    #define class breaks to array seen below (upper limits), apply this classification to pt and car travel times
    bins = [0,5,10,15,20,25,30,40,50,60]
    classifier = mapclassify.UserDefined.make(bins)
    
    #make new columns with class values
    geodata["classified"] = geodata[[column_name]].apply(classifier)
      
        
    #produce an interactive folium map if the optional parameter is passed    
    if(interactive == "yes"):
        
        InteractiveMap(geodata, column_name, transport_method, bins)
    
    #produce a classified static map
    elif(classified == "yes"):
        StaticMap(geodata, geodata["classified"], transport_method)
    
    #produce a static map if interactive parameter is not present
    else:
    
        StaticMap(geodata, column_name, transport_method)



def Comparer(geodata, transport_list, interactive=None):
    """
    Takes geodataframe and list of two transport methods. This function will calculate the time difference between the transport methods from each cell to the destination points and visualise the difference in accessibility with a static map or interactive map if interactive="yes" is passed as an optional argument. It always substracts the second travel method from the first (eg. ["public transport", "bike"] will show positive values where bike is faster and negative where public transit is faster).
    """
    
    #check what is the first item in user given list and assign the right column to column 1
    if(transport_list[0] == "bike"):
        column1 = geodata["min_t_bike"]
    
    elif(transport_list[0] == "car"):
        column1 = geodata["min_t_car"]
        
    elif(transport_list[0] == "public transport"):
        column1 = geodata["min_t_pt"]
        
    #print this if the value doesn't match any of the above
    else:
        print("Acceptable values are bike, car and public transport. Please use quotation marks.")
        
        
    #check what is the second item in user given list and assign the right column to column 2
    if(transport_list[1] == "bike"):
        column2 = geodata["min_t_bike"]
        
    elif(transport_list[1] == "car"):
        column2 = geodata["min_t_car"]
        
    elif(transport_list[1] == "public transport"):
        column2 = geodata["min_t_pt"]
        
    else:
        print("Acceptable values are bike, car and public transport. Please use quotation marks.")
        
    
    #calculate the difference between the column values 
    geodata["difference"] = column1 - column2
    
    #define upper limits for classifier values
    bins = [-30,-20,-10,-5,0,5,10,20,30]
    #apply the classifier on the difference column
    classifier = mapclassify.UserDefined.make(bins)
    #make new columns with class values
    geodata["classified"] = geodata[["difference"]].apply(classifier)
        
    #produce interative map if user requested it
    if(interactive == "yes"):
        
        InteractiveMap(geodata, geodata["difference"], "comparison", bins)
    
    #otherwise produce a regular map
    else: 
        StaticMap(geodata, geodata["classified"], "comparison")