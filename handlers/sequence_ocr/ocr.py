try:
	import Image
except ImportError:
	from PIL import Image

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
	edge_dog = mahotas.dog(numpy_picture)
	Image.fromarray(mahotas.dilate(edge_dog, np.ones((10,10))).astype('uint8')*255).save('image.png')
	"""
	sobel_image = mahotas.dog(numpy_picture).astype(np.uint8)
	Image.fromarray(sobel_image).save('image.png')
	"""
	download = time.time() - start
	recognised_string = pytesseract.image_to_string(image_for_recognition, lang='eng').replace("\n","").upper()
	end = time.time() - start - download
	return (download, end, recognised_string, image_for_recognition)


