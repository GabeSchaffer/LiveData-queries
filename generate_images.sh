#!/bin/bash

# generate images using graphviz dot

# definitions are in the ./dot folder
# output images to the ./images folder
for f in ./dot/*.dot; do
    dot -Tpng $f -o ./images/$(basename $f .dot).png
done
