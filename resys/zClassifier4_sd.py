#!/usr/bin/python
#-*-coding:utf8-*-

##   I am trying to make the classifier more general purpose
##   by reading the data from a file.
##   Each line of the file contains tab separated fields.
##   The first line of the file describes how those fields (columns) should
##   be interpreted. The descriptors in the fields of the first line are:
##
##        comment   -  this field should be interpreted as a comment
##        class     -  this field describes the class of the field
##        num       -  this field describes an integer attribute that should 
##                     be included in the computation.
##
##        more to be described as needed
## 
##
##    So, for example, if our file describes athletes and is of the form:
##    Shavonte Zellous   basketball  70  155
##    The first line might be:
##    comment   class  num   num
##
##    Meaning the first column (name of the player) should be considered a comment; 
##    the next column represents the class of the entry (the sport); 
##    and the next 2 represent attributes to use in the calculations.
##
##    The classifer reads this file into the list called data.
##    The format of each entry in that list is a tuple
##  
##    (class, normalized attribute-list, comment-list)
##
##    so, for example
##
##   [('basketball', [1.28, 1.71], ['Brittainey Raven']),
##    ('basketball', [0.89, 1.47], ['Shavonte Zellous']),
##    ('gymnastics', [-1.68, -0.75], ['Shawn Johnson']),
##    ('gymnastics', [-2.27, -1.2], ['Ksenia Semenova']),
##    ('track', [0.09, -0.06], ['Blake Russell'])]
##
##  map/filter/reduce，都是对一个集合进行处理，filter很容易理解用于过滤，map用于映射，reduce用于归并.
##  py3.x中map变成了lazy类


from math import sqrt
import codecs,sys,traceback,random

class Classifier:
    def __init__(self,path,filename):

        self.medianAndDeviation = []
        
        with codecs.open(path+filename,'r','utf-8') as f:
            lines = f.readlines()
            ## for line in f:
            ##    print(line.split('\t'))

        # 得到表头
        self.format = lines[0].strip().split('\t')
        self.data = []
        print(self.format)

        for line in lines[1:]:
            fields = line.strip().split('\t')
            ignore = []
            vector = []

            # 构造loiost数据结构
            for i in range(len(fields)):
                if self.format[i] == 'num':
                    vector.append(float(fields[i]))
                elif self.format[i] == 'comment':
                    ignore.append(fields[i])
                elif self.format[i] == 'class':
                    classification = fields[i]
            self.data.append((classification, vector, ignore))
        self.rawData = list(self.data)
        ## print(self.rawData)
        # get length of instance vector
        self.vlen = len(self.data[0][1])
        # now normalize the data
        for i in range(self.vlen):
            self.normalizeColumn(i)
    
    ##################################################
    ###
    ###  CODE TO COMPUTE THE MODIFIED STANDARD SCORE

    def getMedian(self, alist):
        """return median of alist"""
        if alist == []:
            return []
        blist = sorted(alist)
        length = len(alist)
        if length % 2 == 1:
            # length of list is odd so return middle element
            return blist[int(((length + 1) / 2) -  1)]
        else:
            # length of list is even so compute midpoint
            v1 = blist[int(length / 2)]
            v2 =blist[(int(length / 2) - 1)]
            return (v1 + v2) / 2.0        

    def getAbsoluteStandardDeviation(self, alist, median):
        """given alist and median return absolute standard deviation"""
        sum = 0
        for item in alist:
            sum += abs(item - median)
        return sum / len(alist)

    ## 初始化过程中对data数据的normalize
    def normalizeColumn(self, columnNumber):
       """given a column number, normalize that column in self.data"""
       # first extract values to list
       col = [v[1][columnNumber] for v in self.data]
       median = self.getMedian(col)
       asd = self.getAbsoluteStandardDeviation(col, median)
       #print("Median: %f   ASD = %f" % (median, asd))
       # 构造medianAndDeviation数据结构
       self.medianAndDeviation.append((median, asd))
       for v in self.data:
           v[1][columnNumber] = (v[1][columnNumber] - median) / asd
       ## print(self.data)


    # 对指定数据进行normalize
    def normalizeVector(self, v):
        """We have stored the median and asd for each column.
        We now use them to normalize vector v"""
        vector = list(v)
        for i in range(len(vector)):
            (median, asd) = self.medianAndDeviation[i]
            vector[i] = (vector[i] - median) / asd
        return vector
    
    ###
    ### END NORMALIZATION
    ##################################################

    ## 将manhattan距离转换成vector之间的操作
    def manhattan(self, vector1, vector2):
        """Computes the Manhattan distance."""
        return sum(map(lambda v1, v2: abs(v1 - v2), vector1, vector2))

    # 找出最近邻进行推荐
    def nearestNeighbor(self, itemVector):
        """return nearest neighbor to itemVector"""
        return min([ (self.manhattan(itemVector, item[1]), item)
                     for item in self.data])
    
    def classify(self, itemVector):
        """Return class we think item Vector is in"""
        return(self.nearestNeighbor(self.normalizeVector(itemVector))[1][0])


