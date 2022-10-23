import numpy as np
import random
import math
import csv
import copy
import time



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
    
    print(fragment_c1,len(fragment_c1))
    print(fragment_c2,len(fragment_c2))
    
    notinslice_c1 = [X for X in c2.citynums if X not in fragment_c1]
    notinslice_c2 = [X for X in c1.citynums if X not in fragment_c2]
    
    print(notinslice_c1,len(notinslice_c1))
    print(notinslice_c2,len(notinslice_c2))
    
    #リストを合体
    a = fragment_c1 + notinslice_c1
    b = fragment_c2 + notinslice_c2
    c1.citynums = a
    c2.citynums = b
    
    return c1,c2


#経路被るから未完成
def TwoPoint(ind1, ind2):
    c1 = copy_route(ind1)
    c2 = copy_route(ind2)
    size = CITIES_N
    cxpoint1 = random.randint(1, size)
    cxpoint2 = random.randint(1, size - 1)
    #print(cxpoint1,cxpoint2)
    if cxpoint2 >= cxpoint1:
        cxpoint2 += 1
    else:  # Swap the two cx points
        cxpoint1, cxpoint2 = cxpoint2, cxpoint1

    c1.citynums[cxpoint1:cxpoint2], c2.citynums[cxpoint1:cxpoint2] \
        = c2.citynums[cxpoint1:cxpoint2], c1.citynums[cxpoint1:cxpoint2]

    return c1, c2


def unknown_crossover(p1, p2, number_of_cities = CITIES_N):
    child1 = Route()
    child2 = Route()
    chk1 = {}
    chk2 = {}
    for i in range(number_of_cities):
        chk1[i] = 0
        chk2[i] = 0
    citynums1 = [-1] * number_of_cities
    citynums2 = [-1] * number_of_cities
    
    y1 = 1
    y2 = 1
    for x in range(len(p1.citynums)):
        if x % 2 == 0:
            citynums1[x] = p1.citynums[x]
            chk1[p1.citynums[x]] = 1
            
            citynums2[x] = p2.citynums[x]
            chk2[p2.citynums[x]] = 1
    
    for x in range(len(p2.citynums)):
        if chk1[p2.citynums[x]] == 0:
            citynums1[y1] = p2.citynums[x]
            y1 += 2
        if chk2[p1.citynums[x]] == 0:
            citynums2[y2] = p1.citynums[x]
            y2 += 2
        
    child1.citynums = citynums1
    child2.citynums = citynums2
    return child1,child2


#未完
def PMX_crossover(parent1, parent2):
    rng = np.random.default_rng()

    cutoff_1, cutoff_2 = np.sort(rng.choice(np.arange(len(parent1.citynums)+1), size=2, replace=False))

    def PMX_one_offspring(p1, p2):
        offspring = [0]*CITIES_N

        # Copy the mapping section (middle) from parent1
        offspring[cutoff_1:cutoff_2] = p1.citynums[cutoff_1:cutoff_2]

        # copy the rest from parent2 (provided it's not already there
        for i in np.concatenate([np.arange(0,cutoff_1), np.arange(cutoff_2,len(p1.citynums))]):
            candidate = p2.citynums[i]
            while candidate in p1.citynums[cutoff_1:cutoff_2]: # allows for several successive mappings
                #print(f"Candidate {candidate} not valid in position {i}") # DEBUGONLY
                candidate = p2.citynums[np.where(p1.citynums == candidate)[0][0]]
            offspring[i] = candidate
        return offspring

    offspring1 = PMX_one_offspring(parent1, parent2)
    offspring2 = PMX_one_offspring(parent2, parent1)

    return offspring1, offspring2
    
#一様順序交叉
def ordered_crossover(p1, p2):
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

    print(c1, c2)
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

    return ind1, ind2


#循環交叉
def CX(p1,p2):
    cycles = [-1]*CITIES_N
    cycle_no = 1
    cyclestart = (i for i,v in enumerate(cycles) if v < 0)

    for pos in cyclestart:
        while cycles[pos] < 0:
            cycles[pos] = cycle_no
            pos = p1.citynums.index(p2.citynums[pos])

        cycle_no += 1

    c1 = [p1.citynums[i] if n%2 else p2.citynums[i] for i,n in enumerate(cycles)]
    c2 = [p2.citynums[i] if n%2 else p1.citynums[i] for i,n in enumerate(cycles)]
    ind1 = Route()
    ind2 = Route()
    ind1.citynums = c1
    ind2.citynums = c2
    return ind1, ind2


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

start = time.perf_counter()


c1,c2 = CX(p1,p2)


end = time.perf_counter()
tim = end - start
print(tim)


# リストの要素に重複があればTrueを返す
def has_duplicates(seq):
    return len(seq) != len(set(seq))

print(p1.citynums)
print()
print(p2.citynums)
print()
print(c1.citynums)
print()
print(c2.citynums)
print()
print(has_duplicates(c2.citynums),has_duplicates(c1.citynums))