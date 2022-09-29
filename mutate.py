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


# 一様交叉、テストのため確率は100%。pfgaの場合は最初のifいらない
def mutate(c1,c2,mutate_rate=1):
    if random.random() < mutate_rate:
        if random.random() > 0.5:
            select_num = [i for i in range(len(c1.citynums))]
            select_index = random.sample(select_num, 2)
            
            a = c1.citynums[select_index[0]]
            b = c1.citynums[select_index[1]]
            c1.citynums[select_index[1]] = a
            c1.citynums[select_index[0]] = b

        else:
            select_num = [i for i in range(len(c2.citynums))]
            select_index = random.sample(select_num, 2)
            
            a = c2.citynums[select_index[0]]
            b = c2.citynums[select_index[1]]
            c2.citynums[select_index[1]] = a
            c2.citynums[select_index[0]] = b
    
    return c1,c2



# citiesに読み込んだ座標を持つCityオブジェクトを入れる
for i in range(CITIES_N):
    cities.append(City(cities_data[i][0],
                       cities_data[i][1],
                       cities_data[i][2]))  # num,X,Yの順


# populationに個体を追加
for i in range(2):
    population.append(Route())



print(population[0].calc_distance(),population[1].calc_distance())
c1,c2 = mutate(population[0],population[1])
print(c1.calc_distance(),c2.calc_distance())
