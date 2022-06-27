## V5 ##
from random import sample; from random import shuffle; from random import randint; from random import choice; from collections import deque
# Things still pending: (difficulty 1-3)
# x) s̶e̶n̶d̶ ̶p̶l̶a̶y̶e̶d̶ ̶c̶a̶r̶d̶s̶ ̶t̶o̶ ̶a̶ ̶n̶e̶w̶ ̶d̶e̶c̶k̶ ̶f̶o̶r̶ ̶w̶h̶e̶n̶ ̶t̶h̶e̶ ̶o̶r̶i̶g̶i̶n̶a̶l̶ ̶d̶e̶c̶k̶ ̶r̶u̶n̶s̶ ̶o̶u̶t̶ ̶o̶f̶ ̶c̶a̶r̶d̶s̶ ̶(̶w̶o̶n̶d̶e̶r̶ ̶h̶o̶w̶ ̶t̶h̶e̶y̶'̶r̶e̶ ̶g̶o̶n̶n̶a̶ ̶t̶e̶s̶t̶ ̶t̶h̶a̶t̶ ̶t̶h̶o̶)
# x) ̶t̶a̶k̶e̶ ̶c̶a̶r̶d̶s̶ ̶o̶u̶t̶ ̶o̶f̶ ̶d̶e̶c̶k
# 2) turns
# 2) special cards mechanics
# ?) bugs such as 12 shown as 0
# ?) whatever else shows up lol
# Issues
# -) how are u gonna take cards out of the deck if you can't index 🤦🏻‍♂️ "list(dict.keys())" takes away the efficiency (couldn't find a better way)
# -) how are u gonna look for color/type matches in cpus_hands you can ask "if key in dic" for the number but since color and type are values well... 🤦🏻‍♂️
#    (pretty meh)
# -) possible bug where the card on the table also appears on discarded ??? I'll worry bout that l8ter

def DeckMaker():
    #10-12 ... 94-96 block(🛇) - reverse(⇆) - +2
    Deck  = {}
    Color = {0:'red', 1:'yellow', 2:'green', 3:'blue'}
    Type  = {0:'🛇', 1:'⇆', 2:'+2'}
    changeType, changeCol, move = 0, 0, 10
               
    for numero in range(1,97):
        if numero > 9 and numero % move in Type:   # > 9 or else the first 3 cards would be special cards
            changeType = numero % move 
            Deck[numero] = [numero, Color[changeCol], Type[changeType]]
            if numero % move == 2:
                move += 12   # To correct the positioning after the first 3 changeType
        else:
            Deck[numero] = [numero, Color[changeCol], '']
        if numero % 12 == 0:
            changeCol += 1        # To change color 
        if numero % 48 == 0:      # So that we get 2 cards of every card
            changeCol = 0
            changeType = 0
    return Deck

def CardDistribution(Deck):
    #Each player grabs 8 cards and then those cards get deleted from deck
    NewPlayer = {}
    NewPlayerCards = [Deck.pop(x) for x in sample(list(Deck),8)]
    for carta in NewPlayerCards: 
        NewPlayer[carta[0]] = carta
    return NewPlayer

def DeckShuffling(Deck): 
    lista = list(Deck.items())
    shuffle(lista)
    Deck = dict(lista)
    return Deck

def makeAMove(Player,state,Discarded):

    print('\nYour cards are:\n')
    count = 0
    for carta in Player:
        print(f'{count}: {Player[carta][0] % 12} {Player[carta][1]} {Player[carta][2]}')  #have to fix 12 shown as 0 
        count+=1
    print('\nChoose one by indicating the index')

    indice = int(input()); listKeys = list(Player.keys()); chosen = listKeys[indice]

    if state == 'Empty':
        Table = Player.pop(chosen)
        Discarded[chosen] = Table
        print(f'The card at play after your move is now: {Table[0] %12} {Table[1]} {Table[2]}')

    elif Player[chosen][0] % 12 == (state[0] % 12): #% 12 So that numbers match cause they're stored as 1-96, 
        print('same number, doable')
        Table = Player.pop(chosen)
        Discarded[chosen] = Table
        print(f'The card at play after your move is now: {Table[0] %12} {Table[1]} {Table[2]}')

    elif Player[chosen][1] == state[1]:
        print('same color, doable')
        Table = Player.pop(chosen)
        Discarded[chosen] = Table
        print(f'The card at play after your move is now: {Table[0] %12} {Table[1]} {Table[2]}')

    elif Player[chosen][0] % 12 >= 10 and Player[chosen][2] == state[2]: #causes issues cause 12 isn't 12
        print('same type, doable')
        Table = Player.pop(chosen)
        Discarded[chosen] = Table
        print(f'The card at play after your move now is: {Table[0] %12} {Table[1]} {Table[2]}')
    else:
        print('Invalid move')
        return

