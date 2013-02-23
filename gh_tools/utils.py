

def unescape(html):
    "Returns the given HTML with ampersands, quotes and carets decoded" 
    if not isinstance(html, basestring): 
        html = str(html) 
    return html.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&#39;',"'")