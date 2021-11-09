from random import randint, random
from operator import add
from functools import reduce
import numpy as np
import uuid

produtos = [
    { "nome": 'Chocolate',      "peso": 1.2, "preco": 2.1  },
    { "nome": 'Coca-Cola',      "peso": 3.3, "preco": 8.3  },
    { "nome": 'Pasta de Dente', "peso": 0.6, "preco": 3.2  },
    { "nome": 'Cebola',         "peso": 1.7, "preco": 3.4  },
    { "nome": 'Alho',           "peso": 4.1, "preco": 8.6  },
    { "nome": 'Toddy',          "peso": 3.2, "preco": 1.7  },
    { "nome": 'Nutella',        "peso": 5.5, "preco": 20.3 },
    { "nome": 'Detergente',     "peso": 1.0, "preco": 0.2  },
    { "nome": 'Arroz',          "peso": 3.6, "preco": 2.0  },
]


def individual(length, min, max):
    'Create a member of the population.'
    return [ randint(min,max) for x in range(length) ]

def population(count, length, min, max):
    """
    Create a number of individuals (i.e. a population).

    count: the number of individuals in the population
    length: the number of values per individual
    min: the minimum possible value in an individual's list of values
    max: the maximum possible value in an individual's list of values

    """
    return [ individual(length, min, max) for x in range(count) ]

def getWeight(individual):
    ret = 0
    for i in range(len(individual)):
        ret += produtos[i]['peso'] * individual[i]
    return ret

def getPrice(individual):
    ret = 0
    for i in range(len(individual)):
        ret += produtos[i]['preco'] * individual[i]
    return ret

def fitness(individual, capacidadeTotal):
    """
    Determina o fitness do individuo, levando em conta seu peco
    e tambem o quanto seu peso excede a capacidade total.

    Caso o peso ultrapasse a capacidade total, o fitness
    será reduzido em 10 * o excesso de peso.
    """
    price = getPrice(individual)
    weight = getWeight(individual)
    overweight = weight - capacidadeTotal
    return price - (10*overweight if overweight > 0 else 0)

def media_peso(pop):
    'Encontra o peso médio de uma população'
    summed = reduce(add, (getWeight(x) for x in pop), 0)
    return summed / (len(pop) * 1.0)

def media_fitness(pop, capacidadeTotal):
    'Encontra o fitness médio de uma população'
    summed = reduce(add, (fitness(x, capacidadeTotal) for x in pop), 0)
    return summed / (len(pop) * 1.0)

def melhor_fitness(pop, capacidadeTotal):
    'Encontra o melhor fitness de uma população'
    best = pop[0]
    for i in pop:
        best = i if fitness(i, capacidadeTotal) > fitness(best, capacidadeTotal) else best
    return best

def evolve(pop, capacidadeTotal, retain=0.5, random_select=0.5, mutate=0.1):
    'Tabula cada individuo e o seu fitness'
    graded = [ (fitness(x, capacidadeTotal), x) for x in pop]
    'Ordena pelo fitness os individuos - maior->menor'
    graded = [ x for x in sorted(graded, reverse=True)]
    'Calcula total de fitness'
    fitnessTotal = sum(x[0] for x in pop)
    'Rolando roleta'
    parents = []
    for individual in graded:
        'Calcula representação do individuo na roleta'
        percentage = individual[0]/fitnessTotal
        'Gira a roleta'
        if percentage > random():
            parents.append(individual[1])
    'Adicionando OUTROS para variedade genetica'
    retain_length = int(len(graded)*retain)
    for individual in graded[retain_length:]:
        if random_select > random():
            parents.append(individual[1])
    'Mutacao em alguns individuos'
    for individual in parents:
        if mutate > random():
            pos_to_mutate = randint(0, len(individual)-1)
            individual[pos_to_mutate] = randint(
                min(individual), max(individual))
    'Crossover dos pais'
    parents_length = len(parents)
    'Descobre quantos filhos terao que ser gerados alem da elite e aleatorios'
    desired_length = len(pop) - parents_length
    children = []
    limite = 10
    'Comeca a gerar filhos que faltam'
    while len(children) < desired_length:
        'escolhe pai e mae no conjunto de pais'
        male = randint(0, parents_length - 1)
        female = randint(0, parents_length - 1)
        if male != female:
            male = parents[male]
            female = parents[female]
            half = len(male) // 2
            'gera filho metade de cada'
            child = male[:half] + female[half:]
            'adiciona novo filho a lista de filhos'
            children.append(child)
        limite -= 1
        if limite == 0:
            break
    'Adiciona a lista de pais os filhos gerados'
    parents.extend(children)
    return parents

capacidadeTotal  = 15        # Peso total que a mochila irá aguentar
tamanhoPopulacao = 25       # Tamanho da população de cara geração
geracoes = 100              # Quantidade de gerações

# Definição da array usada para geração do arquivo .csv
csvData = [['Id', 'Media Fitness', 'Media peso', 'Maior Fitness', 'Maior Fitness - Peso']]
buffer = 0

p = population(tamanhoPopulacao, len(produtos), 0, 1)
for i in range(geracoes):
    p = evolve(p, capacidadeTotal)
    
    melhor = melhor_fitness(p, capacidadeTotal)
    if buffer == 0:
        csvData.append([i, round(media_fitness(p, capacidadeTotal),2), round(media_peso(p),2), fitness(melhor, capacidadeTotal), getWeight(melhor)])
        buffer = 10
    else:
        buffer -= 1

    print('\nGeração #'+str(i+1)+" - Média: R$"+str(round(media_fitness(p, capacidadeTotal),2)) + " - " +str(round(media_peso(p),2))+ "Kg")
    melhor = melhor_fitness(p, capacidadeTotal)
    print('Melhor:')
    print('\t'+str(melhor) + ' - ' + str(fitness(melhor, capacidadeTotal)) + ' \t R$' + str(getPrice(melhor)) + ' - ' + str(getWeight(melhor)) + 'Kg')
    print("\n")

# Exportando caso para arquivo CSV
fileName = uuid.uuid4().hex.upper()[0:6]                # Gera um id único para o caso
a = np.asarray(csvData, dtype="object")                 # Converte para array do numpy
np.savetxt(fileName+'.csv', a, delimiter=',', fmt='%s') # Exporta como .csv