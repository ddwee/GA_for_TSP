import random
import math
import csv
import copy
import time
import numpy as np



def read_tspfile():
    """
    tspファイルを読み込み、都市の座標(float型)を
    [[都市番号,X,Y],[...],...] の形で返す
    """
    def str2float(cities):
        data = [0]*len(cities)
        for i in range(len(cities)):
            city = [0]*len(cities[i])
            data[i] = city
            try:
                for j in range(len(cities[i])):
                    data[i][j] = float(cities[i][j])
            except:
                data[i]=None
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


def mutate(ind):
    c = Route()
    c.citynums = ind.citynums[::]
    mini, maxi = sorted(random.sample(range(CITIES_N),2))
    #print(mini,maxi)
    c.citynums[mini:maxi+1] = c.citynums[mini:maxi+1][::-1]
    return c


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


def crossover(p1, p2):
    size = CITIES_N

    # Choose random start/end position for crossover
    c1, c2 = [-1] * size, [-1] * size
    start, end = sorted([random.randrange(size) for _ in range(2)])

    # Replicate mum's sequence for alice, dad's sequence for bob
    c1_inherited = []
    c2_inherited = []
    for i in range(start, end + 1):
        c1[i] = p1.citynums[i]
        c2[i] = p2.citynums[i]
        c1_inherited.append(p1.citynums[i])
        c2_inherited.append(p2.citynums[i])

    #Fill the remaining position with the other parents' entries
    current_p1_position, current_p2_position = 0, 0

    fixed_pos = list(range(start, end + 1))       
    i = 0
    while i < size:
        if i in fixed_pos:
            i += 1
            continue

        test_c1 = c1[i]
        if test_c1==-1: #to be filled
            p2_trait = p2.citynums[current_p2_position]
            while p2_trait in c1_inherited:
                current_p2_position += 1
                p2_trait = p2.citynums[current_p2_position]
            c1[i] = p2_trait
            c1_inherited.append(p2_trait)
            
        test_c2 = c2[i]
        if test_c2==-1: #to be filled
            p1_trait = p1.citynums[current_p1_position]
            while p1_trait in c2_inherited:
                current_p1_position += 1
                p1_trait = p1.citynums[current_p1_position]
            c2[i] = p1_trait
            c2_inherited.append(p1_trait)

        #repeat block for bob and mom
        i +=1
    ind1 = Route()
    ind2 = Route()
    ind1.citynums = c1
    ind2.citynums = c2
    
    mutate_probablity = np.random.rand()
    if mutate_probablity > 0.5:
        if mutate_probablity < 0.95:
            ind1 = mutate(ind1)
        else:
            ind1 = mutate2(ind1)
    else:
        if mutate_probablity > 0.05:
            ind2 = mutate(ind2)
        else:
            ind2 = mutate2(ind2)

    return ind1, ind2

def pfga():

    # 2未満なら追加。これだけだとランダムに2こ取り出す動作でエラー吐く。別途初期集団は作っておく
    if len(population) < 2:
        population.append(Route())

    # ランダムに2個取り出す
    p1 = population.pop(random.randint(0, len(population)-1))
    p2 = population.pop(random.randint(0, len(population)-1))

    # 子を作成
    c1,c2 = crossover(p1,p2)

    if p1.calc_distance() < p2.calc_distance():
        p_good = p1  # 短い経路(優秀)
        p_bad = p2  # 長い経路(淘汰される)
    else:
        p_good = p2
        p_bad = p1
    if c1.calc_distance() < c2.calc_distance():
        c_good = c1
        c_bad = c2
    else:
        c_good = c2
        c_bad = c1

    if c_bad.calc_distance() <= p_good.calc_distance():
        # 子2個体がともに親の2個体より良かった場合
        # 子2個体及び適応度の良かった方の親個体計3個体が局所集団に戻り、局所集団数は1増加する。
        population.append(c1)
        population.append(c2)
        population.append(p_good)
    elif p_bad.calc_distance() <= c_good.calc_distance():
        # 子2個体がともに親の2個体より悪かった場合
        # 親2個体のうち良かった方のみが局所集団に戻り、局所集団数は1減少する。
        population.append(p_good)
    elif p_good.calc_distance() <= c_good.calc_distance() and p_bad.calc_distance() >= c_good.calc_distance():
        # 親2個体のうちどちらか一方のみが子2個体より良かった場合
        # 親2個体のうち良かった方と子2個体のうち良かった方が局所集団に戻り、局所集団数は変化しない。
        population.append(c_good)
        population.append(p_good)
    elif c_good.calc_distance() <= p_good.calc_distance() and c_bad.calc_distance() >= p_good.calc_distance():
        # 子2個体のうちどちらか一方のみが親2個体より良かった場合
        # 子2個体のうち良かった方のみが局所集団に戻り、全探索空間からランダムに1個体選んで局所集団に追加する。局所集団数は変化しない。
        population.append(c_good)
        population.append(Route())
    else:
        raise ValueError("not comming")


# 時間計測開始
start = time.perf_counter()


# citiesに読み込んだ座標を持つCityオブジェクトを入れる
for i in range(CITIES_N):
    cities.append(City(cities_data[i][0],
                       cities_data[i][1],
                       cities_data[i][2]))  # num,X,Yの順


# populationに個体を追加
for i in range(2):
    population.append(Route())
    

best = random.choice(population)  # 個体(経路)
record_distance = best.calc_distance()  # 距離
gen = 0  # 世代カウント用
a280 = 2586.76964756316  # a280の最適解
att48 = 33523.7085074355  # att48の最適解
kroA100 = 21285.44318157108


with open('普通のPfGA_result.csv','w') as fout:
    
    csvout = csv.writer(fout)
    result = []
    
    while True:
        population.sort(key=Route.calc_distance)
        distance1 = population[0].calc_distance()  # 最短経路
        
        
        if distance1 < record_distance:
            print(record_distance)
            record_distance = distance1
            best = population[0]  # 最短経路を更新
            data = []
            data.extend([gen,record_distance])
            result.append(data)
            
        pfga()
        
        
        gen+=1
        # 終了条件：誤差率が--になるまで
        if (record_distance - a280)/record_distance <= 0.15:
            csvout.writerows(result)
            print(best.citynums)
            
            
            # 時間計測終了(秒)
            end = time.perf_counter()
            tim = end - start
            print(tim)
            break
        


