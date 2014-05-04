#!/usr/bin/python
#-*-coding:utf8-*-

from math import sqrt
import codecs,sys,traceback,random

athletes = {"Shawn Johnson": [57, 90],
            "Li Shanshan": [57, 79],
            "Deng Linlin": [54, 68],
            "Bridget Sloan": [59, 104],
            "Nastia Liukin": [63, 99],
            "Ksenia Semenova": [54, 77],
            "Jennifer Lacy": [75, 175],
            "Shavonte Zellous": [70, 155],
            "Nakia Sanford": [76, 200],
            "Shanna Crossley": [70, 155],
            "Brittainey Raven": [72, 162],
            "Nikki Blue": [68,163],
            "Dita Constantina": [65, 105],
            "Lisa Hunter-Galvan": [66, 132],
            "Mara Yamauchi": [64, 112],
            "Blake Russell": [66, 110],
            "Martha Komu": [65, 115],
            "Jelena Prokopcuka": [66, 112]}

sport = {"Shawn Johnson": "Gymnastics",
            "Li Shanshan": "Gymnastics",
            "Deng Linlin": "Gymnastics",
            "Bridget Sloan": "Gymnastics",
            "Nastia Liukin": "Gymnastics",
            "Ksenia Semenova": "Gymnastics",
            "Jennifer Lacy": "Basketball",
            "Shavonte Zellous": "Basketball",
            "Nakia Sanford": "Basketball",
            "Shanna Crossley": "Basketball",
            "Brittainey Raven": "Basketball",
            "Nikki Blue": "Basketball",
            "Dita Constantina": "Track",
            "Lisa Hunter-Galvan": "Track",
            "Mara Yamauchi": "Track",
            "Blake Russell": "Track",
            "Martha Komu": "Track",
            "Jelena Prokopcuka": "Track"}

data  = [['i100', 'both', 'sedentary', 'moderate', 'yes'],
         ['i100', 'both', 'sedentary', 'moderate', 'no'],
         ['i500', 'health', 'sedentary', 'moderate', 'yes'],
         ['i500', 'appearance', 'active', 'moderate', 'yes'],
         ['i500', 'appearance', 'moderate', 'aggressive', 'yes'],
         ['i100', 'appearance', 'moderate', 'aggressive', 'no'],
         ['i500', 'health', 'moderate', 'aggressive', 'no'],
         ['i100', 'both', 'active', 'moderate', 'yes'],
         ['i500', 'both', 'moderate', 'aggressive', 'yes'],
         ['i500', 'appearance', 'active', 'aggressive', 'yes'],
         ['i500', 'both', 'active', 'aggressive', 'no'],
         ['i500', 'health', 'active', 'moderate', 'no'],
         ['i500', 'health', 'sedentary', 'aggressive', 'yes'],
         ['i100', 'appearance', 'active', 'moderate', 'no'],
         ['i100', 'health', 'sedentary', 'moderate', 'no']]


