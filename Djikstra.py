import csv

path=[]
it=[]
nodes=[]
contTemp=0
caminho=[]

class Data(object):
    def __init__(self, origin, destination, distance):
        self.origin = origin
        self.destination = destination
        self.distance = distance

class Interacao(object):
    def __init__(self, node, distance, origin, status):
        self.node = node
        self.distance = distance
        self.origin = origin
        self.status = status

def remove_repetidos(lista):
    l = []
    for i in lista:
        if i not in l:
            l.append(i)
    l.sort()
    return l

def read_file():
    global path
    global nodes
    with open('djikstra.csv', 'r') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            path.append(Data(row[0], row[1], row[2]))
    csvFile.close()

    for i in range(len(path)): #gera lista de todos os nós
        nodes.append(path[i].origin)
        nodes.append(path[i].destination)
    nodes = remove_repetidos(nodes)

def iteracao(ref):
    global it
    global path
    dist = 0
    for i in range (len(path)):
        if path[i].origin == str(ref):
            for x in range (len(it)):
                if it[x].node == str(ref):
                    dist = int(it[x].distance)
            dist = int(path[i].distance) + dist
            it.append(Interacao(path[i].destination, dist, path[i].origin, 0))


def define_permanente():
    global it
    controle = 1000000
    indice = 0
    referencia = 0
    global contTemp
    contTemp = contTemp + 1
    for i in range (len(it)):
        if int(it[i].distance) < controle and it[i].status==0:
            controle = int(it[i].distance)
            novoPermanenteOrigem = it[i].node
            novoPermanenteDist = int(it[i].distance)
    for x in range (len(it)): #necessario para casos onde dois caminhos possiveis de mesma distancia existem
        if it[x].node == novoPermanenteOrigem and it[x].distance == novoPermanenteDist:
            it[x].status = 1
            referencia = it[x].node
    if referencia == '100':
        for x in range (len(it)):
            if(it[x].status!='1'):
                referencia = it[x].node
    return referencia

def trata_duplicatas():
    global it
    aux=[]
    for i in range (len(nodes)):
        controle = 1000000
        for x in range (len(it)):
            if nodes[i] == it[x].node:
                if int(it[x].distance) < controle:
                    controle = int(it[x].distance)
                    distanciaControle = it[x].distance
        for y in range (len(it)):
            if it[y].node == nodes[i] and it[y].distance == distanciaControle:
                aux.append(y)
    itAux=it
    it=[]
    for z in range (len (aux)):
        it.append(Interacao(itAux[aux[z]].node, itAux[aux[z]].distance, itAux[aux[z]].origin, itAux[aux[z]].status))             


def define_caminho(indice):
    global nodes
    caminho.append(it[indice].node)
    caminho.append(it[indice].origin)
    d = it[indice].origin
    while d != '1':
        x=0
        for x in range (len(it)):
            if it[x].node == d:
                d = it[x].origin
                caminho.append(it[x].origin)
    print('Caminho:')
    for i in range (len(caminho)):
        print(caminho[len(caminho)-1-i])
    caminho.clear()
    
def main():
    read_file()
    it.append(Interacao('1', '0', '-', '1')) #primeira iteracao
    referencia = 1 #referencia = permanente inicial para controle
    destino = '100'
    while contTemp != (len(nodes)-1):
        iteracao(referencia)
        trata_duplicatas()
        referencia = define_permanente()
        #print('no     rotulo      status')
        #for x in range (len(it)):
        #    print(str(it[x].node) + '    [' + str(it[x].distance) + ',' + str(it[x].origin) + ']     ' + str(it[x].status))

    for i in range (len(it)):
        if it[i].node == destino:
            define_caminho(i)
    #tirar comentario para printa tabela final        
    #print('nó     rótulo      status')
    #for x in range (len(it)):
    #    print(str(it[x].node) + '    [' + str(it[x].distance) + ',' + str(it[x].origin) + ']     ' + str(it[x].status))

    for x in range (len(it)):
        if it[x].node == destino:
            print('Distancia: ' + str(it[x].distance))
    
if __name__ == "__main__":
    main()
