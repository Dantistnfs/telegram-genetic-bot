# Telegram Gene Bot
Small bot that was created to help you in your gene-lab practice.

[Add bot to your contacts](http://telegram.me/genetics_bot)

Or just scan qr-code:

![qrcode](https://chart.googleapis.com/chart?cht=qr&chl=http%3A%2F%2Ftelegram.me%2Fgenetics_bot&chs=180x180&choe=UTF-8&chld=L|2)


## Avalible functions

For now he can:
- Reverse Transcription: ```/RT [nucleotide sequence]```
- ENTREZID Search: ```/enterezid [ENTREZID]```
- Search by GENENAME in NCBI database ```/ncbigene [GENE NAME]```
- Make recognition of seqeunces from photo```/ocr_seqeunce```

## TODO function
- [x] Gene ENTREZID
- [x] Gene GENENAME
- [x] Sequence recognition from image
- [ ] Gene transcription factors
- [ ] Probably converters
- [ ] Sci-Hub search
- [ ] Impact factor search?
- [ ] Metabolic search?

## Configure and run

Clone the repository
```
git clone https://github.com/Dantistnfs/telegram-genetic-bot/
```
Install some dev packages (you might need more, depends on your currently installed libs)
```
 sudo apt-get install python3-dev libffi-dev tesseract-ocr
```
Create python virtual environment in the project root directory (don't forget about python3)
```
cd telegram-genetic-bot
virtualenv -p python3 venv
```
Enter the virtual environment
```
source venv/bin/activate
```
Update the dependencies
```
pip install -r requirements.txt
```
Create .env file and add bot api key (get one from [BotFather](https://telegram.me/botfather)):
```
echo "TELEGRAM_BOT_API_KEY = YOUR_KEY_FROM_BOT_FATHER" > .env
```
Install heroky CLI from [here](https://devcenter.heroku.com/articles/heroku-cli#download-and-install) and run locally, you will also need to register on heroku to enter credentials
```
heroku local
```
Now you are ready to test your bot with [Telegram clients](https://telegram.org/apps). Enjoy!


## REFERENCES

1. Cock PA, Antao T, Chang JT, Bradman BA, Cox CJ, Dalke A, Friedberg I, Hamelryck T, Kauff F, Wilczynski B and de Hoon MJL (2009) Biopython: freely available Python tools for computational molecular biology and bioinformatics. Bioinformatics, 25, 1422-1423
2. Coelho, L.P. 2013. Mahotas: Open source software for scriptable computer vision. Journal of Open Research Software 1(1):e3, DOI: http://dx.doi.org/10.5334/jors.ac


## DISCLAIMER

Photos that you send to ocr processing, stored on Heroku servers only on time when they are processed, but it may be stored on Telegram servers, thus I don't take responsibility for errors in ocr, information loss, hardware errors, etc.


## Thanks to:

- [zaytoun]https://github.com/zaytoun for creating sci-hub python API.