def unitTest():
    path = 'Classifier/'
    filename = 'athletesTrainingSet.txt'    
    classifier = Classifier(path,filename)
    br = ('Basketball', [72, 162], ['Brittainey Raven'])
    nl = ('Gymnastics', [61, 76], ['Viktoria Komova'])
    cl = ("Basketball", [74, 190], ['Crystal Langhorne'])
    # first check normalize function
    brNorm = classifier.normalizeVector(br[1])
    nlNorm = classifier.normalizeVector(nl[1])
    clNorm = classifier.normalizeVector(cl[1])
    assert(brNorm == classifier.data[1][1])
    assert(nlNorm == classifier.data[-1][1])
    print('normalizeVector fn OK')
    # check distance
    assert (round(classifier.manhattan(clNorm, classifier.data[1][1]), 5) == 1.16823)
    assert(classifier.manhattan(brNorm, classifier.data[1][1]) == 0)
    assert(classifier.manhattan(nlNorm, classifier.data[-1][1]) == 0)
    print('Manhattan distance fn OK')
    # Brittainey Raven's nearest neighbor should be herself
    result = classifier.nearestNeighbor(brNorm)
    assert(result[1][2]== br[2])
    # Nastia Liukin's nearest neighbor should be herself
    result = classifier.nearestNeighbor(nlNorm)
    assert(result[1][2]== nl[2])
    # Crystal Langhorne's nearest neighbor is Jennifer Lacy"
    assert(classifier.nearestNeighbor(clNorm)[1][2][0] == "Jennifer Lacy")
    print("Nearest Neighbor fn OK")
    # Check if classify correctly identifies sports
    assert(classifier.classify(br[1]) == 'Basketball')
    assert(classifier.classify(cl[1]) == 'Basketball')
    assert(classifier.classify(nl[1]) == 'Gymnastics')
    print('Classify fn OK')




def accruateTest(path,training_filename, test_filename):
    """Test the classifier on a test set of data"""
    classifier = Classifier(path,training_filename)
    f = open(path+test_filename)
    lines = f.readlines()
    f.close()
    numCorrect = 0.0
    for line in lines:
        data = line.strip().split('\t')
        vector = []
        classInColumn = -1
        for i in range(len(classifier.format)):
              if classifier.format[i] == 'num':
                  vector.append(float(data[i]))
              elif classifier.format[i] == 'class':
                  classInColumn = i
        theClass= classifier.classify(vector)
        prefix = '-'
        if theClass == data[classInColumn]:
            # it is correct
            numCorrect += 1
            prefix = '+'
        print("%s  %12s  %s" % (prefix, theClass, line))
    print("%4.2f%% correct" % (numCorrect * 100/ len(lines)))


   

if __name__=='__main__':
    import sys
    print(sys.path)
    dir(sys)
    assert(7==7)
    
    path = 'Classifier/'
    cf = Classifier(path,'athletesTrainingSet.txt')
    print(cf.data)
    
    list1 = [54, 72, 78, 49, 65, 63, 75, 67, 54, 76, 68,
             61, 58, 70, 70, 70, 63, 65, 66, 61]
    list2 = [66, 162, 204, 90, 99, 106, 175, 123, 68,
             200, 163, 95, 77, 108, 155, 155, 108, 106, 97, 76]
    m1 = cf.getMedian(list1)
    assert(round(m1, 3) == 65.5)
    m2 = cf.getMedian(list2)
    assert(round(m2, 3) == 107)
    assert(round(cf.getAbsoluteStandardDeviation(list1, m1),3) == 5.95)
    assert(round(cf.getAbsoluteStandardDeviation(list2, m2),3) == 33.65)
    print("getMedian and getAbsoluteStandardDeviation are OK")
    
    # test normalizeColumn
    list1 = [[-1.9328, -1.2184], [1.0924, 1.6345], [2.1008, 2.8826],
             [-2.7731, -0.5052], [-0.084, -0.2377], [-0.4202, -0.0297],
             [1.5966, 2.0208], [0.2521, 0.4755], [-1.9328, -1.159],
             [1.7647, 2.7637], [0.4202, 1.6642], [-0.7563, -0.3566],
             [-1.2605, -0.8915], [0.7563, 0.0297], [0.7563, 1.4264],
             [0.7563, 1.4264], [-0.4202, 0.0297], [-0.084, -0.0297],
             [0.084, -0.2972], [-0.7563, -0.9212]]

    for i in range(len(list1)):
        assert(round(cf.data[i][1][0],4) == list1[i][0])
        assert(round(cf.data[i][1][1],4) == list1[i][1])
    print("normalizeColumn is OK")

    print("开始unitTest")
    unitTest()    

    print("")
    accruateTest(path,'athletesTrainingSet.txt', 'athletesTestSet.txt')
    accruateTest(path,"irisTrainingSet.data", "irisTestSet.data")
    accruateTest(path,"mpgTrainingSet.txt", "mpgTestSet.txt")    
