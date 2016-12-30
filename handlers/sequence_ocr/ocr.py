try:
	import Image
except ImportError:
	from PIL import Image

from . import pytesseract
import requests
from io import BytesIO
import time
import mahotas

def sequence_ocr_processing(image_url):
	start = time.time()
	image_downloaded = Image.open(BytesIO(requests.get(image_url).content))
	download = time.time() - start
	recognised_string = pytesseract.image_to_string(image_downloaded, lang='eng').replace("\n","").upper()
	end = time.time() - start - download
	return (download, end, recognised_string)