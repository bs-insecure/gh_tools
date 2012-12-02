import urllib,urllib2
import httplib
 
from BeautifulSoup import BeautifulSoup
 
def bing_grab(query):
 
    address = "http://www.bing.com/search?q=%s" % (urllib.quote_plus(query))
    request = urllib2.Request(address, None, {'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)'} )
    urlfile = urllib2.urlopen(request)
    page = urlfile.read(200000)
    urlfile.close()
 
    soup = BeautifulSoup(page)
    links =   [x.find('a')['href'] for x in soup.find('div', id='results').findAll('h3')]
 
    return links


def GetPageRank(query):
    def GetHash(query):
        SEED = "Mining PageRank is AGAINST GOOGLE'S TERMS OF SERVICE. Yes, I'm talking to you, scammer."
        Result = 0x01020345
        for i in range(len(query)) :
            Result ^= ord(SEED[i%len(SEED)]) ^ ord(query[i])
            Result = Result >> 23 | Result << 9
            Result &= 0xffffffff
        return '8%x' % Result

    prhost='toolbarqueries.google.com'
    prpath='/tbr?client=navclient-auto&ch=%s&features=Rank&q=info:%s'

    conn = httplib.HTTPConnection(prhost)
    hsh = GetHash(query)
    path = prpath % (hsh,query)
    conn.request("GET", path)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    ret = data.split(":")[-1]
    if ret == '':
        ret = None
    else:
        ret = int(ret)
    return ret
