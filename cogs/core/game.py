from json import loads, dumps

import disnake

resources_lst = ('медь', 'свинец', 'метастекло', 'графит', 'песок', 'уголь', 'титан', 'торий', 'металлолом', 'кремний',
                 'пластан', 'фазовая ткань', 'кинетический сплав', 'споровый стручок', 'пиротит', 'взрывчатая смесь')
buildings_lst = ('Ядра', 'Буры', 'Турели', 'Стены', 'Эффекты')


def simple(in_arr):
    out_arr = []
    for i in set(in_arr):
        out_arr.append(f'{i} * {in_arr.count(i)}')
    return out_arr


def fight(attacker, defender):
    step = 0
    while attacker and defender:
        attack = attacker.damage(step)
        contrattack = defender.damage(step)
        print(step, attack, contrattack)
        attacker.attack(contrattack)
        defender.attack(attack)
        step += 1
        if step > 60:
            break


class ResourceList:
    def __init__(self, resources=None):
        self.resources = resources if resources else [0] * 16

    def __str__(self):
        return str('\n'.join(
            [f"{resources_lst[i]}: {self.resources[i]}".capitalize() for i in range(16) if self.resources[i]]))

    def __add__(self, other):
        return ResourceList([self.resources[i] + other.resources[i] for i in range(16)])

    def __ge__(self, other):
        return self.resources >= other.resources

    def __sub__(self, other):
        return ResourceList([self.resources[i] - other.resources[i] for i in range(16)])

    def __mul__(self, other: int):
        return ResourceList([self.resources[i] * other for i in range(16)])

    def dump(self):
        return self.resources

    def correction(self, capacity):
        self.resources = [min(i, capacity) for i in self.resources]


class Object:
    def __init__(self):
        self.cost = ResourceList()
        self.data = ''
        self.health = 0
        self.max_health = 0
        self.name = ''
        self.type = ''

    def buy(self, user):
        if user.resources > self.cost:
            user.resources - self.cost
            eval(f'user.{self.data}.append(self)')

    def hurt(self, value):
        self.health -= value if value < self.health else self.health

    def dump(self):
        return self.data, self.health

    def display(self):
        return f'**{self.name}**\nПрочность: {self.health}({100 * round(self.health / self.max_health, 2)}%)'

    def update(self, regeneration):
        self.health = min(regeneration + self.health, self.max_health)
        return ResourceList()


'''    def __str__(self):
        return str(self.health)'''


class Shard(Object):
    def __init__(self, health: int = 1100):
        super().__init__()
        self.health = health
        self.max_health = 1100
        self.cost = ResourceList([1000, 800] + [0] * 14)
        self.capacity = 4000
        self.data = 'Shard'
        self.type = 'core'
        self.name = 'Осколок'


class Drill(Object):
    def __init__(self):
        super().__init__()
        self.mining = ResourceList()
        self.volume = 0
        self.type = 'drill'

    def update(self, regeneration):
        self.health = min(regeneration + self.health, self.max_health)
        return self.mining


class MechanicalDrill(Drill):
    def __init__(self, health=160):
        super().__init__()
        self.cost = ResourceList([12] + [0] * 15)
        self.health = health
        self.max_health = 160
        self.data = 'MechanicalDrill'
        self.name = 'Механический бур'
        self.mining = ResourceList([21, 21, 0, 0, 24, 20, 0, 0, 24] + [0] * 7)


class Weapon:
    def __init__(self):
        self.bullets = 0
        self.damage = 0
        self.splash_damage = 0
        self.recharging = 0
        self.can_attack_air = True
        self.can_attack_ground = True


class LaserWeapon:
    def __init__(self):
        self.damage = 0
        self.duration = 0
        self.recharging = 0
        self.can_attack_air = True
        self.can_attack_ground = True


class Turret(Object, Weapon):
    def __init__(self):
        super().__init__()
        self.type = 'turret'


class LaserTurret(Object, LaserWeapon):
    def __init__(self):
        super().__init__()
        self.type = 'turret'


class Duo(Turret):
    def __init__(self, health=250):
        super().__init__()
        self.cost = ResourceList([35] + [0] * 15)
        self.health = health
        self.max_health = 250
        self.bullets = 1
        self.damage = 9
        self.recharging = 33
        self.data = 'Duo'
        self.name = 'Двойная турель'


class Wall(Object):
    def __init__(self):
        super().__init__()
        self.type = 'wall'


