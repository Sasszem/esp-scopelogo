"""
Read SVG image and generate points

Scales & translates points to the 1.0*(-1-1j; 1+1j) bounding box.

Part of my esp-scopelogo generator script. Should not be used as-is.
"""


import svg.path
from lxml import etree as ET


def _interpolate(elem, invstep, trans, scale):
    """Interpolate SVG path element so on average we have ~invstep points per unit distance"""
    dist = abs(elem.start - elem.end) * scale
    steps = max(1, int(dist * invstep))
    return [scale * (elem.point(i/steps)+trans) for i in range(steps)]


def _get_paths(filepath):
    """Read and parse all paths in file"""
    tree = ET.parse(filepath) # pylint: disable=c-extension-no-member
    root = tree.getroot()

    return [svg.path.parse_path(node.get("d")) for node in tree.findall(".//path", root.nsmap)]


def _find_bounding_box(paths):
    """Find bounding box of SVG paths"""
    minx, miny, maxx, maxy = 10**10, 10**10, 0, 0
    for path in paths:
        for elem in path:
            minx = min(minx, elem.start.real, elem.end.real)
            miny = min(miny, elem.start.imag, elem.end.imag)
            maxx = max(maxx, elem.start.real, elem.end.real)
            maxy = max(maxy, elem.start.imag, elem.end.imag)
    return minx, miny, maxx, maxy


def _center(path):
    num_points = 0
    sum_of_coords = 0
    for elem in path:
        for i in range(20):
            sum_of_coords += elem.point(i/20)
            num_points += 1
    return sum_of_coords/num_points


def _parse_image(filepath, interpolation_factor, progress):
    """Read image, parse & interpolate points"""
    if progress:
        print("Parsing image")

    paths = _get_paths(filepath)
    paths = sorted(paths, key=lambda x: 5*_center(x).imag + _center(x).real)
    image_points = []

    minx, miny, maxx, maxy = _find_bounding_box(paths)
    trans = -complex(maxx+minx, maxy+miny) / 2
    scale = 1.0/max(maxx-minx, maxy-miny)

    for path in paths:
        for elem in path:
            if isinstance(elem, svg.path.Move):
                continue
            image_points.extend(_interpolate(
                elem, interpolation_factor, trans, scale))
    return image_points


def read_image(filepath, interpolation_factor, progress=False):
    """Read SVG and return list of complex numbers"""
    return _parse_image(filepath, interpolation_factor, progress)
