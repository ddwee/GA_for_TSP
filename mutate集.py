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


#偶数個の都市を入れ替えられる
def mutate1(ind,num=random.randint(2,4)):
    indices = random.sample(list(range(CITIES_N)),num)
    print(indices)
    c = Route()
    c.citynums = ind.citynums[::]
    
    # citynumsの2つの値を入れ替える  a,b = b,a
    for i in range(num-1):
        c.citynums[indices[i]],c.citynums[indices[(i+1)%num]] = \
        c.citynums[indices[(i+1)%num]], c.citynums[indices[i]] #↑継続文字
    return c


#2つだけ入れ替える
def mutate2(ind):
    c = Route()
    c.citynums = ind.citynums[::]
    select_num = [i for i in range(len(c.citynums))]
    select_index = random.sample(select_num, 2)
    #print(select_index)
    
    a = c.citynums[select_index[0]]
    b = c.citynums[select_index[1]]

    c.citynums[select_index[1]] = a
    c.citynums[select_index[0]] = b
    return c


#多分2と同じ
def mutate3(ind):
    c = Route()
    c.citynums = ind.citynums[::]
    index1 = random.randint(0,CITIES_N-1)
    index2 = random.randint(0,CITIES_N-1)
    cop = c.citynums[index1]
    c.citynums[index1] = c.citynums[index2]
    c.citynums[index2] = cop
    return c


#逆位、ランダムに選択した区間について、遺伝子の順序を反転
def mutate4(ind):
    c = Route()
    c.citynums = ind.citynums[::]
    mini, maxi = sorted(random.sample(range(1,CITIES_N+1), 2))
    print(mini,maxi)
    a = c.citynums[mini:maxi+1]
    b = c.citynums[maxi:mini-1:-1]
    a = b
    #ind.citynums[mini:maxi+1] = ind.citynums[maxi:mini-1:-1]
    print(c.citynums[mini:maxi+1])
    print(c.citynums[maxi:mini-1:-1])
    c.citynums = c.citynums[0:mini] + a + c.citynums[maxi+1:]
    
    return c


def mutate5(ind):
    c = Route()
    c.citynums = ind.citynums[::]
    for i in range(CITIES_N):
        if random.random() < 1/CITIES_N:
            j = random.randrange(CITIES_N)
            # Swap
            c.citynums[i], c.citynums[j] = c.citynums[j], c.citynums[i]
    return c


#逆位はこっち使うべき、↑は0,CITIES_Nの組み合わせができない
def mutate6(ind):
    c = Route()
    c.citynums = ind.citynums[::]
    mini, maxi = sorted(random.sample(range(CITIES_N),2))
    #print(mini,maxi)
    c.citynums[mini:maxi+1] = c.citynums[mini:maxi+1][::-1]
    return c



# citiesに読み込んだ座標を持つCityオブジェクトを入れる
for i in range(CITIES_N):
    cities.append(City(cities_data[i][0],
                       cities_data[i][1],
                       cities_data[i][2]))  # num,X,Yの順


# populationに個体を追加
for i in range(2):
    population.append(Route())

# ランダムに2個取り出す
p1 = population.pop(random.randint(0, len(population)-1))
p2 = population.pop(random.randint(0, len(population)-1))

def has_duplicates(seq):
    return len(seq) != len(set(seq))

c= mutate6(p1)
print(p1.citynums)
print(c.citynums,len(c.citynums))
print(p1.citynums == c.citynums)
print(has_duplicates(c.citynums))
