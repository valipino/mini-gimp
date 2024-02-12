# mini-gimp - Image Processing Tool

This self-created project, developed as part of the "Computer Graphics and Image Processing" lecture, presents an image processing tool built using the Python libraries Pillow (PIL) and Tkinter. The fundamental concepts and functions acquired during the lecture and exercises have been applied in this tool.

## Features

The tool supports various image processing operations that can be entered through the command line. Implementation utilizes the argparse library to parse input parameters and perform corresponding edits. The following image processing functions are available:

- **Threshold:** Sets a threshold value for the image.
- **Brightness:** Adjusts the brightness of the image.
- **Contrast:** Adjusts the contrast of the image.
- **Blur:** Applies a blur filter to the image.
- **Sharpen:** Sharpens the image using a filter kernel.
- **Saturation:** Changes the saturation of the image.
- **Channelchange:** Swaps the color channels of the image based on a specified order.
- **Colormode:** Changes the color mode of the image.

The tool allows the combination of multiple editing steps in a single execution by specifying the corresponding parameters via the command line.

## Implementation

The implementation of image processing functions involves loops and pixel manipulations in the image data. The user interface is provided by the Tkinter library, displaying the edited image directly in the GUI.

The use of the argparse library enables flexible and user-friendly control of the image processing tool via the command line. The project showcases the application of knowledge in image processing and programming, offering the ability to easily combine and apply basic image editing functions.