class KnnClassifier:
    def __init__(self, data = {}, category = {}):
        self.data = data
        self.category = category
        self.normalizeValues = {}

    def loadData(self, filename):
        f = open(filename)
        i = 0
        for line in f:
            elements = line.split('\t')
            if len(elements) >= 5:
                i += 1
                name = elements[0]
                sport = elements[1]
                # not using age which is elements[2]
                height = int(elements[3])
                weight = int(elements[4])
                #print("%s SPORT: %s  hght: %i  wt: %i" % (name, sport, height, weight))
                self.data[name] = [height, weight]
                self.category[name] = sport
            else:
                print("SKIPPING %s" % line)
        print("%i entries loaded" % i)
    
    ##################################################
    ###
    ###   ADDED CODE TO COMPUTE STANDARDIZED SCORE

    def getMedian(self, alist):
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
        sum = 0
        for item in alist:
            sum += abs(item - median)
        return sum / len(alist)


    def normalize(self, alist):
        median = self.getMedian(alist)
        print(median)
        asd = self.getAbsoluteStandardDeviation(alist, median)
        print(asd)
        for element in alist:
            print((element - median) / asd)

    def normalizeColumn(self, columnNumber):
        # first extract values to list
        col = [v[columnNumber - 1] for v in self.data.values()]
        print(col)
        median = self.getMedian(col)
        asd = self.getAbsoluteStandardDeviation(col, median)
        print("Median: %f   ASD = %f" % (median, asd))
        self.normalizeValues[columnNumber - 1] = (median, asd)
        
        for (k, v) in self.data.items():
            tmp = self.data[k]
            #tmp[columnNumber] = (v - median) / asd
            self.data[k][columnNumber - 1] = (v[columnNumber - 1] - median) / asd


    def normalizeInstance(self, instanceVector):
        result = []
        for i in range(len(instanceVector)):
            if i in self.normalizeValues:
                (median, asd) = self.normalizeValues[i]
                result.append((instanceVector[i] - median) / asd)
            else:
                result.append(instanceVector[i])
        return result

    def manhattan(self, vector1, vector2):
        """Computes the Manhattan distance."""
        distance = 0
        total = 0
        n = len(vector1)
        for i in range(n):
            distance += abs(vector1[i] - vector2[i])
            total += 1
        return distance


    def computeNearestNeighbor(self, itemName, itemVector):
        """creates a sorted list of items based on their distance to item"""
        distances = []
        for otherItem in self.data:
            if otherItem != itemName:
                distance = self.manhattan(itemVector, self.data[otherItem])
                distances.append((distance, otherItem))
        # sort based on distance -- closest first
        distances.sort()
        return distances

    def classify(self, itemName, itemVector):
        """Classify the itemName based on user ratings
           Should really have items and users as parameters"""
        # first find nearest neighbor
        nearest = self.computeNearestNeighbor(itemName, self.normalizeInstance(itemVector))[0][1]
        rating = self.category[nearest]
        #print(itemVector)
        #print("Closest to %s" % nearest)
        #print("%s: %s" % (itemName, rating))
        return rating


    ## KNN算法计算
    def kNN(self, itemName, itemVector, k):
        # first find nearest neighbor
        tmp = {}
        resultSet = self.computeNearestNeighbor(itemName, self.normalizeInstance(itemVector))[:k]
        # the resultSet now contains the k nearest neighbors
        for res in resultSet:
            classification = self.category[res[1]]
            if classification in tmp:
                tmp[classification] += 1
            else:
                tmp[classification] = 1

        
        recommendations = list(tmp.items())
        # recommendations is a list of classes and how many times
        # that class appeared in the nearest neighbor list (votes)
        # i.e. [['gymnastics', 2], ['track', 1]]
        recommendations.sort(key=lambda artistTuple: artistTuple[1], reverse = True)
        print(recommendations)
        # construct list of classes that have the largest number of votes
        topRecommendations = list (filter(lambda k: k[1] == recommendations[0][1], recommendations))
        # if only one class has the highest number of votes return that class
        if len(topRecommendations) == 1:
            rating =  topRecommendations[0][0]
        else:
            rint = random.randint(0, len(topRecommendations) - 1)
            rating = topRecommendations[rint][0]
        return rating


    def evalClassifier(self, filename):
        """evaluate test set data"""
        f = open(filename)
        total = 0
        correct = 0
        for line in f:
            elements = line.split('\t')
            if len(elements) >= 5:
                total += 1
                name = elements[0]
                sport = elements[1]
                # not using age which is elements[2]
                height = int(elements[3])
                weight = int(elements[4])
                classification = self.classify(name, (height, weight))
                if classification == sport:
                    print("%s CORRECT" % name)
                    correct += 1
                else:
                    print("%s MISCLASSIFIED AS %s. Should be %s" % (name, classification, sport))
        print("%f correct" % (correct / total))
 
    def evalKNN(self, filename):
            """evaluate test set data"""
            f = open(filename)
            total = 0
            correct = 0
            for line in f:
                elements = line.split('\t')
                if len(elements) >= 5:
                    total += 1
                    name = elements[0]
                    sport = elements[1]
                    # not using age which is elements[2]
                    height = int(elements[3])
                    weight = int(elements[4])
                    #print("%s SPORT: %s  hght: %i  wt: %i" % (name, sport, height, weight))
                    classification = self.kNN(name, (height, weight), 3)
                    if classification == sport:
                        print("%s CORRECT" % name)
                        correct += 1
                    else:
                        print("%s MISCLASSIFIED AS %s. Should be %s" % (name, classification, sport))
            print("%f correct" % (correct / total))


