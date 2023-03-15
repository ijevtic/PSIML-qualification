
# Olympic Rings
## Description

You are given the colored image with different geometrical shapes such as circle, square etc. Some of these shapes form Olympic logos. You are expected to find valid logos in the image.

    Olympic logo is said to be valid if and only if it has five circles (of potentially different radii) and following circles intersect each other: blue and yellow, black and yellow, green and black & green and red.
    Olympic logo can be valid even if it's contained into another shape, but no additional intersections are allowed.

## Task 1: Count colors

Count number of pixels for each of five Olympic colors.

### Additional notes:

    All images are in PNG format.
    All images are in 768x768 resolution.
    Background is always white.
    If you find any other pattern in the public set, it's reasonable to expect it holds in the private set as well.

## Task 2: Find logos

Find valid Olympic logos on the image & print colors and coordinates of their centers.
## Input

Your program should read a single line through standard input. This line contains path to the PNG image.
## Output

First five lines contain number of pixels for each of five Olympic colors. Next line of the standard output contains number of valid Olympic logos. For each valid logo, output color and location of the center. Order of colors can't be arbitrary. See public examples for the exact order and color symbols. Order of logos isn't important so you can print them in any order you'd like.
Colors

Image can contain different colors. If we use RGB chromatic scheme as a reference, we define Olympic colors to be red (255, 0, 0), blue (0, 0, 255), green (0, 255, 0), yellow (255, 255, 0) and black (0, 0, 0). So, for example, color (0, 0, 214) isn't considered to be blue.

As said before, background is always white (255, 255, 255).
## Scoring

Each test case can bring a maximum of 150 points. Correctly counted pixels in the first task brings 30 points per test case. Remaining 120 points are given if both tasks are correctly solved.

Center of each circle in the task 2 can differ by at most 1 pixel from the solution.
## Limitations

The time limit for task execution is 5 seconds per input image.

Allowed packages are numpy, PIL and all other packages from the standard Python library.
