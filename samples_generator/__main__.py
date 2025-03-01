"""
SVG to samples converter for scopelogo project
Usage:
pipenv run samples_generator <input_svg_path> [output_path] [--interpolation-factor FACTOR]

Generates samples for the ESP code (shape[] array data) from an SVG file.
Samples the SVG points based on interpolation_factor and converts the (filtered) list
to 8-bit numbers.
"""

from itertools import chain
import click
from read_image import read_image
import pickle as pck

@click.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.argument("output", type=click.Path(), default="shape.c")
@click.option("--interpolation-factor",
              help="Interpolation factor (how many points per unit distance)"
              "Should be ~500 or more. Less points means less resolution.",
              show_default=True,
              default=500
              )
@click.option("--mirror/--no-mirror", help="Mirror the image", show_default=True, default=False, type=bool)
@click.option("--export", help="Export resulting image using PIL into specified filename", show_default=True, type=str, default=None)
@click.option("--pickle", help="Save data into pickle file", type=str, default=None)
def main(input_path: str, output: str, interpolation_factor: int, mirror: bool, export: str, pickle: str):
    """Generate samples for the ESP firmware to draw from an SVG file"""
    points = read_image(input_path, interpolation_factor, False)

    if mirror:
        points = [point.conjugate() for point in points]

    new_points = [(p+0.5+0.5j) * 255 for p in points]
    pairs = list(map(lambda x: (int(x.real), int(x.imag)), new_points))

    # remove double occurances
    new_pairs: list[tuple[int, int]] = []
    for point in pairs:
        if new_pairs and new_pairs[-1] == point:
            continue
        new_pairs.append(point)
    pairs = new_pairs

    data = list(chain(*pairs))
    if export:
        from write_image import export_image
        export_image(data, export)
    if pickle:
        with open(pickle, "wb") as f:
            pck.dump(data, f)
    else:
        with open(output, "w", encoding="utf-8") as outfile:
            outfile.write(
                "char shape[] = {" + ", ".join(str(point) for point in data) + "};\n")
            outfile.write(f"int length = {len(data)//2};\n")
    print(f"Samples count: {len(data)//2}")

if __name__ == "__main__":  # how would this ever fail?
    main()  # pylint: disable=no-value-for-parameter
