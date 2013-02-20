import urllib, urllib2
import httplib, httplib2
import re, sys
import mechanize
import cookielib
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


def PostDirectory_PortalArticole(title, content, tags):
    # Browser
    br = mechanize.Browser()
    
    # Cookie Jar
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)
    
    # Browser options
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    
    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    
    # User-Agent (this is cheating, ok?)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    
    # The site we will navigate into, handling it's session
    br.open('http://portal-articole.ro/wp-login.php')
    #for f in br.forms():
    #    print f
    # Select the first (index zero) form
    
    br.select_form(nr=0)
    
    # User credentials
    br.form['log'] = 'george'
    br.form['pwd'] = '123789aA'
    br.submit()
    br.follow_link(nr=19)

    #Adaugi Titlu
    br.select_form(nr=1)
    br.form['post_title'] = title
    #Adaugi Content
    br.form['content'] = content
    #Adaugi Tag-uri
    br.form['tax_input[post_tag]'] = ','.join(tags)
    #Selectezi Categoria
    br.form.find_control("post_category[]", nr=1).value = ["79"]
    #Publish de Post
    br.submit("publish")


def PostDirectory_DirectorSubmit():
    pass

def PostDirectory_EArticole(title, content, tags):
    # Browser
    br = mechanize.Browser()
    
    # Cookie Jar
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)
    
    # Browser options
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    
    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    
    # User-Agent (this is cheating, ok?)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    
    # The site we will navigate into, handling it's session
    br.open('http://earticole.com/wp-login.php')
    #for f in br.forms():
    #    print f
    # Select the first (index zero) form
    
    br.select_form(nr=0)
    
    # User credentials
    br.form['log'] = 'george'
    br.form['pwd'] = 'ZxQXvHXBKEBv'
    br.submit()
    #br.follow_link(nr=19)
    #print br.response().read()

    #Adaugi Titlu
    br.select_form(nr=1)
    br.form['title'] = title
    #Adaugi Content
    br.form['post'] = content
    #Adaugi Tag-uri
    #br.form['tax_input[post_tag]'] = 'tag1, tag2'
    #Selectezi Categoria
    br.form.find_control("cats[]", nr=0).value = ["820"]
    #Publish de Post
    br.submit()