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


@click.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.argument("output", type=click.Path(), default="shape.c")
@click.option("--interpolation-factor",
              help="Interpolation factor (how many points per unit distance) Should be ~500 or more. Less points means less resolution.",
              show_default=True,
              default=500
              )
def main(input_path: str, output: str, interpolation_factor: int):
    """Generate samples for the ESP firmware to draw from an SVG file"""
    points = read_image(input_path, interpolation_factor, False)
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
    with open(output, "w", encoding="utf-8") as outfile:
        outfile.write(
            "int shape[] = {" + ", ".join(str(point) for point in data) + "};\n")
        outfile.write("int length = sizeof(shape)/2;\n");

if __name__ == "__main__":  # how would this ever fail?
    main() # pylint: disable=no-value-for-parameter
