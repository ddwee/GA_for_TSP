import random
import math
import csv
import copy



def read_tspfile():
    """
    tspファイルを読み込み、都市の座標(float型)を
    [[都市番号,X,Y],[...],...] の形で返す
    """
    def str2float(cities):
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
    
    with open("a280.tsp","r") as fin:
        data = [city.split(' ') for city in fin.read().splitlines()]
        remove_blank(data)
        cities_data = str2float(data)
    return cities_data



cities_data = read_tspfile()
population = []  # [[経路],[経路],[経路]...[経路]]
cities = []  # Cityオブジェクトを入れるリスト
CITIES_N = len(cities_data)  # 都市数



class City:
    def __init__(self,num,X,Y):
        self.num = num
        self.X = X
        self.Y = Y



class Route:
    def __init__(self):
        self.distance = 0
        
        #　経路を作成(重複なしのランダム)
        self.citynums = random.sample(list(range(CITIES_N)),CITIES_N)
    
    
    def calc_distance(self):
        """ citynumsリストの各都市間の距離の総和を求める """
        self.distance = 0
        for i,num in enumerate(self.citynums):
            """ 
            1つ前の都市との距離を計算
            i=0のとき、i-1は最後の都市(最後の都市からスタートへの距離)
            """
            self.distance += math.dist((cities[num].X,
                                        cities[num].Y),
                                       (cities[self.citynums[i-1]].X,
                                        cities[self.citynums[i-1]].Y))
        return self.distance



def copy_route(route):
    return copy.deepcopy(route)


# citiesに読み込んだ座標を持つCityオブジェクトを入れる
for i in range(CITIES_N):
    cities.append(City(cities_data[i][0],
                       cities_data[i][1],
                       cities_data[i][2]))  # num,X,Yの順


# populationに個体を追加
for i in range(2):
    population.append(Route())


population.sort(key=Route.calc_distance)
copy_test = copy_route(population[0].citynums)

print(population[0].citynums)
print(copy_test)