try:
    import Image
except ImportError:
    from PIL import Image

from . import pytesseract
import requests
from io import BytesIO

def sequence_ocr_processing(image_url):

	return pytesseract.image_to_string(Image.open(BytesIO(requests.get(image_url).content)), lang='eng')