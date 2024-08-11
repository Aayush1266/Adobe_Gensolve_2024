import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.spatial import ConvexHull
from scipy.interpolate import splprep, splev

def extract_paths(np_data):
    paths = []
    unique_paths = np.unique(np_data[:, 0])
    for path_id in unique_paths:
        path_data = np_data[np_data[:, 0] == path_id]
        unique_segments = np.unique(path_data[:, 1])
        path_segments = []
        for segment_id in unique_segments:
            segment_data = path_data[path_data[:, 1] == segment_id][:, 2:]
            path_segments.append(segment_data)
        paths.append(path_segments)
    return paths

def plot_paths(paths_XYs, title="Path Plot"):
    fig, ax = plt.subplots(figsize=(8, 8))
    colours = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    for i, XYs in enumerate(paths_XYs):
        c = colours[i % len(colours)]
        for XY in XYs:
            ax.plot(XY[:, 0], XY[:, 1], c=c, linewidth=2)
    ax.set_aspect('equal')
    ax.set_title(title)
    plt.show()

def regularize_shapes(paths_XYs):
    regular_shapes = []
    for path in paths_XYs:
        regular_path = []
        for curve in path:
            if is_straight_line(curve):
                regular_path.append(regularize_line(curve))
            elif is_circle(curve):
                regular_path.append(regularize_circle(curve))
            elif is_rectangle(curve):
                regular_path.append(regularize_rectangle(curve))
            elif is_polygon(curve):
                regular_path.append(regularize_polygon(curve))
            else:
                regular_path.append(regularize_to_simpler_shape(curve))
        regular_shapes.append(regular_path)
    return regular_shapes

def is_straight_line(curve):
    if len(curve) < 2:
        return False
    x, y = curve[:, 0], curve[:, 1]
    line_fit = np.polyfit(x, y, 1)
    y_fit = np.polyval(line_fit, x)
    residuals = np.sum((y - y_fit) ** 2)
    return residuals < 1e-4

def is_circle(curve):
    if len(curve) < 3:
        return False
    center = np.mean(curve, axis=0)
    radii = np.linalg.norm(curve - center, axis=1)
    return np.std(radii) / np.mean(radii) < 0.1

def is_rectangle(curve):
    if len(curve) < 4:
        return False
    hull = ConvexHull(curve)
    return len(hull.vertices) == 4

def is_polygon(curve):
    if len(curve) < 5:
        return False
    hull = ConvexHull(curve)
    return len(hull.vertices) > 4

def regularize_line(curve):
    return np.array([curve[0], curve[-1]])

def regularize_circle(curve):
    def residuals(params, curve):
        cx, cy, r = params
        distances = np.sqrt((curve[:, 0] - cx) ** 2 + (curve[:, 1] - cy) ** 2)
        return distances - r
    
    center = np.mean(curve, axis=0)
    radius_guess = np.mean(np.linalg.norm(curve - center, axis=1))
    params_guess = [center[0], center[1], radius_guess]
    res = minimize(lambda params: np.sum(residuals(params, curve) ** 2), params_guess)
    cx, cy, r = res.x

    angles = np.linspace(0, 2 * np.pi, 100)
    x = cx + r * np.cos(angles)
    y = cy + r * np.sin(angles)
    return np.vstack((x, y)).T

def regularize_rectangle(curve):
    hull = ConvexHull(curve)
    vertices = curve[hull.vertices]
    return vertices

def regularize_polygon(curve):
    hull = ConvexHull(curve)
    vertices = curve[hull.vertices]
    return vertices

def regularize_to_simpler_shape(curve):
    tck, u = splprep([curve[:, 0], curve[:, 1]], s=0.5)
    x_smooth, y_smooth = splev(np.linspace(0, 1, 100), tck)
    smooth_curve = np.vstack((x_smooth, y_smooth)).T
    
    if is_straight_line(smooth_curve):
        return regularize_line(smooth_curve)
    elif is_circle(smooth_curve):
        return regularize_circle(smooth_curve)
    elif is_rectangle(smooth_curve):
        return regularize_rectangle(smooth_curve)
    elif is_polygon(smooth_curve):
        return regularize_polygon(smooth_curve)
    return smooth_curve


path_frag0 = 'frag0.csv'
data_frag0 = np.genfromtxt(path_frag0, delimiter=',')

paths_frag0 = extract_paths(data_frag0)
regularized_paths_frag0 = regularize_shapes(paths_frag0)
output_csv_path = 'regularized_frag0.csv'

plot_paths(regularized_paths_frag0, title="Regularized Paths - frag0.csv")
