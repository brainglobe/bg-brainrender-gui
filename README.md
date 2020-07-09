# bg-brainrender-gui
A GUI built on brainrender: visualise brain regions, neurons and labelled cells. 

The goal is to build a **nice** GUI (using pyside2) around brainrender.

Design: 
  - right sidebar: buttons to do thinks like `add brain regions`
        these buttons, when clicked, should open a new window with the widget for the specific function (e.g. an input for the brain regions to add, colors, alpha etc...)
  - brainrender widget: most of the window should be dedicated to the brainrender window for visualisation and interaction
  - right sidebar: an overview of what's currently rendered in the scene with an option to toggle visibility on/off
  
  
To do:
 - [ ] general UI
 - [ ] brainrender widget
 - [ ] left sidebar buttons
      - [ ] add_brain_regions functionality
      - [ ] add cells from file functionality
  - [ ] right sidebar
       - [ ] rendered item list
       - [ ] visibility toggle functionality
