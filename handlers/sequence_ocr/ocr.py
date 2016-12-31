try:
	import Image
except ImportError:
	from PIL import Image, ImageDraw, ImageFont

from . import pytesseract
import requests
from io import BytesIO, StringIO
import time
import mahotas
import numpy as np
import png
import logging
logger = logging.getLogger(__name__)
from pylab import imshow, gray, show, subplot



def downscale_image(im, max_dim=2048):
    """Shrink im until its longest dimension is <= max_dim.
    Returns new_image, scale (where scale <= 1).
    """
    a, b = im.size
    if max(a, b) <= max_dim:
        return 1.0, im

    scale = 1.0 * max_dim / max(a, b)
    new_im = im.resize((int(a * scale), int(b * scale)), Image.ANTIALIAS)
    return scale, new_im


def sequence_ocr_processing(image_url):
	numpy_picture = np.array(Image.open(BytesIO(requests.get(image_url).content)).convert('L')).astype(np.uint8)
	start = time.time()
	#threshold = mahotas.rc(numpy_picture)
	image_processed = Image.fromarray(numpy_picture)
	edge_dog = mahotas.dog(numpy_picture,sigma1=4,multiplier=1.5)
	first_dilation = mahotas.dilate(edge_dog, np.ones((15,30)))
	#second_dilation = mahotas.dilate(first_dilation, np.ones((15,30)))
	labeled, nr_objects = mahotas.label(first_dilation)
	bboxes = mahotas.labeled.bbox(labeled)
	draw = ImageDraw.Draw(image_processed)
	width, height = image_processed.size
	font = ImageFont.truetype("arial.ttf", int(height/15))
	for index in range(1,len(bboxes)):
		box_coordinates = bboxes[index]
		draw.rectangle([box_coordinates[2],box_coordinates[0],box_coordinates[3],box_coordinates[1]])
		draw.text([(box_coordinates[2]+5),box_coordinates[0]], str(index), font = font)
	image_processed.save('image.png')
	download = 0
	end = time.time() - start
	recognised_string = "123"
	return (download, end, recognised_string, image_processed)


def ocr_process(image, box_coordinates):
	start = time.time()
	recognised_string = pytesseract.image_to_string(image_for_recognition, lang='eng').replace("\n","").upper()
	end = time.time() - start
	return