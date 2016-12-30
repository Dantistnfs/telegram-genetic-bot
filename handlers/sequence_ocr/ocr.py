try:
	import Image
except ImportError:
	from PIL import Image

from . import pytesseract
import requests
from io import BytesIO
import time


def sequence_ocr_processing(image_url):
	image_downloaded = Image.open(BytesIO(requests.get(image_url).content))
	start = time.time()
	recognised_string = pytesseract.image_to_string(image_downloaded, lang='eng').replace("\n","").upper()
	end = time.time() - start
	message = 'Operation tooked: %f seconds. \n Here your sequence: \n %s' % (end, recognised_string)
	return message