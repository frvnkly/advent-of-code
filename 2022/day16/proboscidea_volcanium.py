import sys
import math

sys.path.append('.')
from util import get_input

class Valve:
    def __init__(self, name, flow):
        self.name = name
        self.flow = flow
        self.tunnels = []

class Tunnel:
    def __init__(self, to, cost=1):
        self.to = to
        self.cost = cost

def get_shortest_path(valves, v1, v2):
    def recurse(cost, seen, valve):
        if valve.name == v2: return cost

        seen.add(valve.name)        
        costs = [math.inf]
        for tunnel in valve.tunnels:
            if not tunnel.to.name in seen:
                costs.append(recurse(cost + 1, set(seen), tunnel.to))
                
        return min(costs)

    return recurse(0, set(), valves[v1])

def simplify_valves(valves):
    new_valves = {}
    for valve in valves.values():
        if valve.flow or valve.name == 'AA':
            new_valve = Valve(valve.name, valve.flow)
            new_valves[valve.name] = new_valve

    for valve1 in new_valves:
        for valve2 in new_valves:
            if valve1 == valve2: continue
            cost = get_shortest_path(valves, valve1, valve2)
            tunnel = Tunnel(new_valves[valve2], cost)
            new_valves[valve1].tunnels.append(tunnel)

    return new_valves

def build_cave():
    lines = get_input('2022/day16/input.txt')

    valves = {}
    for line in lines:
        arr = line.split(' ')
        name = arr[1]
        flow = int(arr[4][5:-1])

        valve = Valve(name, flow)
        valves[name] = valve

    for line in lines:
        arr = line.split(' ')
        name = arr[1]
        tunnels = list(map(lambda x: x.replace(',', ''), arr[9:]))

        valve = valves[name]
        for tunnel in tunnels:
            valve.tunnels.append(Tunnel(valves[tunnel]))

    return simplify_valves(valves)['AA']

def part1(cave):
    def recurse(minutes, open_valves, valve):
        if minutes <= 0:
            return 0

        open_valves.add(valve.name)

        pressure = 0
        if valve.flow:
            minutes -= 1
            pressure = valve.flow * minutes        
        
        next_tunnels = list(filter(
            lambda x: not x.to.name in open_valves and x.cost < minutes,
            valve.tunnels
        ))
        if next_tunnels:
            pressure += max(map(
                lambda x: recurse(minutes - x.cost, set(open_valves), x.to),
                next_tunnels
            ))
        
        return pressure

    return recurse(30, set(), cave)

if __name__ == '__main__':
    cave = build_cave()
    
    print(f'part 1: {part1(cave)}')
