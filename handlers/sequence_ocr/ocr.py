try:
	import Image
except ImportError:
	from PIL import Image, ImageDraw

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
	start = time.time()
	numpy_picture = np.array(Image.open(BytesIO(requests.get(image_url).content)).convert('L')).astype(np.uint8)
	#threshold = mahotas.rc(numpy_picture)
	image_for_recognition = Image.fromarray(numpy_picture)
	edge_dog = mahotas.dog(numpy_picture,sigma1=4,multiplier=1.5)
	first_dilation = mahotas.dilate(edge_dog, np.ones((15,30)))
	second_dilation = mahotas.dilate(first_dilation, np.ones((15,30)))
	labeled, nr_objects = mahotas.label(second_dilation)
	bboxes = mahotas.labeled.bbox(labeled)
	image = Image.fromarray(labeled.astype('uint8')*255)
	draw = ImageDraw.Draw(image_for_recognition)
	for box in bboxes:
		draw.rectangle([box[2],box[0],box[3],box[1]])
	image_for_recognition.save('image.png')
	#imshow(labeled, interpolation='nearest')
	#show()
	"""
	sobel_image = mahotas.dog(numpy_picture).astype(np.uint8)
	Image.fromarray(sobel_image).save('image.png')
	"""
	download = time.time() - start
	recognised_string = pytesseract.image_to_string(image_for_recognition, lang='eng').replace("\n","").upper()
	end = time.time() - start - download
	return (download, end, recognised_string, image_for_recognition)


