# -*- coding: utf-8 -*-
"""
Black Jack Game
Created on Sat Dec 20 12:08:27 2025

@author: Kolokolnikova Sarum
"""
import random

# Масти карт
suits = ('♥', '♦', '♣', '♠')
# Ранги карт (достоинства)
ranks = ('2','3','4','5','6','7','8','9','10','J','Q','K','A')
# Значения карт в игре Blackjack
values = {'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':10,
          'Q':10,'K':10,'A':11}


class Card:
    """Класс, представляющий игральную карту."""
    
    def __init__(self, suit, rank):
        """
        Инициализирует карту.
        
        Parameters
        ----------
        suit : str
            Масть карты (♥, ♦, ♣, ♠)
        rank : str
            Достоинство карты (2-10, J, Q, K, A)
        """
        self.suit = suit
        self.rank = rank
        
    def __str__(self):
        """Возвращает строковое представление карты."""
        return self.rank + ' ' + self.suit


class Deck:
    """Класс, представляющий колоду из 52 карт."""
    
    def __init__(self):
        """Инициализирует полную колоду из 52 карт."""
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))
                
    def __str__(self):
        """Возвращает строковое представление всей колоды."""
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n' + card.__str__()
        return 'В колоде находятся карты: ' + deck_comp
    
    def shuffle(self):
        """Тщательно перемешивает колоду карт."""
        random.shuffle(self.deck)
        
    def deal(self):
        """
        Раздает одну карту из колоды.
        
        Returns
        -------
        Card
            Карта, взятая из верхней части колоды
        """
        single_card = self.deck.pop()
        return single_card


class Hand:
    """Класс, представляющий руку игрока или дилера."""
    
    def __init__(self):
        """
        Инициализирует пустую руку.
        """
        self.cards = []  # Список карт на руке
        self.value = 0   # Общая стоимость карт на руке
        self.aces = 0    # Количество тузов на руке (нужно для корректного расчета)
    
    def add_card(self, card):
        """
        Добавляет карту в руку и пересчитывает стоимость.
        
        Parameters
        ----------
        card : Card
            Карта для добавления в руку
        """
        self.cards.append(card)
        self.value += values[card.rank]
        
        # Учитываем тузы при добавлении карты
        if card.rank == 'A':
            self.aces += 1
        
    def adjust_for_ace(self):
        """
        Корректирует стоимость тузов.
        
        Если общая стоимость превышает 21 и в руке есть тузы,
        считает тузы как 1 вместо 11.
        """
        while self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1


class Chips:
    """Класс для управления фишками игрока."""
    
    def __init__(self, total=100):
        """
        Инициализирует стартовый банк игрока.
        
        Parameters
        ----------
        total : int, optional
            Начальное количество фишек (по умолчанию 100)
        """
        self.total = total 
        self.bet = 0  # Текущая ставка
    
    def win_bet(self):
        """Добавляет выигранную ставку к общему количеству фишек."""
        self.total += self.bet
        
    def lose_bet(self):
        """Вычитает проигранную ставку из общего количества фишек."""
        self.total -= self.bet


def take_bet(chips):
    """
    Запрашивает у игрока ставку и проверяет ее корректность.
    
    Parameters
    ----------
    chips : Chips
        Объект с фишками игрока
        
    Notes
    -----
    Цикл продолжается до тех пор, пока игрок не введет корректную ставку:
    - Должно быть целое число
    - Не больше текущего количества фишек
    """
    while True:
        try:
            chips.bet = int(input('Сколько фишек вы хотите поставить? '))
        except ValueError:
            print('Ошибка: введите целое число')
        else:
            if chips.bet > chips.total:
                print(f'Недостаточно фишек. Доступное количество: {chips.total}')
            elif chips.bet <= 0:
                print('Ставка должна быть положительным числом')
            else:
                break


