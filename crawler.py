import urllib.request 
from multiprocessing import Pool, Queue
from pageProcessor import PageProcessor
from resultProcessor import ResultProcessor

class Crawler():

    def __init__(self, infile):
        self.startfile = infile

    def crawl(self):
        text = ""
        with open(self.startfile, "r") as f:
            text = f.read()
        done = []
        toProcess = []
        exclude = []
        #get initial links
        lmap = {}
        for x in text.split("\n"):
             if(x!=""):
                 toProcess.append(x)
        while toProcess != [] and len(done)<75:
            poolcnt = 4
            #if there are less links than desired num of pools, reduce number of pools
            if(len(toProcess)<poolcnt):
                poolcnt = len(toProcess)
            #remove links that have been looked at, or are duplicates
            toProcess = [toProcess[x] for x in range(0, len(toProcess)) if toProcess[x] not in exclude and toProcess[x] not in toProcess[0:x]]
            split = []
            #If the number of links in list would put us over 75 pages processed, only send part of the list
            if(len(toProcess) + len(done)>75 ):
                split = self.splitArray(toProcess[0:75-len(done)], poolcnt)
            else:
                #split the link list evenly into multiple parts, to send to each pool
                split = self.splitArray(toProcess[0:len(toProcess)], poolcnt)
            with Pool(poolcnt) as p:
                #process sent links
                result = p.map(self.crawlWorker, split)
            for tup in result:
                #put all links (success or error) processed into exclude list, for checking duplicates
                exclude.extend(tup[0])
                exclude.extend(tup[1])
                #Successfully processed links go into done list
                done.extend(tup[0])
                #new links go to the main link list
                toProcess.extend(tup[2])
                #store what pages had which links in a map
                for k, v in tup[3].items():
                    if(k in lmap):
                        lmap[k].append(v)
                    else:
                        lmap[k] = v
        for x in done: print(x)
        
        return lmap
            
            


            


    def crawlWorker(self, pages):
        success = []
        error = []
        new = []
        lmap = {}
        for page in pages:
            try:
                processor = PageProcessor()
                html = urllib.request.urlopen(page)
                pageText = str(html.read())
                processor.setPage(pageText)
                temp = processor.getLinks()
                lmap[page] = temp
                new.extend(temp)
                success.append(page)
                print("Page Processed")
            except Exception as e:
                error.append(page)
                print(e)
        return success, error, new, lmap

    #split an array into multiple subarrays evenly, used to divide up the work among processes
    def splitArray(self, arr, max = 4):
        if(max>len(arr)):
            max = len(arr)
        result = [[] for x in range(0,max)]
        cnt = 0
        for el in arr:
            result[cnt].append(el)
            cnt = (cnt+1)%max
        return result





def main():
    crawler = Crawler("urls6.txt")
    lmap = crawler.crawl()
    rprocessor = ResultProcessor(lmap)
    rprocessor.drawAndWrite()


if __name__ == "__main__":
    main()
