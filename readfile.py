"""

"""


def str2float(cities):
    """ [[str,str],[str]] → [[float,float],[float]] """
    
    data = [[0]]*len(cities)
    
    for i in range(len(cities)):
        city = [0]*len(cities[i])
        data[i] = city
        try:
            for j in range(len(cities[i])):
                data[i][j] = float(cities[i][j])
        except:
            data[i]*=0
            continue
    
    data2 = list(filter(None,data))
    
    return data2
    

def remove_blank(cities):
    for i in range(len(cities)):
        for j in range(len(cities[i])):
            try:
                cities[i].remove('')
            except:
                continue
    

with open("ali535.tsp","r") as fin:
    data = [city.split(' ') for city in fin.read().splitlines()]
    
    remove_blank(data)
    cities = str2float(data)

    
print(cities,len(cities))


