from math import sqrt

users = {"Angelica": {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0},
         "Bill":{"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0},
         "Chan": {"Blues Traveler": 5.0, "Broken Bells": 1.0, "Deadmau5": 1.0, "Norah Jones": 3.0, "Phoenix": 5, "Slightly Stoopid": 1.0},
         "Dan": {"Blues Traveler": 3.0, "Broken Bells": 4.0, "Deadmau5": 4.5, "Phoenix": 3.0, "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 2.0},
         "Hailey": {"Broken Bells": 4.0, "Deadmau5": 1.0, "Norah Jones": 4.0, "The Strokes": 4.0, "Vampire Weekend": 1.0},
         "Jordyn":  {"Broken Bells": 4.5, "Deadmau5": 4.0, "Norah Jones": 5.0, "Phoenix": 5.0, "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 4.0},
         "Sam": {"Blues Traveler": 5.0, "Broken Bells": 2.0, "Norah Jones": 3.0, "Phoenix": 5.0, "Slightly Stoopid": 4.0, "The Strokes": 5.0},
         "Veronica": {"Blues Traveler": 3.0, "Norah Jones": 5.0, "Phoenix": 4.0, "Slightly Stoopid": 2.5, "The Strokes": 3.0}
        }

class SimDistance:
    pass


def __init__(self):
    pass

## data preprocess to regularation
def preprocess_data():        
    pass

def pearson(user1,user2):
    sum_xy = 0
    sum_x = 0
    sum_y = 0
    sum_x2 = 0
    sum_y2 = 0
    n = 0
    for key in user1:
        if key in user2:
            n += 1
            x = user1[key]
            y = user2[key]
            sum_xy += x * y
            sum_x += x
            sum_y += y
            sum_x2 += pow(x, 2)
            sum_y2 += pow(y, 2)
    # now compute denominator
    denominator = sqrt(sum_x2 - pow(sum_x, 2) / n) * sqrt(sum_y2 - pow(sum_y, 2) / n)

    similairy = 0
    if denominator == 0:
        similairy = 0
    else:
        similairy = (sum_xy - (sum_x * sum_y) / n) / denominator

    print(similairy)    
    return similairy


def cosine_similarity(user1,user2):
    similairy = 0
    return similairy

def jaccard_similarity(user1,user2):
    pass


## to refactor:  distance class
def manhattan_distance(user1,user2):
    """Computes the Manhattan distance. Both user1 and user2 are dictionaries
       of the form {'The Strokes': 3.0, 'Slightly Stoopid': 2.5}"""
    distance = 0 ## there is a tricky. if there is no common key, distance must be -1 instead of 0
    common_flag = False
    for key in user1:
        if key in user2:
            """ mean there exists common key in user1 and user2 """
            distance += abs(user1[key]-user2[key])     
            common_flag = True
    if common_flag:
        return distance
    else:
        return -1

def euclidean_distance(user1,user2):
    distance = 0
    return distance

def minkowski_distance(user1,user2,r):
    distance = 0 
    common_flag = False
    for key in user1:
        if key in user2:
            """ mean there exists common key in user1 and user2 """
            distance += pow(abs(user1[key]-user2[key]),r)     
            common_flag = True
    if common_flag:
        return pow(distance,1/r)
    else:
        return -1

def compute_nearest_neighbor(username):
    """creates a sorted list of users based on their distance to username"""
    distances = []
    for user in users:
        if user != username:
            distance = manhattan_distance(users[user], users[username])
            distances.append((distance, user)) ## built-in function enumerate
    # sort based on distance -- closest first
    distances.sort()
    return distances[0]

""" recommend to the user by using method """
def recommend(username,method="manhattan"):
    ## find the nearest neighbor 
    neighbor = compute_nearest_neighbor(username)[1]

    ## 利用邻居用户进行推荐，在推荐的时候只须给user推荐不存在rating的item 
    recommendations = []
    neighbor_rating = users[neighbor]
    user_rating = users[username]

    for info in neighbor_rating:
        if not info in user_rating:
            recommendations.append((info, neighbor_rating[info]))

    recommendations.sort(key=lambda x:x[1],reverse = True)
    return recommendations

if __name__ == '__main__':
    # print(users)

    print(type(SimDistance))
    print(type(SimDistance()))
    
    print(recommend('Hailey'))
    print(recommend('Chan'))

    pearson(users['Angelica'], users['Bill' ])
    pearson(users['Angelica'], users['Hailey' ])
