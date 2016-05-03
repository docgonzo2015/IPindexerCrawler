# IPindexerCrawler

crawler for [ipindex](http://ipindex.dihe.de/index.php)

## How it works?
1. Download the tool
```bash
wget -O ipindex.tar.gz https://github.com/lucidtrip/IPindexerCrawler/archive/master.tar.gz
tar xfvz ipindex.tar.gz
python IPindexerCrawler-master --help
```
2. You need a file in each line are an URL.
exampel:
```text
http://google.com/
http://wordpress.com/
etc...
```
3. Start the python script.
4. Now you have a `new_rang.txt` file with the IP-Rangs.
5. Have fun!

## help
```
usage: . [-h] [-m MAX_RANG_SIZE] [-r] FILE

positional arguments:
  FILE                  The file with urls (one url per line!)

optional arguments:
  -h, --help            show this help message and exit
  -m MAX_RANG_SIZE, --max-rang-size MAX_RANG_SIZE
                        The maximal rang size (default=4294967296(=Total
                        number of IPv4 addresses)) (6400=25*256)
  -r, --resize          Resize to big rangs to the max-rang-size
```

## examples
- simpel
```python ipindex.py urls.txt```
- resize the crawled rang
```python ipindex.py urls.txt -m 6400 -r```
- ignor rangs bigger than 6400 ip adresses (whithout resize)
```python ipindex.py urls.txt -m 6400```

## history:
- 03/05/2016: upload to github
- 02/05/2016: project start

## Support
You can support me for more useful tools and scripts with a litte donation
* Bitcoin: 16codezBZqw3Uc2tCcrxZ3q62SFoKGjJFq
