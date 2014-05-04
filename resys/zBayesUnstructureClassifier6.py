import os, codecs, math

## 
## 对文本数据进行bayes分类
## Bayes理论的另一应用（Novig的拼写检查器）：http://blog.youxu.info/spell-correct.html
##

class BayesText:
    def __init__(self, trainingdir, stopwordlist):
        """This class implements a naive Bayes approach to text classification
        trainingdir is the training data. Each subdirectory of trainingdir is titled with the
        name of the classification category -- those subdirectories in turn contain the text files
        for that category.
        The stopwordlist is a list of words (one per line) will be removed before any counting takes
        place.
        """
        self.vocabulary = {}
        self.prob = {}
        self.totals = {}
        self.stopwords = {}
        f = open(stopwordlist)
        for line in f:
            self.stopwords[line.strip()] = 1
        f.close()
        # 与sys.path的区别，os.listdir展示dir路径下的所有文件
        categories = os.listdir(trainingdir)
        #filter out files that are not directories
        # 这里可以用python对模式识别中的pcx数据进行分类
        self.categories = [filename for filename in categories if os.path.isdir(trainingdir + filename)]
        print("Counting ...")
        for category in self.categories:
            print('    ' + category)
            (self.prob[category], self.totals[category]) = self.train(trainingdir, category)        
        # print(list(self.prob.items())[0])
        # print(list(self.totals.items())[0])
        # print(list(self.vocabulary.items())[0])
        
        ''' 注意：python list删除操作 '''
        # I am going to eliminate any word in the vocabulary that doesn't occur at least 3 times
        toDelete = []
        for word in self.vocabulary:
            if self.vocabulary[word] < 3:
                # mark word for deletion
                # can't delete now because you can't delete from a list you are currently
                # iterating over
                toDelete.append(word)
        # now delete
        for word in toDelete:
            del self.vocabulary[word]

            
        # now compute probabilities 计算概率
        ## p(W(k)|H(i)) = (N(k)+1)/(N+|vocabulary|)
        ## 其中W(k)表示文档中独立的单词个数，N(k)表示每个字出现的次数；
        ## |vocabulary|即W(k)，N表示文档中总的单词个数
        vocabLength = len(self.vocabulary)
        print("Computing probabilities:")
        for category in self.categories:
            print('    ' + category)
            denominator = self.totals[category] + vocabLength
            for word in self.vocabulary:
                if word in self.prob[category]:
                    count = self.prob[category][word]
                else:
                    count = 1
                self.prob[category][word] = (count + 1) / denominator
                    

    def train(self, trainingdir, category):
        """counts word occurrences for a particular category"""
        currentdir = trainingdir + category
        files = os.listdir(currentdir)
        counts = {}
        total = 0
        for file in files:
            #print(currentdir + '/' + file)
            f = codecs.open(currentdir + '/' + file, 'r', 'iso8859-1')
            for line in f:
                tokens = line.split()
                for token in tokens:
                    # get rid of punctuation and lowercase token
                    token = token.strip('\'".,?:-')
                    token = token.lower()
                    if token != '' or not token in self.stopwords:
                        self.vocabulary.setdefault(token, 0)
                        self.vocabulary[token] += 1
                        counts.setdefault(token, 0)
                        counts[token] += 1
                        total += 1
            f.close()
        return(counts, total)



                    
    ################################################
    ##
    ## START OF TEXT CLASSIFIER 
    ##
    ##
    def classify(self, filename):
        results = {}
        for category in self.categories:
            results[category] = 0
        f = codecs.open(filename, 'r', 'iso8859-1')
        for line in f:
            tokens = line.split()
            for token in tokens:
                #print(token)
                token = token.strip('\'".,?:-').lower()
                if token in self.vocabulary:
                    for category in self.categories:
                        if self.prob[category][token] == 0:
                            print("%s %s" % (category, token))
                        results[category] += math.log(self.prob[category][token])
        f.close()
        results = list(results.items())
        results.sort(key=lambda tuple: tuple[1], reverse = True)
        # for debugging I can change this to give me the entire list
        return results[0][0]

    def testCategory(self, directory, category):
        files = os.listdir(directory)
        total = 0
        correct = 0
        for file in files:
            total += 1
            result = self.classify(directory + file)
            if result == category:
                correct += 1
        return (correct, total)

    def test(self, testdir):
        """Test all files in the test directory--that directory is organized into subdirectories--
        each subdir is a classification category"""
        categories = os.listdir(testdir)
        #filter out files that are not directories
        categories = [filename for filename in categories if os.path.isdir(testdir + filename)]
        correct = 0
        total = 0
        for category in categories:
            (catCorrect, catTotal) = self.testCategory(testdir + category + '/', category)
            correct += catCorrect
            total += catTotal
        print("Accuracy is  %f%%  (%i test instances)" % ((correct / total) * 100, total))


    ##
    ## END OF TEXT CLASSIFIER 
    ## 
    ##
    ################################################


if __name__ == '__main__':
    import time
    print('Bayes文本分类')
    start = time.clock()
    c = BayesText('20newsgroups/training/', 
                  '20newsgroups/stoplist.txt')
    print('%s %f' % ('loading数据时间：',time.clock()-start))
    print('Bayes正确率：')
    c.test('20newsgroups/test/')
