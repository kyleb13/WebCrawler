from class_point import Point
from class_showpoint import ShowPoint
from class_showline import ShowLine
from tkinter import Tk, Canvas, W
from random import Random

alphabet = "abcdefghijklmno"

#represents a drawable text element 
class DrawText():
    def __init__(self, c, inpoint = Point(), intext = ""):
        self.canvas = c
        self.point = inpoint
        self.text = intext

    def draw(self):
        self.canvas.create_text(self.point.xpt, self.point.ypt, anchor =W, text=self.text, fill="red", font=("Helvetica bold", 12))

#Class for processing the results of the crawler
class ResultProcessor():
    def __init__(self, inlinks = {}):
        self.linkmap = inlinks
        self.displaydim= 800
        self.labels = []
        for char in alphabet:
            for i in range(1,6):
                self.labels.append(char + str(i))

    #draw the graph that represents the relationships between links,
    #and write relevant info to a csv file. Both are done in the same method out of convenience 
    def drawAndWrite(self):
        top = Tk()
        canvas = Canvas(top, width = self.displaydim, height = self.displaydim)
        canvas.pack()
        #remember what links have already been drawn
        drawn = {}
        #store the num of times each page is linked to
        popular = {}
        rand = Random()
        #the main output file
        outcsv = open("out.csv", "w")
        #stores a table that shows which links are referenced by which label
        table = open("table.csv", "w")
        outcsv.write("Page,Links\n")
        table.write("Label,Page\n")
        for k, v in self.linkmap.items():
            kpoint = None
            #if a point has been drawn before, get the object from the map
            if(k in drawn):
                kpoint = drawn[k]
            else:
            #otherwise make a new point and store it in the map
                kx = rand.randint(0,self.displaydim)
                ky = rand.randint(0,self.displaydim)
                kpoint = DrawText(canvas, Point(kx, ky), self.labels.pop(0))
                table.write(kpoint.text + "," + k + "\n")
                kpoint.draw()
                drawn[k] = kpoint
            #string for bulding tuples in the output file
            writestr = k + ","
            for val in v:
                #limit the points drawn to the pages that were processed, for visibility's sake
                if val in self.linkmap:
                    vpoint = None
                    #same idea as before, but for the values
                    if(val in drawn):
                        vpoint = drawn[val]
                    else:
                        vx = rand.randint(0,self.displaydim)
                        vy = rand.randint(0,self.displaydim)
                        vpoint = DrawText(canvas, Point(vx, vy), self.labels.pop(0))
                        table.write(vpoint.text + "," + val + "\n")
                        vpoint.draw()
                        drawn[val] = vpoint
                    line = ShowLine(canvas, Point(kpoint.point.xpt, kpoint.point.ypt), Point(vpoint.point.xpt, vpoint.point.ypt))
                    line.draw()
                writestr += val + ","
                #update popularity stats
                if val in popular:
                    popular[val] += 1
                else:
                    popular[val] = 1
            writestr+="\n"
            #write output string to file
            outcsv.write(writestr)
        
        #find the most popular link
        mostpopular = max([count for count in popular.values()])
        popularlist = [coolkid for coolkid in popular.keys() if popular[coolkid] == mostpopular]
        print("most popular: " + str(popularlist) + "\ncnt: " + str(mostpopular))
        outcsv.write("most popular:," + str(popularlist) + "\ncnt:," + str(mostpopular))
        outcsv.close()
        table.close()
        top.mainloop()



