import codecs 
from math import sqrt


""" users2 ds represent the slope one algorithm """
users2 = {"Amy": {"Taylor Swift": 4, "PSY": 3, "Whitney Houston": 4},
          "Ben": {"Taylor Swift": 5, "PSY": 2},
          "Clara": {"PSY": 3.5, "Whitney Houston": 4},
          "Daisy": {"Taylor Swift": 5, "Whitney Houston": 3}}

users = {"Angelica": {"Blues Traveler": 3.5, "Broken Bells": 2.0,
                      "Norah Jones": 4.5, "Phoenix": 5.0,
                      "Slightly Stoopid": 1.5, "The Strokes": 2.5,
                      "Vampire Weekend": 2.0},
         "Bill":{"Blues Traveler": 2.0, "Broken Bells": 3.5,
                 "Deadmau5": 4.0, "Phoenix": 2.0,
                 "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0},
         "Chan": {"Blues Traveler": 5.0, "Broken Bells": 1.0,
                  "Deadmau5": 1.0, "Norah Jones": 3.0,
                  "Phoenix": 5, "Slightly Stoopid": 1.0},
         "Dan": {"Blues Traveler": 3.0, "Broken Bells": 4.0,
                 "Deadmau5": 4.5, "Phoenix": 3.0,
                 "Slightly Stoopid": 4.5, "The Strokes": 4.0,
                 "Vampire Weekend": 2.0},
         "Hailey": {"Broken Bells": 4.0, "Deadmau5": 1.0,
                    "Norah Jones": 4.0, "The Strokes": 4.0,
                    "Vampire Weekend": 1.0},
         "Jordyn":  {"Broken Bells": 4.5, "Deadmau5": 4.0,
                     "Norah Jones": 5.0, "Phoenix": 5.0,
                     "Slightly Stoopid": 4.5, "The Strokes": 4.0,
                     "Vampire Weekend": 4.0},
         "Sam": {"Blues Traveler": 5.0, "Broken Bells": 2.0,
                 "Norah Jones": 3.0, "Phoenix": 5.0,
                 "Slightly Stoopid": 4.0, "The Strokes": 5.0},
         "Veronica": {"Blues Traveler": 3.0, "Norah Jones": 5.0,
                      "Phoenix": 4.0, "Slightly Stoopid": 2.5,
                      "The Strokes": 3.0}
        }



class recommender:

   def __init__(self, data, k=1, metric='pearson', n=5):
      """ initialize recommender
      currently, if data is dictionary the recommender is initialized
      to it.
      For all other data types of data, no initialization occurs
      k is the k value for k nearest neighbor
      metric is which distance formula to use
      n is the maximum number of recommendations to make"""
      self.k = k
      self.n = n
      self.username2id = {}
      self.userid2name = {}
      self.productid2name = {}
      #
      # The following two variables are used for Slope One
      # 
      self.frequencies = {} # card(Si,j)
      self.deviations = {} # deviration
      # for some reason I want to save the name of the metric
      self.metric = metric
      if self.metric == 'pearson':
         self.fn = self.pearson
      #
      # if data is dictionary set recommender data to it
      #
      if type(data).__name__ == 'dict':
         self.data = data

   def convertProductID2name(self, id):
      """Given product id number return product name"""
      if id in self.productid2name:
         return self.productid2name[id]
      else:
         return id


   # no use
   def userRatings(self, id, n):
      """Return n top ratings for user with id"""
      print ("Ratings for " + self.userid2name[id])
      ratings = self.data[id]
      print(len(ratings))
      ratings = list(ratings.items())[:n]
      ratings = [(self.convertProductID2name(k), v)
                 for (k, v) in ratings]
      # finally sort and return
      ratings.sort(key=lambda artistTuple: artistTuple[1],
                   reverse = True)      
      for rating in ratings:
         print("%s\t%i" % (rating[0], rating[1]))


   def showUserTopItems(self, user, n):
      """ show top n items for user"""
      items = list(self.data[user].items())
      items.sort(key=lambda itemTuple: itemTuple[1], reverse=True)
      for i in range(n):
         print("%s\t%i" % (self.convertProductID2name(items[i][0]),
                           items[i][1]))
            
   def loadMovieLens(self, path=''):
      self.data = {}
      #
      # first load movie ratings
      #
      i = 0
      #
      # First load movie ratings into self.data
      #
      ## use the with 
      #f = codecs.open(path + "u.data", 'r', 'utf8')
      f = codecs.open(path + "u.data", 'r', 'ascii')
      #  f = open(path + "u.data")
      for line in f:
         i += 1
         #separate line into fields
         fields = line.split('\t')
         user = fields[0]
         movie = fields[1]
         rating = int(fields[2].strip().strip('"'))
         if user in self.data:
            currentRatings = self.data[user]
         else:
            currentRatings = {}
         currentRatings[movie] = rating
         self.data[user] = currentRatings         
      f.close()
            
      #
      # Now load movie into self.productid2name
      # the file u.item contains movie id, title, release date among
      # other fields
      #
      #f = codecs.open(path + "u.item", 'r', 'utf8')
      f = codecs.open(path + "u.item", 'r', 'iso8859-1', 'ignore')
      #f = open(path + "u.item")
      for line in f:
         i += 1
         #separate line into fields
         fields = line.split('|')
         mid = fields[0].strip()
         title = fields[1].strip()
         self.productid2name[mid] = title
      f.close()
      #
      #  Now load user info into both self.userid2name
      #  and self.username2id
      #
      #f = codecs.open(path + "u.user", 'r', 'utf8')
      f = open(path + "u.user")
      for line in f:
         i += 1
         fields = line.split('|')
         userid = fields[0].strip('"')
         self.userid2name[userid] = line
         self.username2id[line] = userid
      f.close()
      print(i)
                

   """计算slope one方差 """
   def computeDeviations(self):
      # for each person in the data:
      #    get their ratings
      for ratings in self.data.values():
         # for each item & rating in that set of ratings:
         for (item, rating) in ratings.items():
            self.frequencies.setdefault(item, {})
            self.deviations.setdefault(item, {})                    
            # for each item2 & rating2 in that set of ratings:
            for (item2, rating2) in ratings.items():
               if item != item2:
                  # add the difference between the ratings to our
                  # computation
                  ## setdefault函数主要获取信息，如果获取不到的时候就按照他的参数设置该值
                  self.frequencies[item].setdefault(item2, 0)
                  self.deviations[item].setdefault(item2, 0.0)
                  self.frequencies[item][item2] += 1
                  self.deviations[item][item2] += rating - rating2

      ## self.deviations[“Taylor Swift”][“PSY”]
      for (item, ratings) in self.deviations.items():
         for item2 in ratings:
            ratings[item2] /= self.frequencies[item][item2]


   def slopeOneRecommendations(self, userRatings):
      recommendations = {}
      frequencies = {}
      # for every item and rating in the user's recommendations
      for (userItem, userRating) in userRatings.items():
         # for every item in our dataset that the user didn't rate
         for (diffItem, diffRatings) in self.deviations.items():
            if diffItem not in userRatings and \
               userItem in self.deviations[diffItem]:
               freq = self.frequencies[diffItem][userItem]

               recommendations.setdefault(diffItem, 0.0)
               frequencies.setdefault(diffItem, 0)
               # add to the running sum representing the numerator
               # of the formula
               recommendations[diffItem] += (diffRatings[userItem] +
                                             userRating) * freq
               # keep a running sum of the frequency of diffitem
               frequencies[diffItem] += freq
      recommendations =  [(self.convertProductID2name(k),
                           v / frequencies[k])
                          for (k, v) in recommendations.items()]
      # finally sort and return
      recommendations.sort(key=lambda artistTuple: artistTuple[1],
                           reverse = True)
      # I am only going to return the first 50 recommendations
      return recommendations[:50]
        
   def pearson(self, rating1, rating2):
      sum_xy = 0
      sum_x = 0
      sum_y = 0
      sum_x2 = 0
      sum_y2 = 0
      n = 0
      for key in rating1:
         if key in rating2:
            n += 1
            x = rating1[key]
            y = rating2[key]
            sum_xy += x * y
            sum_x += x
            sum_y += y
            sum_x2 += pow(x, 2)
            sum_y2 += pow(y, 2)
      if n == 0:
         return 0
      # now compute denominator
      denominator = sqrt(sum_x2 - pow(sum_x, 2) / n) * \
                    sqrt(sum_y2 - pow(sum_y, 2) / n)
      if denominator == 0:
         return 0
      else:
         return (sum_xy - (sum_x * sum_y) / n) / denominator


if __name__=="__main__":
   import time
      
   # 测试数据
   print('测试数据结果：')
   data={"a":2,"b":4}
   li = list(data.items()).sort(key=lambda x:x[1],reverse = True )
   print(li)
   lst = [(k,v) for (k,v) in data.items()]
   print(lst)
   print(lst[:1])
   
   # 使用user2数据，计算slope one
   print('user2数据结果：')
   r = recommender(users2)
   r.computeDeviations()
   print(r.deviations)
   g = users2['Ben']
   print(r.slopeOneRecommendations(g))

   # 使用movie数据，计算slope one
   print('movie数据结果：')
   r = recommender(0) 
   r.loadMovieLens('MovieLens/ml-100k/')
   print(list(r.data.items())[0])# 显示data的数据格式
   ## r.showUserTopItems('1',50)
   print('开始运行slope one 算法：')
   start = time.clock()
   r.computeDeviations()
   ## print(list(r.deviations.items())[0])# 显示deviations的数据格式
   print(r.slopeOneRecommendations(r.data['1']))
   print('%s%f' % ('slope one算法运行时间：',time.clock()-start))
