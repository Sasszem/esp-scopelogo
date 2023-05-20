#!/bin/env python3
import pickle

import sys

images = []

for file in sys.argv[1:]:
    with open(file, "rb") as f:
        images.append(pickle.load(f))

index = 0
starts = []
sizes = []
data = []
for im in images:
    starts.append(index)
    sizes.append(len(im)//2)
    index += sizes[-1]
    data.extend(im)

def to_array(ar):
    return "{" + ", ".join(str(i) for i in ar) + "}"

with open('shape.c', 'w') as f:
    f.write(f"char data[] = {to_array(data)};\n")
    f.write(f"long int starts[] = {to_array(starts)};\n")
    f.write(f"long int sizes[] = {to_array(sizes)};\n")
    f.write(f"int count = {len(images)};\n")
