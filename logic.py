from random import randint
import requests

pokemon_img = 'https://www.google.com/url?sa=i&url=https%3A%2F%2Fanime-characters-fight.fandom.com%2Fru%2Fwiki%2F%25D0%259F%25D0%25B8%25D0%25BA%25D0%25B0%25D1%2587%25D1%2583_%25D0%25AD%25D1%2588%25D0%25B0&psig=AOvVaw1x8ss28AIPpm2Huin42RCo&ust=1701087406215000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCLCZwMjS4YIDFQAAAAAdAAAAABAE'


class Pokemon:
    pokemons = {}

    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer

        self.pokemon_number = randint(1, 1000)
        self.img = self.get_full_image()
        self.name = self.get_name()
        self.hp = randint(1, 100)
        self.power = randint(50, 100)

        Pokemon.pokemons[pokemon_trainer] = self
        print(
            f'Добавлен покемон для пользователя {pokemon_trainer} в словарь Pokemon.pokemons')

    def __lt__(self, other):
        return self.hp < other.hp

    def __gt__(self, other):
        return self.hp > other.hp

    def __eq__(self, other):
        return self.hp == other.hp

    def __str__(self):
        return self.info()

    def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['name'])
        else:
            return 'Pikachu'

    def get_front_image(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}/'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['sprites']['front_default'])
        else:
            return pokemon_img

    def get_back_image(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}/'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['sprites']['back_default'])
        else:
            return pokemon_img

    def get_full_image(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}/'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['sprites']['other']['official-artwork']['front_default'])
        else:
            return pokemon_img

    def info(self):
        return f'Тренер покемона: @{self.pokemon_trainer}\nИмя твоего покеомона: {self.name}\nЗдоровье покемона: {self.hp}%\nСила покемона: {self.power}'

    def show_img(self):
        return self.img

    def attack(self, enemy):
        if isinstance(enemy, Wizard):
            chance = randint(1, 5)
            if chance == 1:
                return "Покемон-волшебник применил щит в сражении"
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"""Сражение @{self.pokemon_trainer} с @{enemy.pokemon_trainer}
Здоровье @{enemy.pokemon_trainer} теперь {enemy.hp}"""
        else:
            enemy.hp = 0
            return f"Победа @{self.pokemon_trainer} над @{enemy.pokemon_trainer}!"


class Wizard(Pokemon):
    def info(self):
        return "У тебя покемон-волшебник 🧙\n\n" + super().info()


class Fighter(Pokemon):
    def attack(self, enemy):
        super_power = randint(1, 3)
        self.power *= super_power
        result = super().attack(enemy)
        self.power /= super_power
        return result + f'\nБоец применил суперсилу и увеличил урон по противнику в {super_power} раз!'

    def info(self):
        return "У тебя покемон-боец 💪\n\n" + super().info()


pokemon = Pokemon('user1')
pokemon2 = Pokemon('user2')

print(pokemon.info())
print('____________________________\n')
print(pokemon2.info())
print('____________________________\n')
print(pokemon < pokemon2)
print(pokemon > pokemon2)
print(pokemon == pokemon2)
print('____________________________\n')
print(pokemon)