class Bayes:    
    def __init__(self, data):
        # here I am assuming the first column of the data is the class.
        self.data = data
        self.prior = {} # 先验概率
        self.conditional = {} # 条件概率

    def train(self):
         """train the Bayes Classifier
         basically a lot of counting"""
         total = 0
         classes = {} 
         counts = {}
         # determine size of a training vector
         size = len(self.data[0])
         #
         #   iterate through training instances
         for instance in self.data:
             total += 1
             category = instance[0]
             classes.setdefault(category, 0)
             counts.setdefault(category, {})
             classes[category] += 1
             # now process each column in instance
             col = 0
             for columnValue in instance[1:]:
                 col += 1
                 tmp = {}
                 if col in counts[category]:
                     tmp = counts[category][col]
                 if columnValue in tmp:
                     tmp[columnValue] += 1
                 else:
                    tmp[columnValue] = 1
                 counts[category][col] = tmp
             ## print(classes) {'i500': 9, 'i100': 6}
             ## print(counts)
                #############################
                ## counts数据结构: 但该DS有一个不足就是：如果数据量特别大的时候，数据结构的构造非常麻烦。
                # {'i500': {1: {'appearance': 3, 'health': 4, 'both': 2}, 2: {'active': 4, 'sedentary': 2, 'moderate': 3}, 3: {'aggressive': 6, 'moderate': 3}, 4: {'yes': 6, 'no': 3}},
                #  'i100': {1: {'both': 3, 'health': 1, 'appearance': 2}, 2: {'active': 2, 'sedentary': 3, 'moderate': 1}, 3: {'aggressive': 1, 'moderate': 5}, 4: {'yes': 2, 'no': 4}}}
                #############################


         # ok. done counting. now compute probabilities
         #
         # first prior probabilities
         #         
         for (category, count) in classes.items():
             self.prior[category] = count / total
         # now compute conditional probabilities 算法改进
         for (category, columns) in counts.items():
             tmp = {}
             for (col, valueCounts) in columns.items():
                 tmp2 = {}
                 for (value, count) in valueCounts.items():
                     tmp2[value] = count / classes[category]
                 tmp[col] = tmp2
             #convert tmp to vector
             tmp3 = []
             for i in range(1, size):
                 tmp3.append(tmp[i])
             self.conditional[category] = tmp3
         ## print(self.conditional)
            #############################
            ## conditional数据结构
            # {'i500': [{'health': 0.4444444444444444, 'appearance': 0.3333333333333333, 'both': 0.2222222222222222}, 
            # {'active': 0.4444444444444444, 'sedentary': 0.2222222222222222, 'moderate': 0.3333333333333333}, 
            # {'aggressive': 0.6666666666666666, 'moderate': 0.3333333333333333}, 
            # {'yes': 0.6666666666666666, 'no': 0.3333333333333333}], 
            # 'i100': [{'both': 0.5, 'health': 0.16666666666666666, 'appearance': 0.3333333333333333}, 
            # {'active': 0.3333333333333333, 'sedentary': 0.5, 'moderate': 0.16666666666666666}, 
            # {'aggressive': 0.16666666666666666, 'moderate': 0.8333333333333334}, 
            # {'yes': 0.3333333333333333, 'no': 0.6666666666666666}]}
            #############################


    ## 计算公式如下：
    ## P(i100 | health, moderateExercise, moderateMotivation, techComfortable)  = 
    ## P(health|i100) P(moderateExercise|i100) P(moderateMotivated|i100) P(techComfortable|i100)P(i100)
    def classify(self, instance):
        categories = {}
        for (category, vector) in self.conditional.items():
            prob = 1
            for i in range(len(vector)):
                colProbability = .0000001
                if instance[i] in vector[i]:
                    # get the probability for that column value
                    colProbability = vector[i][instance[i]]
                prob = prob * colProbability
            prob = prob * self.prior[category]
            categories[category]  = prob
        cat = list(categories.items())
        cat.sort(key=lambda catTuple: catTuple[1], reverse = True)
        ## print(cat)
        return (cat[0])if len(cat)!=0 else []


if __name__ == '__main__':
    knncf = KnnClassifier()
    path = 'Classifier/'
    trainpath = path+'athletes2.txt'
    testpath = path+'athletes2Test.txt'
    knncf.loadData(trainpath)
    knncf.evalClassifier(testpath)

    print('KNN分类')
    print(knncf.kNN('Paula Radcliffe', (63, 99), 3))

    print('Bayes分类')
    bayes = Bayes(data)
    bayes.train()
    print(bayes.classify(['health', 'moderate', 'aggressive', 'yes']))
    print(bayes.classify(['health', 'moderate', 'moderate', 'yes']))
    print(bayes.classify(['appearance', 'moderate', 'moderate', 'no']))
