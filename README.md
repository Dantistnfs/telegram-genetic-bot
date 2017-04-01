# Telegram Gene Bot
Small bot that was created to help you in your gene-lab practice.

[Add bot to your contacts](http://telegram.me/genetics_bot)
Or just scan qr-code:

![GitHub Logo](https://chart.googleapis.com/chart?cht=qr&chl=http%3A%2F%2Ftelegram.me%2Fgenetics_bot&chs=180x180&choe=UTF-8&chld=L|2)


## Avalible functions

For now he can:
- Reverse Transcription: ```/RT [nucleotide sequence]```
- ENTREZID Search: ```/enterezid [ENTREZID]```
- Search by GENENAME in NCBI database ```/ncbigene [GENE NAME] ```
- Make recognition of text ```/ocr_sequnce```

## TODO function
- [x] Gene ENTREZID
- [x] Gene GENENAME
- [ ] Rewrite ncbigene function to make it faster, now it uses 2 GET's from website.
- [x] Sequence recognition from image, partialy, still need upgrade to make this feature powerfull
- [ ] Gene transcription factors
- [ ] Probably converters
- [ ] Sci-Hub search
- [ ] Impact factor search?
- [ ] Metabolic search?

## Documentaion

Documentation will be written later

## REFERENCES

1. Cock PA, Antao T, Chang JT, Bradman BA, Cox CJ, Dalke A, Friedberg I, Hamelryck T, Kauff F, Wilczynski B and de Hoon MJL (2009) Biopython: freely available Python tools for computational molecular biology and bioinformatics. Bioinformatics, 25, 1422-1423
2. Coelho, L.P. 2013. Mahotas: Open source software for scriptable computer vision. Journal of Open Research Software 1(1):e3, DOI: http://dx.doi.org/10.5334/jors.ac
