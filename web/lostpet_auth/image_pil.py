from image_utils import ImageText
from PIL import *

# image_file = str("%simages/%s" % (settings.BASE_DIR + settings.STATIC_URL, client.pet_image))
image = Image.new('RGB', (714, 374), (85, 113, 127))
pet_image = Image.open("lost_dog.jpg")
ratio = 340.0 / pet_image.size[1]
width = int(pet_image.size[0] * ratio)

pet_image = pet_image.resize((width, 340), Image.ANTIALIAS)
pet_image.save("lost_pet_new.png")
image.paste(pet_image, ((image.size[0] - pet_image.size[0])/2, 34))
image.save("sample.png")

img = ImageText(str("sample.png"), background=(255, 0, 0, 255))
img.write_text_box((0, 0), "MISSING PET ALERT - %s, %s" % ("Chicago", "IL"), box_width=img.getWidth(), font_filename=str("IMPACT.TTF"), font_size=35, color=(250, 250, 250), place='center')
img.save("sample.png")
