import asyncio
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


async def copy_route(route):
    return copy.deepcopy(route)


async def mutate(ind,num=random.randint(1,2)):
    indices = random.sample(list(range(CITIES_N)),num)
    c = Route()
    c.citynums = ind.citynums[:]
    
    # citynumsの2つの値を入れ替える  a,b = b,a
    for i in range(num-1):
        c.citynums[indices[i]],c.citynums[indices[(i+1)%num]] = \
        c.citynums[indices[(i+1)%num]], c.citynums[indices[i]] #↑継続文字
    return c


async def crossover_2(p1, p2):
    # 子の遺伝子情報
    c1 = await copy_route(p1)
    c2 = await copy_route(p2)
    # 切り離す位置をランダムに選択
    index = random.randint(1,len(cities_data)-2)
    # indexの前までは自身の経路
    #indexの後からは相方のリスト(index前の都市と重複しないように)
    fragment_c1 = c1.citynums[:index]
    fragment_c2 = c2.citynums[:index]
    
    # 経路を反転(突然変異)
    if random.random() < 0.001:
        fragment_c1 = c1.citynums[::-1]
        fragment_c2 = c2.citynums[::-1]
    
    notinslice_c1 = [X for X in fragment_c2 if X not in c1.citynums]
    notinslice_c2 = [X for X in fragment_c1 if X not in c2.citynums]
    #リストを合体
    c1.citynums += notinslice_c1
    c2.citynums += notinslice_c2
    
    if random.random() > 0.5:
        c1 = await mutate(c1)
    else:
        c2 = await mutate(c2)
    
    return c1,c2


async def crossover_1(p1):
    # 子の遺伝子情報
    c1 = await copy_route(p1)
    c2 = Route()
    # 切り離す位置をランダムに選択
    index = random.randint(1,len(cities_data)-2)
    # indexの前までは自身の経路
    #indexの後からは相方のリスト(index前の都市と重複しないように)
    fragment_c1 = c1.citynums[:index]
    fragment_c2 = c2.citynums[:index]
    
    # 経路を反転(突然変異)
    if random.random() < 0.001:
        fragment_c1 = c1.citynums[::-1]
        fragment_c2 = c2.citynums[::-1]
    
    notinslice_c1 = [X for X in fragment_c2 if X not in c1.citynums]
    notinslice_c2 = [X for X in fragment_c1 if X not in c2.citynums]
    #リストを合体
    c1.citynums += notinslice_c1
    c2.citynums += notinslice_c2
    
    if random.random() > 0.5:
        c1 = await mutate(c1)
    else:
        c2 = await mutate(c2)
    
    return c1,c2


async def crossover_0():
    # 子の遺伝子情報
    c1 = Route()
    c2 = Route()
    # 切り離す位置をランダムに選択
    index = random.randint(1,len(cities_data)-2)
    # indexの前までは自身の経路
    #indexの後からは相方のリスト(index前の都市と重複しないように)
    fragment_c1 = c1.citynums[:index]
    fragment_c2 = c2.citynums[:index]
    
    # 経路を反転(突然変異)
    if random.random() < 0.001:
        fragment_c1 = c1.citynums[::-1]
        fragment_c2 = c2.citynums[::-1]
    
    notinslice_c1 = [X for X in fragment_c2 if X not in c1.citynums]
    notinslice_c2 = [X for X in fragment_c1 if X not in c2.citynums]
    #リストを合体
    c1.citynums += notinslice_c1
    c2.citynums += notinslice_c2
    
    if random.random() > 0.5:
        c1 = await mutate(c1)
    else:
        c2 = await mutate(c2)
    
    return c1,c2


async def pfga():

    # 2未満なら追加。
    if len(population) < 2:
        try:
            individual1, individual2 = await crossover_1(population[0])
            population.append(individual1)
            population.append(individual2)
        except:
            individual1, individual2 = await crossover_0()
            population.append(individual1)
            population.append(individual2)

    # ランダムに2個取り出す
    p1 = population.pop(random.randint(0, len(population)-1))
    p2 = population.pop(random.randint(0, len(population)-1))

    # 子を作成
    c1, c2 = await crossover_2(p1,p2)

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
        # 子2個体のうち良かった方のみが局所集団に戻る
        population.append(c_good)
        population.append(Route())
        #await pfga()
    else:
        raise ValueError("not comming")


async def main():
    await asyncio.gather(
        pfga(),
        pfga(),
        pfga(),
        pfga(),
        )


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






with open('multiple_PfGA_result.csv','w') as fout:
    
    csvout = csv.writer(fout)
    result = []
    
    while True:
        population.sort(key=Route.calc_distance)
        distance1 = population[0].calc_distance()  # 最短経路
        population = population[:4]  # 最長経路は淘汰
        
        if distance1 < record_distance:
            record_distance = distance1
            best = population[0]  # 最短経路を更新
            print(record_distance)
            data = []
            data.extend([gen,record_distance])
            result.append(data)
        
        asyncio.run(main())
        
        gen+=1
        # 終了条件：誤差率が--になるまで
        if (record_distance - a280)/record_distance <= 0.65:
            csvout.writerows(result)
            print(best.citynums)
            # 時間計測終了(秒)
            end = time.perf_counter()
            tim = end - start
            print(tim)
            break



    
            
            