def hit(deck, hand):
    """
    Берет одну карту из колоды и добавляет ее в руку.
    
    Parameters
    ----------
    deck : Deck
        Колода карт
    hand : Hand
        Рука игрока или дилера
    """
    single_card = deck.deal()
    hand.add_card(single_card)
    hand.adjust_for_ace()


def show_some(player, dealer):
    """
    Показывает карты игрока и одну карту дилера.
    
    Parameters
    ----------
    player : Hand
        Рука игрока
    dealer : Hand
        Рука дилера
        
    Notes
    -----
    Одна карта дилера остается скрытой (обозначается [?]),
    чтобы игрок не видел полную руку дилера.
    """
    print("\n" + "="*40)
    print("ТЕКУЩАЯ СИТУАЦИЯ:")
    print("="*40)
    
    print("\nКарты Дилера:")
    print("  [?]")  # Скрытая карта
    print(f"  {dealer.cards[1]}")  # Открытая карта
    
    print("\nКарты Игрока:")
    for card in player.cards:
        print(f"  {card}")
    print(f"Сумма очков: {player.value}")
    print("="*40)


def hit_or_stand(deck, player, dealer):
    """
    Предлагает игроку взять еще карту или остановиться.
    
    Parameters
    ----------
    deck : Deck
        Колода карт
    player : Hand
        Рука игрока
    dealer : Hand
        Рука дилера
        
    Returns
    -------
    bool
        True - игрок хочет взять еще карту
        False - игрок останавливается или превысил 21 очко
    """
    while True:
        choice = input('\nВзять карту (H) или остановиться (S)? Введите h или s: ')
        
        if choice.lower() == 'h':
            hit(deck, player)
            show_some(player, dealer)
            
            # Проверяем, не превысил ли игрок 21 очко
            if player.value > 21:
                return False
            return True
            
        elif choice.lower() == 's':
            print('\nИгрок останавливается. Ход переходит к дилеру.')
            return False
            
        else:
            print('Неверный ввод. Пожалуйста, введите "h" или "s".')


def show_all(player, dealer):
    """
    Показывает все карты игрока и дилера в конце раунда.
    
    Parameters
    ----------
    player : Hand
        Рука игрока
    dealer : Hand
        Рука дилера
    """
    print("\n" + "="*50)
    print("РЕЗУЛЬТАТ РАУНДА:")
    print("="*50)
    
    print("\nКарты Дилера:")
    for card in dealer.cards:
        print(f"  {card}")
    print(f"Сумма очков дилера: {dealer.value}")
    
    print("\nКарты Игрока:")
    for card in player.cards:
        print(f"  {card}")
    print(f"Сумма очков игрока: {player.value}")
    print("="*50)


def player_busts(player, dealer, chips):
    """
    Обрабатывает ситуацию, когда игрок превысил 21 очко.
    
    Parameters
    ----------
    player : Hand
        Рука игрока 
    dealer : Hand
        Рука дилера 
    chips : Chips
        Фишки игрока
    """
    print("\n✖ ПЕРЕБОР! У игрока больше 21 очка.")
    chips.lose_bet()


def player_wins(player, dealer, chips):
    """
    Обрабатывает выигрыш игрока.
    
    Parameters
    ----------
    player : Hand
        Рука игрока 
    dealer : Hand
        Рука дилера 
    chips : Chips
        Фишки игрока
    """
    print("\n✓ ИГРОК ВЫИГРАЛ!")
    chips.win_bet()


def dealer_busts(player, dealer, chips):
    """
    Обрабатывает ситуацию, когда дилер превысил 21 очко.
    
    Parameters
    ----------
    player : Hand
        Рука игрока 
    dealer : Hand
        Рука дилера 
    chips : Chips
        Фишки игрока
    """
    print("\n✓ ДИЛЕР ПЕРЕБРАЛ! Игрок выиграл.")
    chips.win_bet()


