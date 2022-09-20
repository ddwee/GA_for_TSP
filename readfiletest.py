import csv








with open("a280.tsp","r") as fin:
    
    # ヘッダーを読み捨てる
    for i in range(6):
        next(csv.reader(fin))
    
    #['','','1','288','149']みたいなリストが出来上がる
    cities = [data.split(' ') for data in fin.readline().splitlines()]
    
    # 整形のためにあるスペースを削除
    for i in range(2):
        if cities[0][0] == '':
            del cities[0][0]
        else:
            break
    
    # 各要素を数値に変換
    for i in range(3):
        cities[0][i] = int(cities[0][i])
    
print(cities[0],type(cities[0][2]),len(cities[0]))







