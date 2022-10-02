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
    
    with open("att48.tsp","r") as fin:
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


def mutate(c1,c2):
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



def crossover(p1, p2):
    # 子の遺伝子情報
    c1 = copy_route(p1)
    c2 = copy_route(p2)
    # 切り離す位置をランダムに選択
    index = random.randint(1,len(cities_data)-2)
    # indexの前までは自身の経路
    #indexの後からは相方のリスト(index前の都市と重複しないように)
    fragment_c1 = c1.citynums[:index]
    fragment_c2 = c2.citynums[:index]
    # どっちかを反転
    if random.random() > 0.5:
        fragment_c1 = c1.citynums[::-1]
    else:
        fragment_c2 = c2.citynums[::-1]
    
    notinslice_c1 = [X for X in fragment_c2 if X not in c1.citynums]
    notinslice_c2 = [X for X in fragment_c1 if X not in c2.citynums]
    #リストを合体
    c1.citynums += notinslice_c1
    c2.citynums += notinslice_c2
    
    mutated_c1, mutated_c2 = mutate(c1,c2)
    
    return mutated_c1,mutated_c2


# citiesに読み込んだ座標を持つCityオブジェクトを入れる
for i in range(CITIES_N):
    cities.append(City(cities_data[i][0],
                       cities_data[i][1],
                       cities_data[i][2]))  # num,X,Yの順


# populationに個体を追加
for i in range(2):
    population.append(Route())


# リストの要素に重複があればTrueを返す
def has_duplicates(seq):
    return len(seq) != len(set(seq))


#print(population[0].citynums,population[1].citynums)
c1,c2 = crossover(population[0],population[1])
print(c1.citynums,c2.citynums)
print(has_duplicates(c1.citynums),has_duplicates(c2.citynums))
print(len(c1.citynums),len(c2.citynums))