def dealer_wins(player, dealer, chips):
    """
    Обрабатывает выигрыш дилера.
    
    Parameters
    ----------
    player : Hand
        Рука игрока 
    dealer : Hand
        Рука дилера 
    chips : Chips
        Фишки игрока
    """
    print("\n✖ ДИЛЕР ВЫИГРАЛ!")
    chips.lose_bet()


def push(player, dealer):
    """
    Обрабатывает ничью.
    
    Parameters
    ----------
    player : Hand
        Рука игрока 
    dealer : Hand
        Рука дилера 
    """
    print("\n≡ НИЧЬЯ! Ставка возвращается игроку.")

# Подготовка новой игры
deck = Deck()           # Создание новой колоды
deck.shuffle()          # Перемешивание колоды
    
player_hand = Hand()    # Создание руки игрока
dealer_hand = Hand()    # Создание руки дилера
    
# Раздача начальных карт (по 2 карты каждому)
player_hand.add_card(deck.deal())
player_hand.add_card(deck.deal())
dealer_hand.add_card(deck.deal())
dealer_hand.add_card(deck.deal())
    
# Инициализация фишек игрока
player_chips = Chips()
    
print(f"ВАШ БАЛАНС: {player_chips.total} фишек")

# ОСНОВНОЙ ЦИКЛ ИГРЫ
while True:
    # Приветственное сообщение
    print("\n" + "="*60)
    print("ДОБРО ПОЖАЛОВАТЬ В BLACKJACK!")
    print("="*60)
    print("Правила:")
    print("- Цель: набрать сумму очков ближе к 21, чем у дилера")
    print("- Карты 2-10 стоят по номиналу")
    print("- Валет, дама, король = 10 очков")
    print("- Туз = 11 или 1 очко (автоматический выбор)")
    print("- Дилер обязан брать карты, пока у него меньше 17 очков")
    print("="*60)
    

    # Запрос ставки у игрока
    take_bet(player_chips)
    
    # Показ начальной ситуации
    show_some(player_hand, dealer_hand)
    
    # ХОД ИГРОКА
    print("\n" + "~"*30)
    print("ХОД ИГРОКА")
    print("~"*30)
    
    player_turn = True  # Флаг для управления ходом игрока
    
    while player_turn and player_hand.value <= 21:
        player_turn = hit_or_stand(deck, player_hand, dealer_hand)
    
    # Если игрок превысил 21 очко
    if player_hand.value > 21:
        show_all(player_hand, dealer_hand)
        player_busts(player_hand, dealer_hand, player_chips)
    else:
        # ХОД ДИЛЕРА
        print("\n" + "~"*30)
        print("ХОД ДИЛЕРА")
        print("~"*30)
        
        # Открываем скрытую карту дилера
        print(f"Скрытая карта дилера: {dealer_hand.cards[0]}")
        print(f"Текущая сумма дилера: {dealer_hand.value}")
        
        # Дилер берет карты, пока у него меньше 17 очков
        while dealer_hand.value < 17:
            print("\nДилер берет карту...")
            hit(deck, dealer_hand)
            print(f"Дилер взял: {dealer_hand.cards[-1]}")
            print(f"Новая сумма дилера: {dealer_hand.value}")
        
        # Показ финальной ситуации и определение победителя
        show_all(player_hand, dealer_hand)
        
        # Определение результата игры
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)
        else:
            push(player_hand, dealer_hand)
    
    # Отображение баланса игрока
    print("\n" + "="*40)
    print(f"ВАШ БАЛАНС: {player_chips.total} фишек")
    print("="*40)
    
    # Проверка на наличие фишек
    if player_chips.total <= 0:
        print("\n" + "!"*50)
        print("ИГРА ОКОНЧЕНА! У вас закончились фишки.")
        print("!"*50)
        break
    
    # Предложение сыграть еще раз
    print("\n" + "-"*50)
    play_again = input('Хотите сыграть еще раз? (y/n): ')
    
    if play_again.lower() != 'y':
        print("\n" + "="*50)
        print("Спасибо за игру! До новых встреч!")
        print("="*50)
        break