from PIL import Image, ImageTk
import tkinter as tk
import argparse

#Abgabe von Valentino Giorgio Pino, Matr.Nr.: 2225371

# Die Funktionen wurden mithilfe von den Bibliotheken von Python, Pillow, tkinter geschrieben, außerdem wurde das Wissen
# aus der Vorlesung/Übung angewendet und schlussendlich für einige Hilfestellungen ChatGPT

# Parser für Batch-Kommandozeilenbetrieb
# https://docs.python.org/3/library/argparse.html
parser = argparse.ArgumentParser(description='Ein Tool zum Bearbeiten von Bildern')
parser.add_argument('--threshold', type=int,
                    help='Threshold des Bildes setzen. Füge hierfür einen Integer-Wert ein.')
parser.add_argument('--brightness', type=float,
                    help='Brightness des Bildes setzen. Füge hierfür einen float-Wert ein.')
parser.add_argument('--contrast', type=float,
                    help='Contrast des Bildes setzen. Füge hierfür einen float-Wert ein.')
parser.add_argument('--blur', type=int, help='Blurradius des Bildes setzen')
parser.add_argument('--sharpen', type=int, help='Das Bild sharpen')
parser.add_argument('--saturation', type=float, help='Das Bild sättigen')
parser.add_argument('--channelchange', type=str,
                    help='Vertauschen der Farbkanäle jeweiligen Bildes. Füge hierfür einen String-Wert ein.')
parser.add_argument('--colormode', type=str,
                    help='Ändern des Colormodes des Bildes. Zu Beachten: Manche Funktionen konvertieren das Bild zu einem RGB Bild!. Füge hierfür einen String-Wert ein')
parser.add_argument('image', type=str, help='Das Bild hinzufügen')
args = parser.parse_args()

# Mainwindow
root = tk.Tk()

# Hier wird das Bild importiert
i = Image.open(args.image)
result = i.copy()


# Threshold Filter
def threshold(tresh):
    global result
    img = result.copy()

    for x in range(img.width):
        for y in range(img.height):
            r, g, b = img.getpixel((x, y))
            value = (r + g + b) / 3
            if value < tresh:
                new_tresh = 0
            else:
                new_tresh = 255
            img.putpixel((x, y), (new_tresh, new_tresh, new_tresh))
    result = img
    return img


# Brightness Filter
def brightness(factor):
    global result
    img = result.copy()

    for x in range(img.width):
        for y in range(img.height):
            pixel = img.getpixel((x, y))
            new_pixel = tuple(int(value * factor) for value in pixel)
            img.putpixel((x, y), new_pixel)
    return img


# Contrast Filter
def contrast(contrast):
    global result
    img = result.copy()
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            pixel = tuple([int(contrast * (c - 128) + 128) for c in img.getpixel((x, y))])
            img.putpixel((x, y), pixel)
    return img


# Blur Filter
def blur(blur):
    global result
    img = result.copy()
    width, height = img.size
    for x in range(width):
        for y in range(height):
            r, g, b = 0, 0, 0
            count = 0
            for dx in range(-blur, blur + 1):
                for dy in range(-blur, blur + 1):
                    nx = x + dx
                    ny = y + dy
                    if 0 <= nx < width and 0 <= ny < height:
                        pixel = img.getpixel((nx, ny))
                        r += pixel[0]
                        g += pixel[1]
                        b += pixel[2]
                        count += 1
            img.putpixel((x, y), (r // count, g // count, b // count))
    return img


# Sharpen Filter
def sharpen(sharp):
    global result
    img = result.copy()
    kernel = [[0, -1, 0],
              [-1, 5 + sharp, -1],
              [0, -1, 0]]
    w, h = img.size
    div = sum(kernel[0]) + sum(kernel[1]) + sum(kernel[2])
    for x in range(w):
        for y in range(h):
            new_r, new_g, new_b = 0, 0, 0
            for l in range(3):
                for j in range(3):
                    nx = x - 1 + l
                    ny = y - 1 + j
                    if 0 <= nx < w and 0 <= ny < h:
                        r, g, b = img.getpixel((nx, ny))
                        weight = kernel[l][j]
                        new_r += r * weight
                        new_g += g * weight
                        new_b += b * weight
            new_r //= div
            new_g //= div
            new_b //= div
            img.putpixel((x, y), (new_r, new_g, new_b))
    return img


# Extra Filter für Pflichtwahlbereich: Saturation
def saturation(saturation_factor):
    global result
    img = result.copy()
    # Neues Bild erstellen, um das Ergebnis zu speichern
    filtered_image = Image.new("RGB", img.size)

    # Durch jedes Pixel des Bildes iterieren
    for x in range(img.width):
        for y in range(img.height):
            # Pixelwert abrufen
            r, g, b = img.getpixel((x, y))

            # Konvertierung in Graustufen
            gray_value = int(0.2989 * r + 0.5870 * g + 0.1140 * b)

            # Sättigung anpassen
            new_r = int((1 - saturation_factor) * r + saturation_factor * gray_value)
            new_g = int((1 - saturation_factor) * g + saturation_factor * gray_value)
            new_b = int((1 - saturation_factor) * b + saturation_factor * gray_value)

            # Pixelwert im neuen Bild setzen
            filtered_image.putpixel((x, y), (new_r, new_g, new_b))

    return filtered_image


# Farbkanalwechsel
def channelchange(change):
    global result
    img = result.copy()
    img.convert("RGB")
    R, G, B = img.split()
    x = (R, G, B)
    change = change.lower()
    if change == "rgb":
        x = x
    elif change == "rbg":
        x = (x[0], x[2], x[1])
    elif change == "grb":
        x = (x[1], x[0], x[2])
    elif change == "gbr":
        x = (x[1], x[2], x[0])
    elif change == "brg":
        x = (x[2], x[0], x[1])
    elif change == "bgr":
        x = (x[2], x[1], x[0])
    else:
        raise ValueError('Ungültiger Reihenfolge-String: {}'.format(change))
    return Image.merge("RGB", x)


# Farbmoduswechsel
def colormode(scheme):
    global result
    img = result.copy()
    if scheme.lower() == 'rgb':
        converted_image = img.convert('RGB')
    elif scheme.lower() == 'l':
        converted_image = img.convert('L')
    elif scheme.lower() == '1':
        converted_image = img.convert('1')
    elif scheme.lower() == 'rgba':
        converted_image = img.convert('RGBA')
    elif scheme.lower() == 'la':
        converted_image = img.convert('LA')
    elif scheme.lower() == 'p':
        converted_image = img.convert('P')
    else:
        raise ValueError('Ungültiger Colormode: {}'.format(scheme))
    return converted_image


# Überprüfung der Eingabe Parameter und die darauffolgende Auführung der Befehle
if args.threshold is not None:
    result = threshold(args.threshold)
if args.brightness is not None:
    result = brightness(args.brightness)
if args.contrast is not None:
    result = contrast(args.contrast)
if args.blur is not None:
    result = blur(args.blur)
if args.sharpen is not None:
    result = sharpen(args.sharpen)
if args.channelchange is not None:
    result = channelchange(args.channelchange)
if args.colormode is not None:
    result = colormode(args.colormode)
if args.saturation is not None:
    result = saturation(args.saturation)

# Displayen des Bildes
picture = ImageTk.PhotoImage(result)
label = tk.Label(image=picture)
label.pack()
root.mainloop()
