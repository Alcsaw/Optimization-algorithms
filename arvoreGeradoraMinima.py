import csv

path=[]
visitados=[]
pendentes=[]
interacoes=[]

def remove_repetidos(lista):
    l = []
    for i in lista:
        if i not in l:
            l.append(i)
    l.sort()
    return l

def read_file():
    global path
    global visitados
    global pendentes
    with open('arvore.csv', 'r') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            path.append(Data(row[0], row[1], row[2]))
            path.append(Data(row[1], row[0], row[2]))
    csvFile.close()

    for i in range(len(path)):
        pendentes.append(path[i].nodeA)
        pendentes.append(path[i].nodeB)
    pendentes = remove_repetidos(pendentes)
    #print (pendentes)

def interacao():
    global path
    global visitados
    global pendentes
    global interacoes
    distance = 10000000
    for i in range (len(visitados)):
        for x in range (len(path)):
            if visitados[i] == path[x].nodeA:
                if path[x].nodeB in pendentes:               
                    if int(path[x].value) < distance:
                        distance = int(path[x].value)
                        indice = x
    visitados.append(path[indice].nodeB)
    #print (visitados)
    pendentes.remove(path[indice].nodeB)
    #print (pendentes)
    interacoes.append(Data(path[indice].nodeA, path[indice].nodeB, path[indice].value))

class Data(object):
    def __init__(self, nodeA, nodeB, value):
        self.nodeA = nodeA
        self.nodeB = nodeB
        self.value = value

def main():
    read_file()
    inicio = '1'
    visitados.append(inicio)
    pendentes.remove(inicio)
    finalDistance=0
    while len(pendentes)>0:
        interacao()

    for i in range (len(interacoes)):
        finalDistance = finalDistance + int(interacoes[i].value)
    print(finalDistance)
          
if __name__ == "__main__":
    main()


