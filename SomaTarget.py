from random import randint, random
from operator import add
from functools import reduce

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
] # Len -> 9
# Peso - 15
# Preco - 

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

def fitness(individual, capacidadeTotal, precoTotal):
    """
    Determine the fitness of an individual. Higher is better.

    individual: the individual to evaluate
    target: the target number individuals are aiming for

    O fitness do individuo perfeito sera ZERO, ja que o somatorio dara o target
    reduce: reduz um vetor a um escalar, neste caso usando o operador add
    """
    # individual -> [ 1, 0, 1, 0, 1, 0, 1 ]
    # retornar a soma do peso de cada item do 
    weight = getWeight(individual) 
    price = getPrice(individual)
    # sum = reduce(lambda i: , individual, 0)
    weightDist = abs(capacidadeTotal - weight)
    priceDist = abs(precoTotal - price)
    fitness = weightDist/2 + priceDist
    # fitness = weightDist / price
    return fitness

def media_fitness(pop, target, precoTotal):
    'Find average fitness for a population.'
    summed = reduce(add, (fitness(x, target) for x in pop), 0)
    return summed / (len(pop) * 1.0)

def melhor_fitness(pop, target, precoTotal):
    'Find average fitness for a population.'
    best = p[0]
    for i in p:
        best = i if fitness(i, target) < fitness(best, target) else best
    return best

def evolve(pop, target, precoTotal, retain=1, random_select=0.05, mutate=0.01):
    'Tabula cada individuo e o seu fitness'
    graded = [ (fitness(x, target, precoTotal), x) for x in pop]
    'Ordena pelo fitness os individuos - menor->maior'
    graded = [ x[1] for x in sorted(graded)]
    'calcula qtos serao elite'
    retain_length = int(len(graded)*retain)
    'elites ja viram pais'
    parents = graded[:retain_length]
    # randomly add other POUCOS individuals to
    # promote genetic diversity
    for individual in graded[retain_length:]:
        if random_select > random():
            parents.append(individual)
    # mutate some individuals
    for individual in parents:
        if mutate > random():
            pos_to_mutate = randint(0, len(individual)-1)
            # this mutation is not ideal, because it
            # restricts the range of possible values,
            # but the function is unaware of the min/max
            # values used to create the individuals,
            individual[pos_to_mutate] = randint(
                min(individual), max(individual))
    # crossover parents to create children
    parents_length = len(parents)
    'descobre quantos filhos terao que ser gerados alem da elite e aleatorios'
    desired_length = len(pop) - parents_length
    children = []
    limite = 10
    'comeca a gerar filhos que faltam'
    while len(children) < desired_length:
        'escolhe pai e mae no conjunto de pais'
        male = randint(0, parents_length)
        female = randint(0, parents_length)
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
    'adiciona a lista de pais (elites) os filhos gerados'
    parents.extend(children)
    return parents

precoTotal      = 233
capacidadeTotal = 15    # Peso total que a mochila irá aguentar
tamanhoPopulacao = 12 # Tamanho da população de cara geração
geracoes = 60           # Quantidade de gerações

p = population(tamanhoPopulacao, len(produtos), 0, 1)
for i in range(geracoes):
    p = evolve(p, capacidadeTotal, precoTotal)
    print('\nGeração #'+str(i+1)+" - Média: "+str(media_fitness(p, capacidadeTotal, precoTotal)))
    print('Todos:')
    for i in p:
       print('\t'+str(i)+' - R$ '+str(getPrice(i)) + ' - ' + str(getWeight(i)) + 'Kg')
    melhor = melhor_fitness(p, capacidadeTotal, precoTotal)
    print('Melhor:')
    print('\t'+str(melhor) + ' - ' + str(fitness(melhor, capacidadeTotal, precoTotal)) + ' \t R$' + str(getPrice(melhor)) + ' - ' + str(getWeight(melhor)) + 'Kg')
    print("\n")
    #fitness_history.append(media_fitness(p, capacidadeTotal))

# for datum in fitness_history:
#    print (datum)
