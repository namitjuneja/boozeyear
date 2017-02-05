from PIL import ImageEnhance, Image

image = Image.open(open("test.jpg", 'rb'))

image.show()

enhancer = ImageEnhance.Sharpness(image)

for i in range(8):
    factor = i / 4.0
    enhancer.enhance(factor).show("Sharpness %f" % factor)