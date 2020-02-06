# Final Assignment

* Package that needs to be installed in notebooks: Matplotlib Scalebar. Run "pip install matplotlib-scalebar" in terminal

## Topic: 
[AccessViz](https://automating-gis-processes.github.io/site/lessons/FA/final-assignment.html#accessviz): Data handling and visualising tool for Travel time Matrix 2018

Case study: Biking as means of transportation for a uni student 

### Input data: 
- Helsinki Travel Time Matrix 2018 https://blogs.helsinki.fi/accessibility/helsinki-region-travel-time-matrix-2018/, 
- YKR grid 2018 (can be downloaded from the above address, make sure to use all 7 files that the shapefile consists of), 
- OSMnx network data for shortest path analysis (fetches data from Open Street Map, Helsinki Area)

* For your own analysis, download the Travel time and YKR grid data from the above address. Create a folder called "data" under the same folder where you are working. Place the YKR grid in the "data" folder and move the entire folder called "HelsinkiTravelTimeMatrix2018" under the data folder as well. Do not alter the files or filepaths inside HelsinkiTravelTimeMatrix2018.

* More info of the input data in [here](Final_notebook.ipynb)

* Link to limited [example data](data) that I used (uni campuses) 

### Analysis steps: 
1. Identify the YKR id of the area of interest with CellChecker function
2. Use FileFinder to fetch the right files for your AOI
3. Use the filepaths from  FileFinder to join them with YKR grid with TableJoiner
4. Visualise the created geodatabase with static (classifed and unclassified) or interactive maps with the chosen transport method
5. Visualise the comparison of two chosen transport methods on a static map
6. Create a collage of travel time maps for each destination separately
7. Visualise fastest routes by car from address A to address B in Helsinki

* Check out the [Final_notebook.ipynb](Final_notebook.ipynb) to see a walk through of the analysis steps with an example



### Results:
- A toolbox of functions made for visualising the travel time  matrix data
- Cool maps and visulisations made by the user 
- Tutorial demonstrating how to use the tools 
- A case study made with the tools created that proves that bike is a very useful and fast means of transportation for a uni student not to mention its health benefits and being student-budget friendly

- Here you can see some [visualisations](outputs) created  with this tool 

### Links to files:
- [My final script](Final_assignment.py)
- [Tutorial demonstrating the tools and documentation with case study](Final_notebook.ipynb) This file is bigger than the recommended size for notebooks, let me know if there is any trouble opening/ running the code!
- [Flow chart of the process](Flow_chart.png)


Scratch notebooks for trying stuff: 
- [notebook1](Final.ipynb)
- [notebook2](OSMNX.ipynb)
- [Discarded pieces](discarded_pieces.ipynb)
