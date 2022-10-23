"""
tsplibの最適解ファイルを読み込み、最短経路長を計算する
.tourファイルの末尾、-1を削除しておくこと

----
計算した最適解一覧

a280  2586.769647563161

att48  33523.70850743559

gr666  3952.5357015796094

kroA100  21285.44318157108

berlin52  7544.365901904087

ch150  6532.280933145756
----

"""





import random
import math



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
    
    with open("berlin52.tsp","r") as fin:
        data = [city.split(' ') for city in fin.read().splitlines()]
        remove_blank(data)
        cities_data = str2float(data)
    return cities_data


def read_tourfile():
    def str2float(cities):
        data = [0]*len(cities)
        for i in range(len(cities)):
            city = [0]*len(cities[i])
            data[i] = city
            try:
                for j in range(len(cities[i])):
                    data[i][j] = int(cities[i][j])
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
    
    with open("berlin52.opt.tour","r") as fin:
        data = [city.split(' ') for city in fin.read().splitlines()]
        remove_blank(data)
        tour_data = str2float(data)
    return tour_data


cities = []  # Cityオブジェクトを入れるリスト
cities_data = read_tspfile()
tour_data = read_tourfile()
tour = []
for i in range(len(tour_data)):
    tour.extend(tour_data[i])


class City:
    def __init__(self,num,X,Y):
        self.num = num
        self.X = X
        self.Y = Y



class Route:
    def __init__(self):
        self.distance = 0
        self.citynums = random.sample(list(range(len(cities_data)+1)),
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


# citiesに読み込んだ座標を持つCityオブジェクトを入れる
for i in range(len(cities_data)):
    cities.append(City(cities_data[i][0],
                       cities_data[i][1],
                       cities_data[i][2]))  # num,X,Yの順


def minus1(x):
        y = x-1
        return y


test = Route()
tour2 = list(map(minus1,tour))
test.citynums = tour2

print(cities_data)
print(tour2)
print(test.calc_distance())