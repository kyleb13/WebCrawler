import re
import urllib.request 

class PageProcessor():

    def __init__(self, inpage = ""):
        self.page = inpage

    def setPage(self, newpage):
        self.page = newpage



    def getLinks(self):
        ##grab all anchor tags
        results = re.findall(r"(?i)<a\s[^>]+>", self.page)
        temp = []
        #filter out anchor tags without href's
        for match in results:
            hrefPresent = re.search(r"href\s*=\s*[\'\"][^.\s]+\.[^.\s]+\.[^\'\"]+[\'\"]", match)
            if(hrefPresent != None):
                temp.append(hrefPresent[0])
        results = temp
        #get link from href
        results = [re.search(r"[\'\"].+[\'\"]",s)[0] for s in results]
        #remove quotation marks
        results = [link[1:len(link)-1] for link in results]
        #some pages have had links with slashes in front. but no http,
        #so if a link is like that, add https: so it can be processed
        for idx in range(0,len(results)):
            if(results[idx][0:2] == "//"):
                results[idx] = "https:" + results[idx]
        return results


def main():
    # testfile = open("test.html", "r")
    # text = testfile.read()
    # processor = PageProcessor(str(urllib.request.urlopen("http://www.facebook.com/AlbertEinstein").read()))
    # results = processor.getLinks()
    # for x in results: print(x)
    processor = PageProcessor("<A fdsafdsa='test' href='//www.test.com/willitwork/maybeso.html'> <A href='test.css>'")
    results = processor.getLinks()
    print(results)

if __name__ == "__main__":
    main()