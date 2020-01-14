# Final Assignment

### Status

Once you are finished with the final assignment, edit this readme and add "x" to the correct box:

* [ ] Submitted

* [x] I'm still working on my final assignment. 

### Instructions

Read the final assignment instructions from the course webpages [https://autogis.github.io](https://automating-gis-processes.github.io/site/lessons/FA/final-assignment.html). Remember to write readable code, and to provide adequate documentation using inline comments and markdown. Organize all your code(s) / notebook(s) into this repository and **add links to all relevant files to this `README.md`file**. In sum, anyone who downloads this repository should be able to **read your code and documentation** and understand what is going on, and **run your code** in order to reproduce the same results :) 

**Modify this readme so that anyone reading it gets a quick overview of your final work topic, and finds all the necessary input data, code and results.** Add short descriptions, and provide links to relevant files under the topics below (modify the titles according to your topic). You can delete this intro text if you like. 

*Note: If your code requires some python packages not found in the csc notebooks environment, please mention them also in this readme and provide installation instrutions.*

*Note: Don't upload large files into GitHub! If you are using large input files, provide downloading instructions and perhaps a small sample of the data in this repository for demonstrating your workflow.*

## Topic: 
AccessViz: Data handling and visualising tool for Travel time Matrix 2018
Case study: Biking as means of transportation for a uni student 

### Input data: 
- Helsinki Travel Time Matrix 2018 https://blogs.helsinki.fi/accessibility/helsinki-region-travel-time-matrix-2018/, 
- YKR grid 2018 (can be downloaded from the above address, make sure to use all 7 files that the shapefile consists of), 
- OSMnx network data for shortest path analysis (fetches data from Open Street Map, Helsinki Area)

* For your own analysis, download the Travel time and YKR grid data from the above address. Create a folder called "data" under the same folder where you are working. Place the YKR grid in the "data" folder and move the entire folder called "HelsinkiTravelTimeMatrix2018" under the data folder as well. Do not alter the files or filepaths inside HelsinkiTravelTimeMatrix2018.

* More info of the input data in https://pb-elisha-the-witty-d7368195cc.rahtiapp.fi/lab/tree/autogis/exercises/final-assignment-sonjakoivisto/Final_notebook.ipynb

* Link to limited example data that I used (uni campuses) https://pb-elisha-the-witty-d7368195cc.rahtiapp.fi/lab/tree/autogis/exercises/final-assignment-sonjakoivisto/data 

### Analysis steps: 
1. Identify the YKR id of the area of interest with CellChecker function
2. Use FileFinder to fetch the right files for your AOI
3. Use the filepaths from  FileFinder to join them with YKR grid with TableJoiner
4. Visualise the created geodatabase with static (classifed and unclassified) or interactive maps with the chosen transport method
5. Visualise the comparison of two chosen transport methods on a static map
6. Create a collage of travel time maps for each destination separately
7. Visualise fastest routes by car from address A to address B in Helsinki

* Check out the Final_notebook.ipynb to see a walk through of the analysis steps with an example
https://pb-elisha-the-witty-d7368195cc.rahtiapp.fi/lab/tree/autogis/exercises/final-assignment-sonjakoivisto/Final_notebook.ipynb


### Results:
- A toolbox of functions made for visualising the travel time  matrix data
- Cool maps and visulisations made by the user 
- Tutorial demonstrating how to use the tools 
- A case study made with the tools created that proves that bike is a very useful and fast means of transportation for a uni student not to mention its health benefits and being student-budget friendly

- Here you can see some visualisations created  with this tool https://pb-elisha-the-witty-d7368195cc.rahtiapp.fi/lab/tree/autogis/exercises/final-assignment-sonjakoivisto/outputs

### Links to files:
- My final script: https://pb-elisha-the-witty-d7368195cc.rahtiapp.fi/lab/tree/autogis/exercises/final-assignment-sonjakoivisto/Final_assignment.py
- Tutorial demonstrating the tools and documentation with case study: https://pb-elisha-the-witty-d7368195cc.rahtiapp.fi/lab/tree/autogis/exercises/final-assignment-sonjakoivisto/Final_notebook.ipynb
- Flow chart of the process: https://pb-elisha-the-witty-d7368195cc.rahtiapp.fi/lab/tree/autogis/exercises/final-assignment-sonjakoivisto/Flow%20chart.png


- Scratch notebooks for trying stuff: https://pb-elisha-the-witty-d7368195cc.rahtiapp.fi/lab/tree/autogis/exercises/final-assignment-sonjakoivisto/Final.ipynb, https://pb-elisha-the-witty-d7368195cc.rahtiapp.fi/lab/tree/autogis/exercises/final-assignment-sonjakoivisto/OSMNX.ipynb
- Discarded pieces: https://pb-elisha-the-witty-d7368195cc.rahtiapp.fi/lab/tree/autogis/exercises/final-assignment-sonjakoivisto/discarded%20_pieces.ipynb