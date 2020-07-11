# bg-brainrender-gui
A GUI built on brainrender: visualise brain regions, neurons and labelled cells. 

The goal is to build a **nice** GUI (using pyside2) around brainrender.

Design: 
  - right sidebar: buttons to do thinks like `add brain regions`
        these buttons, when clicked, should open a new window with the widget for the specific function (e.g. an input for the brain regions to add, colors, alpha etc...)
  - brainrender widget: most of the window should be dedicated to the brainrender window for visualisation and interaction
  - right sidebar: an overview of what's currently rendered in the scene with an option to toggle visibility on/off
  
  
To do:
 * [x] general UI
 * [x] brainrender widget
 * [x] left sidebar buttons
      * [x] add_brain_regions functionality
      * [x] add cells from file functionality
  * [x] right sidebar
       * [x] rendered item list
       * [x] visibility toggle functionality
  * [x] actors list: UI to show hidden/shown
  * [x] add structures tree widget like bgviewer
  
  * [ ] UI design improvements
  * [ ] more add X functionality??

  * [ ] widget to try different shading styles?
  * [ ] when adding actors to scene, options to edit appearence
         * color
         * alpha
         * wireframe

  * [ ] actors list: add icon to show what kind of data
  * [ ] actors list: single click -> actor edit, doble click toggle on/off
