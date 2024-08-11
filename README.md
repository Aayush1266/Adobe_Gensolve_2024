## Path Regularization and Visualization:
This repository contains code to process and regularize 2D paths from input data. The primary purpose of the project is to extract paths from a CSV file, identify basic geometric shapes (such as lines, circles, rectangles, and polygons) within those paths, and regularize them into their simplest form. The resulting paths are then plotted for visualization.

### Features:
* Path Extraction: Extracts paths and segments from a CSV file containing path data.
* Shape Regularization: Identifies and regularizes basic geometric shapes, such as:
  * Straight Lines
  * Circles
  * Rectangles
  * Any Polygons
* Simplification: If the shape does not match a predefined category, the curve is smoothed and then rechecked for simpler shapes.
* Visualization: Plots the regularized paths for easy visualization.

### Functions: 
* extract_paths(np_data): Extracts paths and segments from the input data.
* plot_paths(paths_XYs, title): Plots the regularized paths.
* regularize_shapes(paths_XYs): Regularizes the shapes within each path.
* is_straight_line(curve): Checks if a curve is a straight line.
* is_circle(curve): Checks if a curve forms a circle.
* is_rectangle(curve): Checks if a curve forms a rectangle.
* is_polygon(curve): Checks if a curve forms a polygon.
* regularize_line(curve): Regularizes a line.
* regularize_circle(curve): Regularizes a circle.
* regularize_rectangle(curve): Regularizes a rectangle.
* regularize_polygon(curve): Regularizes a polygon.
* regularize_to_simpler_shape(curve): Smooths and rechecks the curve for simpler shapes.

### Modules
* Numpy
* MatplotLib
* Scipy