class CopperWall(Wall):
    def __init__(self, health=1280):
        super().__init__()
        self.cost = ResourceList([24] + [0] * 15)
        self.data = 'CopperWall'
        self.name = 'Медная Стена'
        self.health = health
        self.max_health = 1280


class BuildingsList:
    def __init__(self, core: tuple = (Shard(),), drill: tuple = (), turrets: tuple = (), walls: tuple = (),
                 effects: tuple = ()):
        self.core = core
        self.drill = drill
        self.turrets = turrets
        self.walls = walls
        self.effects = effects

    def dump(self):
        return tuple(i.dump() for i in self.core), tuple(i.dump() for i in self.drill), tuple(
            i.dump() for i in self.turrets), tuple(i.dump() for i in self.walls), tuple(i.dump() for i in self.effects)

    def display(self):
        buildings = [self.core, self.drill, self.turrets, self.walls, self.effects]
        emb = disnake.Embed(title='Ваша база')
        for i in range(5):
            emb.add_field(name=buildings_lst[i], value='\n'.join(simple([j.display() for j in buildings[i]])),
                          inline=False)
        return emb

    def append(self, building: Object):
        type = building.type
        if type == 'core':
            self.core += (building,)
        elif type == 'drill':
            self.drill += (building,)
        elif type == 'wall':
            self.walls += (building,)
        elif type == 'turret':
            self.turrets += (building,)
        elif type == 'effect':
            self.effects += (building,)

    def capacity(self):
        return sum(i.capacity for i in self.core)

    def attack(self, damage):
        walls_health = sum(i.health for i in self.walls)
        walls_damage = min(walls_health, damage)
        damage -= walls_damage
        print(walls_health, walls_damage)
        for i in self.walls:
            i.hurt(walls_damage/len(self.walls))
        if not damage:
            return

    def __iter__(self):
        return iter([self.core, self.drill, self.turrets, self.walls, self.effects])

    def __bool__(self):
        return any(i.health for i in self.core)


class Player:
    def __init__(self, resources: tuple = None, buildngs: tuple = None):
        self.resources = ResourceList(resources)
        self.buildings = BuildingsList(*buildngs)

    def update(self):
        health = 0
        for i in self.buildings:
            for j in i:
                self.resources += j.update(health)
                self.resources.correction(self.buildings.capacity())

    def damage(self, step):
        damage = 0
        splash_damage = 0
        laser_damage = 0
        for i in self.buildings.turrets:
            if isinstance(i, Turret):
                damage += i.damage * i.bullets * (not (step % i.recharging))
                splash_damage += i.splash_damage * i.bullets * (not (step % i.recharging))
            elif isinstance(i, LaserTurret):
                laser_damage += i.damage * (not (step % i.recharging))
        return damage, splash_damage, laser_damage

    def attack(self, damage):
        self.buildings.attack(damage)

    def __bool__(self):
        return bool(self.buildings)


class User(Player):
    def __init__(self, uid: int):
        self.uid = uid
        super().__init__(*self.load())

    def load(self):
        with open('cogs/core/players.json') as f:
            saves = loads(f.read())
            try:
                resources = saves[f'{self.uid}']['resources']
                buildings = []
                for i in saves[f'{self.uid}']['buildings']:
                    s = []
                    for j in i:
                        s.append(eval(f'{j[0]}({j[1]})'))
                    buildings.append(tuple(s))

            except KeyError:
                resources = [100] + [0] * 15
                buildings = None
        return resources, (tuple(buildings) if buildings else ((Shard(),), (), (), (), ()))

    def __del__(self):
        with open('cogs/core/players.json') as f:
            saves = loads(f.read())
            try:
                saves[f'{self.uid}']
            except KeyError:
                saves[f'{self.uid}'] = {}
            saves[f'{self.uid}']['resources'] = self.resources.dump()
            saves[f'{self.uid}']['buildings'] = self.buildings.dump()
        with open('cogs/core/players.json', 'w') as f:
            f.write(dumps(saves))


'''n = ResourceList([1, 2, 3, 4, 5, 6, 7, 8, 0, 1, 2, 3, 4, 5, 6, 7])
m = ResourceList([1, 2, 1, 4, 2, 4, 6, 8, 1, 2, 3, 4, 5, 6, 7, 8])
n -= m
print(n)
core = Shard()
core.damage(200)
print(core)
core.damage(10000)
print(core)
print(n.dump())
s = BuildingsList()
print(s.dump())'''