def AI(Deck,state,who,Discarded):
    whoText = who[0]
    who = who[1]
   
    if state == 'Empty':
        state = who[choice(list(who.keys()))]                                    #ended up converting to list anyway lmao
        print(f'the {whoText} played: {state[0] % 12} {state[1]} {state[2]}')     # gotta fix 12 shown as 0 
        print(f'The card at play now is: {state[0] % 12} {state[1]} {state[2]}')
        Discarded[state[0]] = who.pop(state[0])                                  #Discarded becomes the new deck when the og deck runs out of cards
        print(len(who))
        return state #state keeps the non % 12 value
    
    #Checks if the number of the card at play matches any in the hand of the CPU (not working) the only saving grace of dics and well, f
    CPUListNumbers = {}
    for carta in who:
         if who[carta][0] % 12  != 0 and who[carta][0] % 12 == state[0] % 12: 
            CPUListNumbers[carta] = who[carta][0] #mantains the same Key as CPU so that the cards can be discarded later
    
    if  len(CPUListNumbers) != 0:
        state = who[choice(list(CPUListNumbers.keys()))]
        print('SAME Number')
        print(f'the {whoText} played: {state[0] % 12} {state[1]} {state[2]}') # gotta fix 12 shown as 0 
        print(f'The card at play now is: {state[0] % 12} {state[1]} {state[2]}')
        Discarded[state[0]] = who.pop(state[0]) 
        return state

    #Checks if the color of the card at play matches any in the hand of the CPU
    CPUListColors = {}
    for carta in who:
        if who[carta][1] == state[1] and who[carta][2] == '':
            CPUListColors[carta] = who[carta][1] #mantains the same Key as CPU so that the cards can be discarded later
    
    if len(CPUListColors) != 0:
        state = who[choice(list(CPUListColors.keys()))]
        print('SAME COLOR')
        print(f'the {whoText} played: {state[0] % 12} {state[1]} {state[2]}') # gotta fix 12 shown as 0 
        print(f'The card at play now is: {state[0] % 12} {state[1]} {state[2]}')
        Discarded[state[0]] = who.pop(state[0])
        return state
    
    #Checks if the type of the card at play matches any in the hand of the CPU 
    CPUListType = {}
    for carta in who:
        if who[carta][2] != '' and  who[carta][2] == state[2]:   
            CPUListType[carta] = who[carta][2] #mantains the same Key as CPU so that the cards can be discarded later
    
    if len(CPUListType) != 0:
        state = who[choice(list(CPUListType.keys()))]
        Special.append(state[2]) #To activate effect later
        print('SAME TYPE')
        print(f'the {whoText} played: {state[0] % 12} {state[1]} {state[2]}') # gotta fix 12 shown as 0 
        print(f'The card at play now is: {state[0] % 12} {state[1]} {state[2]}')
        Discarded[state[0]] = who.pop(state[0])
        return state
    
    #If the CPU has no cards, it takes one from deck and removes it
    else:
        if len(Deck) > 0:
            print(f'{whoText} drew a card')
            add = Deck.pop(choice(list(Deck.keys()))) #slowest operation yet
            who[add[0]] = add
        else:
            print(f'Deck is empty, discarded cards are gonna be use now and {whoText} draws a card')
            for key,value in Discarded.items():   # because all other ways of referencing Discarded will cause problems after Discarded gets cleared
                Deck[key] = value
            Discarded.clear()
            add  = Deck.pop(choice(list(Deck.keys()))) #slowest yet
            who[add[0]] = add
            
    return state

def Effects(Deck,whoKey,turn,Special,Participants,order):
    if Special[0] == '🛇':
        turn = Participants[(whoKey + order[0]*2) % 4]
        print(f'a special 🛇 card was used')

    elif Special[0] == '⇆':
        order.append(order.pop()*-1)
        turn = Participants[(abs((whoKey - order[0]) % 4))]
        print(f'a special ⇆ card was used')

    elif Special[0] == '+2':
        add1 = Deck.pop(choice(list(Deck.keys())))
        add2 = Deck.pop(choice(list(Deck.keys())))
        # whoKey[add1[0]] = add1 fix
        # whoKey[add2[0]] = add2 fix
        print(f'a special +2 card was used')
    
    Special.pop()
    return turn

## Driver Code ##
Deck   = DeckMaker()
Player = CardDistribution(Deck); CPU1 = CardDistribution(Deck); CPU2 = CardDistribution(Deck); CPU3 = CardDistribution(Deck)
Deck   = DeckShuffling(Deck) 
Discarded = {}
Special = []
order   = [1]

#So that we can reference who starts the game
Participants = {0:['You',Player,0], 1:['CPU1',CPU1,1], 2:['CPU2',CPU2,2], 3:['CPU3',CPU3,3]}

#Defines starter player

next = Participants[randint(0,3)]
print('The one to start off the game is:',next[0],'\n')

# First instance of the game
Table = 'Empty'
print('The card at play right now is:',Table,'\n')

if next[0] != 'You':
    Table = (AI(Deck,Table,next,Discarded)) 
else:
    makeAMove(Player,Table,Discarded)

# if Table[2] == '⇆':
#     order.append((order.pop()*-1))   
#     next = Participants[abs((Begins[2]+order[0])%4)]
#     print('\n A ⇆ card was played, the next turn goes to:',next[0])
# else: 
#     next = Participants[(Begins[2]+order[0])%4]
#     print('\nThe next turn goes to:',next[0])

# a = next
# print('next',a)

#Rest of the game (fix same player plays twice at the beginning)
while len(Player) != 0 or len(CPU1) != 0 or len(CPU2) != 0 or len(CPU3) != 0:
     if next[0] == 'You':
        makeAMove(Player,Table,Discarded)
        next = Participants[(next[2] + order[0]) % 4] #breaks after players turn
        if len(Special) != 0:
            next = Effects(Deck,next[2],next,Special,Participants,order)
     else:
        Table = AI(Deck,Table,next,Discarded)
        next  = Participants[(next[2] + order[0]) % 4] 
        if len(Special) != 0:
            next = Effects(Deck,next[2],next,Special,Participants,order)


        print('CARTAS DE CADA JUGADOR',len(Player),len(CPU1),len(CPU2),len(CPU3))