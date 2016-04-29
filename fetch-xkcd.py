import urllib, urllib2, re, sys, os, time
from HTMLParser import HTMLParser
# Defining our method of removing HTML tags from alt text when naming retrieved
# files.
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)
# Function that will strip HTML tags from a string.
def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()
# Main function.
def main(argv):
    def usage():
        print("""ABOUT//

Fetch-XKCD v1.0!

Fetch-XKCD is a tool for downloading and updating a collection of comics from popular webcomic xkcd.com. Simply put it in an empty directory and run it to fill that directory with every comic. Then whenever you want to update your collection, simply run it again.

Fetch-XKCD was written in Python 2.7.3 and may not work in Python 3.x.

USAGE//

Place fetch-xkcd.py into an empty directory and run it. Comics will be saved to the comics subdirectory. To bring your collection up to date, run it again.

optional arguments:
  -h, --help              Show this help message and exit
  -n, --nag               Skip nag message""")
    nagmsg = True
    for arg in argv:
        if 'h' in arg:
            usage()
            sys.exit()
        if 'n' in arg:
            nagmsg = False
    print('\n')
    print('  _____    _       _         __  ___  ______ ____  ')
    print(' |  ___|__| |_ ___| |__      \ \/ / |/ / ___|  _ \ ')
    print(" | |_ / _ \ __/ __| '_ \ _____\  /| ' / |   | | | |")
    print(' |  _|  __/ || (__| | | |_____/  \| . \ |___| |_| |')
    print(' |_|  \___|\__\___|_| |_|    /_/\_\_|\_\____|____/ ')
    print('                                                   ')
    print('\n* Fetch-XKCD v1.0\n\n')
    if (nagmsg):
        print('* Check out the latest merch at store.xkcd.com - support your favorite comic!\n')
        time.sleep(1)
        print('* Check out the latest merch at store.xkcd.com - support your favorite comic!\n')
        time.sleep(1)
        print('* Check out the latest merch at store.xkcd.com - support your favorite comic!\n')
        time.sleep(1)
        print('* Check out the latest merch at store.xkcd.com - support your favorite comic!\n')
        time.sleep(1)
        print('* Check out the latest merch at store.xkcd.com - support your favorite comic!\n')
        time.sleep(1)
    print('* Checking xkcd.com for total comics in database...')
    xkcdhomestring = urllib2.urlopen('http://xkcd.com/').read()
    # Get number of comics available so we know how many to retrieve.
    totalzoom1 = re.search('<a rel="prev".+?>', xkcdhomestring).group(0)
    total = int(re.search('\d+', totalzoom1).group(0)) + 1
    print('* ' + str(total) + ' comics found in database.\n')
    total_fetched = 0
    # Create comics folder if needed
    if os.path.isdir('comics') == False:
        os.mkdir('comics')
    # Create a list of all comics already downloaded.
    print('* Checking for gaps in your comic collection...')
    filelist = os.listdir('comics/')
    removethese = []
    for i in filelist:
        if i[-3:] not in ['jpg', 'png', 'gif']:
            removethese.append(i)
    for i in removethese:
        filelist.remove(i)
    comicnumbers = []
    for i in filelist:
        comicnumbers.append(int(re.search('\d+ -', i).group(0)[:-2]))
    # Loop through all the comics, retrieve and rename every one in local
    # working directory.
    print('* Done evaluating collection.\n')
    print('* Retrieving all comics not already in your collection...\n')
    comic_exceptions = [404,    # 404: Comic not found
                        1193,   # Comic not an image
                        1350,   # Links to the wrong comic!
                        1446,   # Hotlink broken
                        1608,   # No static comic
                        1663]   # No static comic
    for i in range(1, total+1):
        if (i in comic_exceptions):
            continue
        if (i) not in comicnumbers:
            print('* Fetching comic #' + str(i) + '...')
            xkcd = urllib2.urlopen('http://xkcd.com/' + str(i) + '/')
            xkcdtext = xkcd.read()
            imgre = re.search('Image URL \(for hotlinking/embedding\): (http://imgs\.xkcd\.com/comics/(.*)(\.jpg|\.png|\.gif))\n',xkcdtext)
            if (imgre == None):
                print "Comic not found!"
                continue
            imgurl = imgre.group(1)
            ext = imgre.group(3)
            alt = re.search('<div id="ctitle">(.*)</div>',xkcdtext).group(1)
            # To make sure our filename is writable, we strip HTML tags, and
            # strip any character not in the whitelist.
            valid_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 -_()!@#$%^&+=;'\",.~`"
            parser = HTMLParser()
            valid_filename = strip_tags(str(parser.unescape(''.join(c for c in alt if c in valid_chars))))
            target_filename = 'comics/'+str(i) + ' - ' + valid_filename + ext
            urllib.urlretrieve(imgurl, target_filename)
            total_fetched += 1
            print("* Success! Comic saved as: \"" + target_filename + "\"")
    print('\n* Total files retrieved: ' + str(total_fetched) + '\n')
    print("* Fetch-XKCD finished! Enjoy your comics!")
    time.sleep(5)
if __name__ == '__main__':
    main(sys.argv[1:])