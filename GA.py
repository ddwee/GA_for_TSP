import random
import math
import csv


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



POP_N = 50  # リストに入れる経路の数
population = []  # [[経路],[経路],[経路]...[経路]]
cities_data = read_tspfile()
cities = []  # Cityオブジェクトを入れるリスト



class City:
    def __init__(self,num,X,Y):
        self.num = num
        self.X = X
        self.Y = Y



class Route:
    def __init__(self):
        self.distance = 0
        
        #　経路を作成(重複なしのランダム)
        self.citynums = random.sample(list(range(len(cities_data))),
                                      len(cities_data))
    
    
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
    
    def mutateN(self,num=random.randint(3,len(cities_data))):
        indices = random.sample(list(range(len(cities_data))),num)
        child = Route()
        child.citynums = self.citynums[:]
        
        # citynumsの2つの値を入れ替える  a,b = b,a
        for i in range(num-1):
            child.citynums[indices[i]],child.citynums[indices[(i+1)%num]] = \
            child.citynums[indices[(i+1)%num]], child.citynums[indices[i]] #↑継続文字
        return child
    
    def crossover(self,partner):
        child = Route()
        
        # 切り離す位置をランダムに選択
        index = random.randint(1,len(cities_data)-2)
        
        # indexの前までは自身の経路
        child.citynums = self.citynums[:index]
        
        # 1/2で経路を反転(突然変異)
        if random.random() < 0.5:
            child.citynums = child.citynums[::-1]
        
        #indexの後からはpartnerのリスト(index前の都市と重複しないように)
        notinslice = [X for X in partner.citynums if X not in child.citynums]
        
        #リストを合体
        child.citynums += notinslice
        return child


# citiesに読み込んだ座標を持つCityオブジェクトを入れる
for i in range(len(cities_data)):
    cities.append(City(cities_data[i][0],
                       cities_data[i][1],
                       cities_data[i][2]))  # num,X,Yの順


# populationに個体を追加
for i in range(POP_N):
    population.append(Route())

best = random.choice(population)  # 個体(経路)
record_distance = best.calc_distance()  # 距離
first = record_distance  # 1番優秀




gen = 0



with open('GA_result.csv','w') as fout:
    
    csvout = csv.writer(fout)
    result = []
    
    while True:
        print(record_distance)
        #print(best.citynums)
        population.sort(key=Route.calc_distance)
        population = population[:POP_N]  # 最長経路は淘汰
        
        distance1 = population[0].calc_distance()  # 最短経路
        
        if distance1 < record_distance:
            record_distance = distance1
            best = population[0]
        
        for i in range(len(cities_data)):
            A,B = random.sample(population,2)
            child = A.crossover(B)
            population.append(child)
        
        for i in range(3,len(cities_data)):
            if i < len(cities_data):
                best_from_new = best.mutateN()
                population.append(best_from_new)
        
        for i in range(3,len(cities_data)):
            if i < len(cities_data):
                other_from_new = random.choice(population)
                other_from_new = other_from_new.mutateN()
                population.append(other_from_new)
        gen+=1
        if gen == 1 or gen%100 == 0:
            data = []
            data.extend([gen,record_distance])
            result.append(data)
            if gen == 500:
                csvout.writerows(result)
                print(best.citynums)
                break



