# Aditya Ganesh
# Term Project 

from cmu_112_graphics import *
import random
import sys
import copy

class attack(object):
    def __init__(self, troop, cx, cy, color, dps, speed, slope, towerOrigin):
        self.troop = troop
        self.cx = cx
        self.cy = cy
        self.color = color
        self.dps = dps
        self.speed = speed
        self.radius = 4
        self.slope = slope
        self.towerOrigin = towerOrigin

class troop(object):

    def __init__(self, name, rarity, elixir, radius, targets,     
                                                    dps, health, attackType, circleR, color, speed, count, sight):
        self.name = name
        self.sight = sight
        self.rarity = rarity
        self.elixir = elixir
        self.radius = radius
        self.targets = targets
        self.dps = dps
        self.count = count
        self.health = health
        self.speed = speed
        self.status = "moving"
        self.attackType = attackType 
        self.circleR = circleR
        self.color = color
        self.cx = 0
        self.cy = 0
    
    def takeDamage(self, damage):
        self.health -= damage

    def getHealth(self):
        return self.health
    
    def attack(self, other):
        # lock on to whatever is nearest in range
        other.health -= self.dps

# properties for all spells
class spell(object):

    # can use inheritance here
    def __init__(self, name, rarity, elixir, radius, targets, damage, time):
        self.name = name
        self.rarity = rarity
        self.elixir = elixir
        self.radius = radius
        self.targets = targets
        self.damage = damage
        self.time = time

# either princess or king tower
class tower(troop):

    def __init__(self, name, dps, radius, targets, xRange, yRange):
        self.name = name
        self.dps = dps
        self.radius = radius
        self.targets = targets
        self.xRange = xRange
        self.yRange = yRange
        self.target = None
        if name.lower().endswith("king"):
            self.health = 4008
        else:
            self.health = 2534

    def getTowerHealth(self):
        return self.health

enemPrincess0 = tower("enemPrincess0", 112, 7.5, {"air", "ground"}, (60, 140), (85, 160))
enemPrincess1 = tower("enemPrincess1", 112, 7.5, {"air", "ground"}, (310, 390), (85, 160))
enemKing = tower("enemKing", 90, 7, {"air", "ground"}, (185, 265), (35, 110))
princess0 = tower("princess0", 112, 7.5, {"air", "ground"}, (60, 140), (485, 560))
princess1 = tower("princess1", 112, 7.5, {"air", "ground"}, (310, 390), (485, 560))
king = tower("king", 90, 7, {"air", "ground"}, (185, 265), (535, 610))

# attempt at adding one troop to a field of cards
# name, rarity, elixir, radius, targets, dps, health, attacktype
giant = troop("Giant", "rare", 5, 5, {"tower"}, 400, 250, "singular", 15, "tan", 1, 1, 0)
goblins = troop("Goblins", "common", 2, 15, {"ground"}, 100, 40, "singular", 8, "green", 2.35, 3, 30)
archers = troop("Archers", "common", 3, 25, {"air", "ground"}, 90, 45, "singular", 8, "pink", 2, 2, 30)
wizard = troop("Wizard", "rare", 5, 45, {"ground"}, 150, 170, "splash", 9, "sky blue", 2, 1, 40)
knight = troop("Knight", "common", 3, 5, {"ground"}, 100, 500, "singular", 9, "silver", 2, 1, 25)
prince = troop("Prince", "epic", 5, 5, {"ground"}, 250, 400, "singular", 10, "gold", 2.25, 1, 50)
skeletons = troop("Skeletons", "common", 1, 5, {"ground"}, 50, 25, "singular", 7, "gray", 2.35, 3, 25)
minions = troop("Minions", "common", 3, 15, {"air", "ground"}, 150, 40, "singular", 8, "blue", 2.35, 3,25) 
sparky = troop("Sparky", "legendary", 6, 50, {"ground"}, 500, 450, "splash", 13, "red", 1.25, 1, 50) 
fireball = spell("Fireball", "rare", 4, 75, {"air", "ground"}, 150, 1) 
zap = spell("Zap", "common", 2, 50, {"air", "ground"}, 90, 0.5) 
hog = troop("Hog", "rare", 4, 5, {"tower"}, 220, 600, "singular", 11, "brown", 2.5, 1, 0) 


def appStarted(app):
    # Idea/Lines from 112 Course Notes, Animations Part 4
    # sprite from https://www.pngfind.com/mpng/iRwboR_8-bit-fire-ball-hd-png-download/
    #app.fireballSprite = app.scaleImage(app.loadImage('fireballsprite.png'), 0.08)
    # sprite from https://www.vhv.rs/viewpic/hoRib_minecraft-lightning-pixel-art-hd-png-download/
    #app.zapSprite = app.scaleImage(app.loadImage('zapsprite.png'), 0.01)
    app.sprites = []
    app.enemTowersDead = 0
    app.towersDead = 0
    app.shownEndMessage = False
    app.timerCount = 0
    app.endgame = False
    app.winner = ""
    # list of all characters on field
    app.troops = []
    app.towerAttacks = []
    app.oppTowerAttacks = []
    app.elixirCount = 0
    app.oppTroops= []
    # starting elixir
    app.elixir = 6
    app.attacks = []
    app.oppAttacks = []
    app.oppElixir = 6
    app.hitTroop = False
    app.oppHitTroop = False
    app.definedTroops = [giant, goblins, archers, wizard, knight, prince, skeletons, minions, sparky, fireball, zap, hog]
    app.towers = [enemPrincess0, enemPrincess1, princess0, princess1]
    for tower in app.towers:
        tower.health = 2534
    app.playableCards = [] 
    app.cardsAvailable = ["Giant", "Goblins", "Archers", "Wizard", "Knight", "Prince", "Skeletons"
                        ,"Minions", "Sparky", "Fireball", "Zap", "Hog"]
    app.deck = [([""] * 4) for r in range(2)]
    app.buttonCoord = (75, 10, 375, 300) 
    app.time = 150 # seconds
    app.gameState = False
    app.play = False
    app.deckBuilt = None
    app.deckRandomized = False
    app.timerDelay = 100 
    app.troopBeingPlaced = ""
    playButton = 'https://i.redd.it/31i7x4db1qwy.png'
    app.playButton = app.scaleImage(app.loadImage(playButton), 0.5)
    app.oppKnowledge = set()
    app.oppDeck = set()
    app.oppPlayableCards = []
    app.leftEnem = True
    app.rightEnem = True
    app.left = True
    app.right = True
    app.resetGame = False

# somewhat remembered from recitation??
def flatten(oglist):
    if oglist == []:
        return oglist
    if isinstance(oglist[0], list):
         return flatten(oglist[0]) + flatten(oglist[1:])
    return oglist[:1] + flatten(oglist[1:])

# attackingmethod
def updateAttacks(app):
    for attack in app.attacks:
        if attack.cy < enemPrincess0.yRange[1] + 2 * attack.radius:
            if attack.cx < 225:
                targetTower = enemPrincess0
            else:
                targetTower = enemPrincess1
            targetTower.health -= attack.dps/8
            app.attacks.remove(attack)
            if targetTower.health <= 0:
                if targetTower.name == "princess0":
                    app.leftEnem = False
                elif targetTower.name == "princess1":
                    app.rightEnem = False
                elif targetTower.name == "enemPrincess0":
                    app.left = False
                elif targetTower.name == "enemPrincess1":
                    app.right = False 
        else:
            attack.cy -= attack.speed

    for attack in app.towerAttacks:
        for troop in app.troops:
            if intersects(troop.cx, troop.cy, troop.circleR, attack.cx, attack.cy, attack.radius):
                app.towerAttacks.remove(attack)
                troop.takeDamage(attack.dps/10)
                app.hitTroop == True
                break
        if app.hitTroop == False:
            if attack.slope != None:
                attack.cx -= attack.slope/abs(attack.slope)
                attack.cy += abs(attack.slope)
            else:
                attack.cy += attack.speed/4.5
        app.hitTroop == False
    
    for attack in app.oppAttacks:
        if attack.cy > princess0.yRange[0] - 2 * attack.radius:
            if attack.cx < 225:
                targetTower = princess0
            else:
                targetTower = princess1
            targetTower.health -= attack.dps/8
            app.oppAttacks.remove(attack)
            if targetTower.health <= 0:
                if targetTower.name == "princess0":
                    app.leftEnem = False
                elif targetTower.name == "princess1":
                    app.rightEnem = False
                elif targetTower.name == "enemPrincess0":
                    app.left = False
                elif targetTower.name == "enemPrincess1":
                    app.right = False 
        else:
            attack.cy += attack.speed

    for attack in app.oppTowerAttacks:
        for troop in app.oppTroops:
            if intersects(troop.cx, troop.cy, troop.circleR, attack.cx, attack.cy, attack.radius):
                app.oppTowerAttacks.remove(attack)
                troop.takeDamage(attack.dps/10)
                app.oppHitTroop == True
                break
        if app.oppHitTroop == False:
            if attack.slope != None:
                attack.cx -= attack.slope/abs(attack.slope)
                attack.cy -= abs(attack.slope)
            else:
                attack.cy -= attack.speed/4.5
        app.oppHitTroop == False
            
def intersects(x0, y0, r0, x1, y1, r1):
    if distance(x0, y0, x1, y1) < (r0 + r1) * 1.2: # trying to get rid of small shooting errors
        return True

def towerIsAttacking(tower, towerAttackList):
    for attack in towerAttackList:
        if attack.troop == tower.name:
            return True
    return False

def towerAttack(tower, troop, app, user):
    if user == "user":
        towerAttackList = app.towerAttacks
        yCoord = 1
    else:
        towerAttackList = app.oppTowerAttacks
        yCoord = 0
    if not towerIsAttacking(tower, towerAttackList):
        if user == "user":
            towerStart = 1
        else:
            towerStart = 0
        cx = (tower.xRange[1]+tower.xRange[0])/2
        xdir = (cx - troop.cx)
        ydir = abs(tower.yRange[towerStart] - troop.cy)
        try:
            slope = ydir/xdir
        except:
            slope = None
        attacking = attack(tower.name, cx, tower.yRange[yCoord], "black", tower.dps, tower.radius, slope, tower.name)
        towerAttackList.append(attacking)
        
def checkWinCPU(app):
    for tower in app.towers:
        if tower.name.startswith("p"):
            if tower.getTowerHealth() > 0:
              return False
    return True

def checkWin(app):
    for tower in app.towers:
        if tower.name.startswith("enem"):
            if tower.getTowerHealth() > 0:
                return False
    return True  

def win(app):
    win = checkWin(app)
    cpuWin = checkWinCPU(app)
    if win == True:
        app.endgame, app.winner = True, "User"
    elif cpuWin == True:
        app.endgame, app.winner = True, "CPU"

def removeStrayBullets(app):
    for attack in app.towerAttacks:
        # 140 is right side of bridge + 10 and 60 is left side of bridge - 10
        if attack.towerOrigin == "enemPrincess0":
            if attack.cx > 140 or attack.cy > 290 or attack.cx < 60:
                app.towerAttacks.remove(attack)
        elif attack.towerOrigin == "enemPrincess1":
            if attack.cx < 310 or attack.cy > 290 or attack.cx > 370:
                app.towerAttacks.remove(attack)
    for attack in app.oppTowerAttacks:
        if attack.towerOrigin == "princess0":
             if attack.cx > 140 or attack.cy < 360 or attack.cx < 60:
                app.oppTowerAttacks.remove(attack)
        elif attack.towerOrigin == "princess1":
             if attack.cx < 310 or attack.cy < 360 or attack.cx > 370:
                app.oppTowerAttacks.remove(attack)

def endgame(app):
    if app.winner == "CPU":
        app.showMessage("You Lose! Your opponent took down both of your towers :(")
        decision = app.getUserInput("Would you like to play again (Yes/No)?")
        if decision.lower() == "yes":
            app.resetGame = True 
        else:
            sys.exit()
    elif app.winner == "User":
        app.showMessage("You Win! You took down both of your opponent's towers :)")
        decision = app.getUserInput("Would you like to play again (Yes/No)?")
        if decision.lower() == "yes":
            app.resetGame = True 
        else:
            sys.exit()

def removeSpells(app):
    for i in range (len(app.sprites)):
        sprite, cx, cy, drawTime = app.sprites[i]
        if drawTime < 5:
            app.sprites[i] =  sprite, cx, cy, drawTime + 1
        else:
            app.sprites.pop(i)

def timerFired(app):
    print(app.oppDeck)
    win(app)
    if app.resetGame:
        appStarted(app)
    elif app.time <= 0:
        lifeDrain(app)
    elif app.endgame:
        endgame(app)
    removeStrayBullets(app)
    removeSpells(app)
    app.timerCount += 1
    if app.gameState == True:
        if len(app.oppDeck) == 8: 
            oppMove(app)
            updateOppTroops(app)
        updateTroops(app)
        updateAttacks(app)
        app.elixirCount += 0.1
        if len(app.playableCards) == 0:
            # creates random starting deck for opp
            while len(app.oppDeck) < 8:
                i = random.randint(0, len(app.cardsAvailable) - 1)
                app.oppDeck.add(app.cardsAvailable[i])
            app.oppDeck = list(app.oppDeck)
            # also creates random startng hands
            while len(app.playableCards) < 4 or len(app.oppPlayableCards) < 4: 
                i = random.randint(0, 7)
                card = app.deck[i]
                oppCard = app.oppDeck[i]
                if not card in app.playableCards:
                    app.playableCards.append(card)
                    app.deck.append(card)
                    app.deck.remove(card)
                if not oppCard in app.oppPlayableCards:
                    app.oppPlayableCards.append(oppCard)
                    app.oppDeck.append(oppCard)
                    app.oppDeck.remove(oppCard)
            app.deckRandomized = True
        if almostEqual(app.elixirCount % 1, 0):
            app.time -= 1
        if app.elixir < 10 and almostEqual(app.elixirCount % 2, 0) and app.elixirCount != 0:
            app.elixir += 1
        if app.oppElixir < 10 and almostEqual(app.elixirCount % 2, 0) and app.elixirCount != 0:
            app.oppElixir += 1

# try and show life draining on towers
def lifeDrain(app):
    minTowerHealth = 4008
    losingTower = None
    for tower in app.towers:
        if tower.getTowerHealth() <= 0:
            if tower.name == "princess0" or tower.name == "princess1":
                app.towersDead += 1
            elif tower.name == "enemPrincess0" or tower.name == "enemPrincess1":
                app.enemTowersDead += 1
    if app.towersDead == app.enemTowersDead:
        for tower in app.towers:
            if tower.getTowerHealth() < minTowerHealth and tower.getTowerHealth() > 0:
                minTowerHealth = tower.getTowerHealth()
                losingTower = tower
    elif app.towersDead > app.enemTowersDead:
        for tower in app.towers:
            if tower.name.startswith("p") and tower.getTowerHealth() <= 0:
                losingTower = tower
                minTowerHealth = tower.getTowerHealth
    else:
        for tower in app.towers:
            if tower.name.startswith("enem") and tower.getTowerHealth() <= 0:
                losingTower = tower
                minTowerHealth = tower.getTowerHealth
    if losingTower.name == "princess0" or losingTower.name == "princess1" and app.shownEndMessage == False:
        app.shownEndMessage = True
        health = losingTower.getTowerHealth()
        if health < 0:
            health = 0
        app.showMessage(f"You Lose! Your tower had the the least HP of all towers, with {health} HP :(")
        decision = app.getUserInput("Would you like to play again (Yes/No)?")
        if decision.lower() == "yes":
            app.resetGame = True
        else:
            sys.exit()
    elif losingTower.name == "enemPrincess0" or losingTower.name == "enemPrincess1" and app.shownEndMessage == False:
        app.shownEndMessage = True
        health = losingTower.getTowerHealth()
        if health < 0:
            health = 0
        app.showMessage(f"You Win! Your opponents tower had the the least HP of all towers, with {health} HP :)")
        decision = app.getUserInput("Would you like to play again (Yes/No)?")
        if decision.lower() == "yes":
            app.resetGame = True
        else:
            sys.exit()

# AI turn
def oppMove(app):
    # each time the user places a card, that is stored in oppKnowledge
    card, placementState = cardDecision(app)
    if card == None:
        return
    newTroop = copy.deepcopy(card)
    if newTroop.elixir <= app.oppElixir:
        # will use the troop and either str defense or offense to determine placement
        newTroop.cx, newTroop.cy = generateLocation(app, placementState)
        if newTroop.cx < app.width/2 and app.leftEnem == False:
            newTroop.cx = app.width - newTroop.cx
        elif newTroop.cx > app.width/2 and app.rightEnem == False:
            newTroop.cx = app.width - newTroop.cx
        check = locationCheck(app)
        if check == "playRight" and app.rightEnem:
            newTroop.cx = random.randint(260, 420)
        elif check == "playLeft" and app.leftEnem:
            newTroop.cx = random.randint(30, 190)
        if isinstance(newTroop, spell):
            targetTower, targetTower.cx, targetTower.cy = findLowestTowerHealth("enemy") #return coordinates later if necessary
            targetTower.health -= newTroop.damage
            if newTroop.name == "Fireball":
                        sprite = app.fireballSprite
                        cx = targetTower.cx
                        cy = targetTower.cy
                        app.sprites.append((sprite, cx, cy, 0))
            elif newTroop.name == "Zap":
                        sprite = app.zapSprite
                        cx = targetTower.cx
                        cy = targetTower.cy
                        app.sprites.append((sprite, cx, cy, 0))
            if targetTower.health <= 0:
                if targetTower.name == "princess0":
                    app.leftEnem = False
                elif targetTower.name == "princess1":
                    app.rightEnem = False
                elif targetTower.name == "enemPrincess0":
                    app.left = False
                elif targetTower.name == "enemPrincess1":
                    app.right = False 
        else:
            app.oppTroops.append(newTroop)
            app.oppElixir -= newTroop.elixir
        index = app.oppPlayableCards.index(newTroop.name)
        app.oppPlayableCards[index] = app.oppDeck[3]
        app.oppDeck.remove(newTroop.name)
        app.oppDeck.insert(0, newTroop.name)
        for tower in app.towers:
            print(f'{tower.name} has {tower.getTowerHealth()} HP')
        print(f'Opponent played {newTroop.name} at x: {newTroop.cx} , y: {newTroop.cy}')
        print(f"Opponent's current elixir: {app.oppElixir}")
        print("-------------------------------------")
                
def findLowestTowerHealth(spellUser):
    if spellUser == "enemy":
        bestHealth = 3000
        bestTower = None
        for tower in [princess0, princess1]:
            if tower.getTowerHealth() <= bestHealth:
                bestTower = tower
                bestHealth = tower.getTowerHealth()
        cx = (bestTower.xRange[0] + bestTower.xRange[1]) / 2
        cy = (bestTower.yRange[0] + bestTower.yRange[1]) / 2
        return bestTower, cx, cy 

def locationCheck(app):
    rightCount = 0
    leftCount = 0
    for troop in app.oppTroops:
        if troop.cx > 225:
            rightCount += 1
        else:
            leftCount += 1
    if rightCount > 3 * leftCount:
        return "playLeft"
    elif leftCount > 3 * rightCount:
        return "playRight"
    else:
        return None 

def generateLocation(app, state):
    if state == "offense":
        towerHP = 3000
        weakestTower = None
        for tower in app.towers:
            if tower.name.startswith("princess"):
                if tower.getHealth() < towerHP:
                    towerHP = tower.getTowerHealth()
                    weakestTower = tower
        if weakestTower.name.endswith("0") and weakestTower.getTowerHealth() < 1000:
            return random.randint(40, 100), 270
        elif weakestTower.name.endswith("1") and weakestTower.getTowerHealth() < 1000:
            return random.randint(350, 410), 270 
        elif weakestTower.name.endswith("0"):
            return random.randint(40, 100), 200
        else:
            return random.randint(350, 410), 200
    elif state == "neutral":
        towerHP = 3000
        weakestTower = None
        for tower in app.towers:
            if tower.name.startswith("princess"):
                if tower.getHealth() < towerHP:
                    towerHP = tower.getHealth()
                    weakestTower = tower
        if weakestTower.name.endswith("0"):
            if app.time < 120:
                y0 = 40
            else:
                y0 = 20
            return random.randint(40, 100), random.randint(y0, 60)
        else:
            if app.time < 120:
                y0 = 40
            else:
                y0 = 20
            return random.randint(350, 410), random.randint(y0, 60)
    else:
        towerHP = 3000
        weakestTower = None
        for tower in app.towers:
            if tower.name.startswith("enemPrincess"):
                if tower.getHealth() < towerHP:
                    towerHP = tower.getHealth()
                    weakestTower = tower
        if weakestTower.name.endswith("0"):
            return 40, 175
        else:
            return 40, 175
    # states are str neutral, offense, defense
    # check other troop positions and tower healths

# opp picks what card they want
def cardDecision(app):
    state = 0
    for trooop in app.troops:
        newTroop = findTroop(app, trooop.name)
        if isinstance(trooop, spell):
            continue
        if "tower" in trooop.targets: # represents game scenario, 20 assigned if there is a tower seeking card
            state -= 20  
        if not isinstance(trooop, spell) and trooop.getHealth() < 0.5*(newTroop.getHealth()): # lower health troops mean less defense
            state -= 5
        else:
            state +=5
        if trooop.elixir < app.oppElixir // 2: # if the troop cost is inexpensive, play it
            state += 3
        else:
            state -= 3
        if not isinstance(trooop, spell) and trooop.dps >= 80:
            state += 7
        if len(app.troops) > 4:
            state -= 8
        else:
            state += 1  
    if princess0.getTowerHealth() < 1700: # go on the offensive
        state += 10 
        for card in app.oppPlayableCards:
            newCard = findTroop(app, card)
            if isinstance(newCard, spell):
                return newCard, "offense"
    elif princess1.getTowerHealth() < 1700:
        for card in app.oppPlayableCards:
            newCard = findTroop(app, card)
            if isinstance(newCard, spell):
                return newCard, "offense"
        state += 10
    elif enemPrincess0.getTowerHealth() < 500: # play defense
        state -= 7
    elif enemPrincess1.getTowerHealth() < 500:
        state -= 7
    for card in app.oppPlayableCards:
        newTroop = findTroop(app, card)
        if state < 0 and not isinstance(newTroop, spell) and newTroop.dps > 50 and "ground" in newTroop.targets:
            return newTroop, "defense"
        elif state > 10 and not isinstance(newTroop, spell) and ("tower" in newTroop.targets or newTroop.dps > 75):
            return newTroop, "offense"
    # checking which card is cheapest if no card can be formulated
    # cycle weak cards is a key strat in CR
    bestElixir = 10
    bestCard = ""
    for card in app.oppPlayableCards:
        newTroop = findTroop(app, card)
        if not isinstance(newTroop, spell) and newTroop.elixir <= bestElixir:
            bestElixir = newTroop.elixir
            bestCard = newTroop
    if len(app.troops) < 2 and app.oppElixir < 10:
        return None, "neutral"
    return bestCard, "neutral"

# Taken from https://www.cs.cmu.edu/~112/notes/notes-variables-and-functions.html
def almostEqual(x, y):
    return abs(x - y) < 0.1

def distance(x0, y0, x1, y1):
    return ((x1-x0)**2 + (y1-y0)**2)**(1/2)

def towerNameToTower(name, app):
    for tower in app.towers:
        if tower.name == name:
            return tower
    return None

def findTower(troop, user):
    if user == "opp":
        if troop.cx < 225:
            return princess0
        else:
            return princess1
    else:
        if troop.cx < 225:
            return enemPrincess0
        else:
            return enemPrincess1

def updateOppTroops(app):
    i = 0
    while i < len(app.oppTroops):
        troop = app.oppTroops[i]
        if isinstance(troop, spell):
            continue
        elif troop.getHealth() <= 0: #make this less than
            app.oppTroops.pop(i)
            tower = findTower(troop, "opp")
            tower.target = None
            i -= 1
        else:
            # if there is a troop nearby then pause all troop movement, fight troop, and if target is dead then unpause movement
            # if not then keep moving towards tower
            if troop.status == "moving":
                moveOppTroop(troop, app)
            # if at tower then attack tower
            else:
                if troop.status == "stationary":
                    seen = set()
                    for oppTroop in app.oppTroops:
                        if oppTroop.name in seen:
                            continue
                        if oppTroop != troop and oppTroop.status == "stationary" and almostOverlapping(troop.cx, oppTroop.cx):
                            seen.add(oppTroop.name)
                            tower = findTower(troop, "opp")
                            if troop.cx < oppTroop.cx and troop.cx - troop.speed > tower.xRange[0]:
                                troop.cx -= troop.speed
                            elif troop.cx < oppTroop.cx and oppTroop.cx + oppTroop.speed < tower.xRange[1]:
                                oppTroop.cx += oppTroop.speed
                            elif troop.cx > oppTroop.cx and troop.cx + troop.speed < tower.xRange[1]:
                                troop.cx += troop.speed
                            elif troop.cx > oppTroop.cx and oppTroop.cx - oppTroop.speed > tower.xRange[0]:
                                oppTroop.cx -= oppTroop.speed
                    if troop.cx < 225 and princess0.getTowerHealth() <= 0:
                        app.oppTroops.pop(i)
                        if (app.oppElixir + 1 < 10):
                            app.oppElixir += 1
                    elif troop.cx > 225 and princess1.getTowerHealth() <= 0:
                        app.oppTroops.pop(i)
                        if (app.oppElixir + 1 < 10):
                            app.oppElixir += 1
                moveOppTroop(troop, app)
                if not isAttacking(troop, app.oppAttacks):
                    # troop.radius/5 is attack speed
                    attacking = attack(troop.name, troop.cx, troop.cy, troop.color, troop.dps, troop.radius/4, 0, None)
                    app.oppAttacks.append(attacking)
        i += 1

def almostOverlapping(x, y):
    if abs(x - y) < 5:
        return True

# takes care of all troop actions
def updateTroops(app):
    i = 0
    while i < len(app.troops):
        troop = app.troops[i]
        if isinstance(troop, spell):
            continue
        elif not isinstance(troop, spell) and troop.getHealth() <= 0: #make this less than
            app.troops.pop(i)
            tower = findTower(troop, "user")
            tower.target = None
            i -= 1
        else:
            # if there is a troop nearby then pause all troop movement, fight troop, and if target is dead then unpause movement
            # if not then keep moving towards tower
            if troop.status == "moving":
                moveTroop(troop, app)
            # if at tower then attack tower
            else:
                if troop.status == "stationary":
                    seen = set()
                    for otherTroop in app.troops:
                        if otherTroop.name in seen:
                            continue
                        if otherTroop != troop and otherTroop.status == "stationary" and almostOverlapping(troop.cx, otherTroop.cx):
                            seen.add(otherTroop.name)
                            tower = findTower(troop, "user")
                            if troop.cx < otherTroop.cx and troop.cx - troop.speed > tower.xRange[0]:
                                troop.cx -= troop.speed
                            elif troop.cx < otherTroop.cx and otherTroop.cx + otherTroop.speed < tower.xRange[1]:
                                otherTroop.cx += otherTroop.speed
                            elif troop.cx > otherTroop.cx and troop.cx + troop.speed < tower.xRange[1]:
                                troop.cx += troop.speed
                            elif troop.cx > otherTroop.cx and otherTroop.cx - otherTroop.speed > tower.xRange[0]:
                                otherTroop.cx -= otherTroop.speed
                    if troop.cx < 225 and enemPrincess0.getTowerHealth() <= 0:
                        app.troops.pop(i)
                        if (app.elixir + 1 < 10):
                            app.elixir += 1
                    elif troop.cx > 225 and enemPrincess1.getTowerHealth() <= 0:
                        app.troops.pop(i)
                        if app.elixir + 1 < 10:
                            app.elixir += 1
                moveTroop(troop, app)
                if not isAttacking(troop, app.attacks):
                    # troop.radius/5 is attack speed
                    attacking = attack(troop.name, troop.cx, troop.cy, troop.color, troop.dps, troop.radius/4, 0, None)
                    app.attacks.append(attacking)
        i += 1

def moveOppTroop(troop, app):
    if troop.cx < 225 and troop.cy < 485 - troop.circleR - troop.radius: #attacking left tower
        movedX = moveOppX(troop, enemPrincess0, 70, 130)
        if troop.cy > 360 and princess0.target == None: # the 360 is when it crosses the bridge
            princess0.target = troop.name
            towerAttack(princess0, troop, app, "enem")
        elif princess0.target == troop.name:
            towerAttack(princess0, troop, app, "enem")
        if not movedX:
            troop.cy += troop.speed
        elif troop.cy > enemPrincess0.yRange[1] and troop.cy + troop.circleR < 290:
            troop.cy += troop.speed
    elif troop.cx > 225 and troop.cy < 485 - troop.circleR - troop.radius: #attacking right tower
        movedX = moveOppX(troop, enemPrincess1, 320, 380)
        if troop.cy > 360 and princess1.target == None:
            princess1.target = troop.name
            towerAttack(princess1, troop, app, "enem")
        elif princess1.target == troop.name:
            towerAttack(princess1, troop, app, "enem")
        if not movedX:
            troop.cy += troop.speed
        elif troop.cy > enemPrincess1.yRange[1] and troop.cy + troop.circleR < 290:
            troop.cy += troop.speed
    else:
        troop.status = "stationary"
        if troop.cx < 225: targetTower = princess0
        else: targetTower = princess1
        towerAttack(targetTower, troop, app, "enem")

def moveOppX(troop, userTower, bridgex0, bridgex1):
    if troop.cy < userTower.yRange[1] + 2 * troop.circleR:
        if troop.cx - troop.circleR * 2 > userTower.xRange[1]:
            troop.cx -= troop.speed
            return True
        elif troop.cx + troop.circleR * 2 < userTower.xRange[0]:
            troop.cx += troop.speed
            return True
        elif (userTower.xRange[0] < troop.cx + troop.circleR) and (troop.cx - troop.circleR < userTower.xRange[1]):
            if userTower == enemPrincess0: troop.cx += troop.speed
            else: troop.cx -= troop.speed
            return True
        return False
    elif (troop.cy + troop.circleR >= 290) and ((troop.cx + troop.circleR < bridgex0) or (troop.cx - troop.circleR > bridgex1)):
        if troop.cx - troop.circleR < bridgex0:
            troop.cx += troop.speed
            return True
        elif troop.cx + troop.circleR > bridgex1:
            troop.cx -= troop.speed
            return True
        return False
    else:
        if troop.cx + troop.circleR > bridgex1:
            troop.cx -= troop.speed
            return True
        elif troop.cx - troop.circleR < bridgex0:
            troop.cx += troop.speed
            return True
        return False

def isAttacking(troop, attackList):
    for attack in attackList:
        if attack.troop == troop.name:
            return True
    return False

def moveTroop(troop, app):
    if troop.cx < 225 and troop.cy > 160 + troop.circleR + troop.radius: #attacking left tower
        movedX = moveX(troop, princess0, 70, 130)
        if troop.cy < 290 and enemPrincess0.target == None:
            enemPrincess0.target = troop.name
            towerAttack(enemPrincess0, troop, app, "user")
        elif enemPrincess0.target == troop.name:
            towerAttack(enemPrincess0, troop, app, "user")
        if not movedX:
            troop.cy -= troop.speed
        elif troop.cy < princess0.yRange[0] and troop.cy - troop.circleR > 360:
            troop.cy -= troop.speed
    elif troop.cx > 225 and troop.cy > 160 + troop.circleR + troop.radius: #attacking right tower
        movedX = moveX(troop, princess1, 320, 380)
        if troop.cy < 290 and enemPrincess1.target == None:
            enemPrincess1.target = troop.name
            towerAttack(enemPrincess1, troop, app, "user")
        elif enemPrincess1.target == troop.name:
            towerAttack(enemPrincess1, troop, app, "user")
        if not movedX:
            troop.cy -= troop.speed
        elif troop.cy < princess1.yRange[0] and troop.cy - troop.circleR > 360:
            troop.cy -= troop.speed
    else:
        troop.status = "stationary"
        if troop.cx < 225: targetTower = enemPrincess0
        else: targetTower = enemPrincess1
        towerAttack(targetTower, troop, app, "user")

def moveX(troop, userTower, bridgex0, bridgex1):
    if troop.cy > userTower.yRange[0] - 2 * troop.circleR:
        if troop.cx - troop.circleR * 2 > userTower.xRange[1]:
            troop.cx -= troop.speed
            return True
        elif troop.cx + troop.circleR * 2 < userTower.xRange[0]:
            troop.cx += troop.speed
            return True
        elif (userTower.xRange[0] < troop.cx + troop.circleR) and (troop.cx - troop.circleR < userTower.xRange[1]):
            if userTower == princess0: troop.cx += troop.speed
            else: troop.cx -= troop.speed
            return True
        return False
    elif (troop.cy - troop.circleR <= 360) and ((troop.cx + troop.circleR < bridgex0) or (troop.cx - troop.circleR > bridgex1)):
        if troop.cx - troop.circleR < bridgex0:
            troop.cx += troop.speed
            return True
        elif troop.cx + troop.circleR > bridgex1:
            troop.cx -= troop.speed
            return True
        return False
    else:
        if troop.cx + troop.circleR > bridgex1:
            troop.cx -= troop.speed
            return True
        elif troop.cx - troop.circleR < bridgex0:
            troop.cx += troop.speed
            return True
        return False

def playGame(app, canvas):
    canvas.create_rectangle(0, 0, 450, 750, fill = "pale green")
    # draws deck grid
    canvas.create_rectangle(0, 650, 90, 750, width = 3, fill = "coral")
    canvas.create_rectangle(90, 650, 180, 750, width = 3, fill = "sky blue")
    canvas.create_rectangle(180, 650, 270, 750, width = 3, fill = "sky blue")
    canvas.create_rectangle(270, 650, 360, 750, width = 3, fill = "sky blue")
    canvas.create_rectangle(360, 650, 450, 750, width = 3, fill = "sky blue")
    # draws bridge (can put this over tkinter version later)
    #canvas.create_image(225, 325, image=ImageTk.PhotoImage(app.scaleImage(app.clashBridge, 1/2)))
    canvas.create_rectangle(70, 290, 130, 360, fill = "brown", width = 0)
    canvas.create_rectangle(320, 290, 380, 360, fill = "brown", width = 0)
    # lists playable cards
    for i in range(len(app.playableCards)):
        troop = findTroop(app, app.playableCards[i])
        canvas.create_text(135 + 90*i, 700, text = app.playableCards[i], font = "comic 11 bold")
        canvas.create_text(135 + 90*i, 725, text = troop.elixir, font = "comic 11 bold")
        canvas.create_text(45, 680, text = "Next Card", font = "comic 11 bold")
    if app.deckRandomized:
        troop = findTroop(app, app.deck[3])
        canvas.create_text(45, 700, text = app.deck[3], font = "comic 11 bold")
        canvas.create_text(45, 725, text = troop.elixir, font = "comic 11 bold")

    # draw 4 life bars for princess towers
    for i in range(2):
        # x0, y0 is a constant, while x1 and y1 are relative to health
        if i == 0:
            enemTower = enemPrincess0
            tower = princess0
        else:
            enemTower = enemPrincess1
            tower = princess1
        if enemTower.getTowerHealth() > 0:
            x1 = (250*i + 75) + 50*(enemTower.getTowerHealth()/2534)
            canvas.create_rectangle(250*i + 75, 70, 250*i + 125, 80, width = 3)
            canvas.create_rectangle(250*i + 75, 70, x1, 80, fill = "red")
        if tower.getTowerHealth() > 0:
            x1 = (250*i + 75) + 50*(tower.getTowerHealth()/2534)
            canvas.create_rectangle(250*i + 75, 470, 250*i + 125, 480, width = 3)
            canvas.create_rectangle(250*i + 75, 470, x1, 480, fill = "red")

    # creates towers
    if enemPrincess0.getTowerHealth() > 0:
        canvas.create_polygon(75, 85, 125, 85, 140, 160, 60, 160, width = 2, fill = "grey")
    if enemPrincess1.getTowerHealth() > 0:
        canvas.create_polygon(325, 85, 375, 85, 390, 160, 310, 160, width = 2, fill = "grey")
    # if enemKing.getTowerHealth() != 0:
    #     canvas.create_polygon(200, 35, 250, 35, 265, 110, 185, 110, width = 2, fill = "gold")
    if princess0.getTowerHealth() > 0:
        canvas.create_polygon(75, 485, 125, 485, 140, 560, 60, 560, width = 2, fill = "grey")
    if princess1.getTowerHealth() > 0:
        canvas.create_polygon(325, 485, 375, 485, 390, 560, 310, 560, width = 2, fill = "grey")
    # if king.getTowerHealth() != 0:
    #     canvas.create_polygon(200, 535, 250, 535, 265, 610, 185, 610, width = 2, fill = "gold")

    canvas.create_text(390, 20, text = f'Time: {app.time} s', font = "Arial 13 bold")
    canvas.create_text(390, 600, text = f'Elixir: {app.elixir}', font = "Arial 13 bold", fill = "purple")

    # drawing troops that user has on board
    for troop in app.troops:
        if isinstance(troop, spell) == False:
            r = troop.circleR
            cx = troop.cx
            cy = troop.cy
            for card in app.definedTroops:
                if card.name == troop.name:
                    health = card.health
                    canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill = troop.color)
                    canvas.create_rectangle(cx-r, cy-r-8, cx+r, cy-r-2)
                    canvas.create_rectangle(cx-r, cy-r-8, (cx-r) + (2*r)*(troop.getHealth()/health), cy-r-2, fill = "purple")
    
    for troop in app.oppTroops:
        if isinstance(troop, spell) == False:
            r = troop.circleR
            cx = troop.cx
            cy = troop.cy
            for card in app.definedTroops:
                if card.name == troop.name:
                    health = card.health
                    canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill = troop.color)
                    canvas.create_rectangle(cx-r, cy-r-8, cx+r, cy-r-2)
                    canvas.create_rectangle(cx-r, cy-r-8, (cx-r) + (2*r)*(troop.getHealth()/health), cy-r-2, fill = "hot pink")

    for attack in app.attacks:
        cx = attack.cx
        cy = attack.cy
        r = attack.radius
        canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill = attack.color)
    
    for attack in app.towerAttacks:
        tower = towerNameToTower(attack.towerOrigin, app)
        if tower.getTowerHealth() > 0:
            cx = attack.cx
            cy = attack.cy
            r = attack.radius
            canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill = attack.color)

    for attack in app.oppAttacks:
        cx = attack.cx
        cy = attack.cy
        r = attack.radius
        canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill = attack.color)
    
    for attack in app.oppTowerAttacks:
        tower = towerNameToTower(attack.towerOrigin, app)
        if tower.getTowerHealth() > 0:
            cx = attack.cx
            cy = attack.cy
            r = attack.radius
            canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill = attack.color)
    
    for i in range (len(app.sprites)):
        sprite, cx, cy, drawTime = app.sprites[i]
        canvas.create_image(cx, cy, image=ImageTk.PhotoImage(sprite))        

def mousePressed(app, event):
    # this dictates what happens on the main screen during the deck builder
    if not app.gameState:
        if (event.x < app.buttonCoord[2] and event.x > app.buttonCoord[0] 
            and event.y < app.buttonCoord[3] and event.y > app.buttonCoord[1]):
            if not contains(app, ""):
                app.gameState = True
                app.deckBuilt = True
                app.deck = flatten(app.deck)
            else:
                app.deckBuilt = False
        (row, col) = getCell(app, event.x, event.y, 375, 2) # this line is a continuation of the notes' getCell
        if ((row, col) != (-1, -1)):
            troop = app.getUserInput("What troop do you want to add to your deck?")
            if troop != None:
                troop = troop.lower().capitalize()
                if not troop in app.cardsAvailable:
                    app.showMessage(f'{troop} is not a valid troop name.')
                elif contains(app, troop):
                    app.showMessage(f'{troop} is already in your deck.')
                else:
                    app.deck[row][col] = troop
                    app.showMessage(f'You added the {troop} to your deck.')
    else:
        if event.y > 650 and event.y < 750: # this if statement is if a card is being chose from the hand
            if event.x > 90 and event. x < 180:
                app.troopBeingPlaced = app.playableCards[0]
            if event.x > 180 and event. x < 270:
                app.troopBeingPlaced = app.playableCards[1]
            if event.x > 270 and event. x < 360:
                app.troopBeingPlaced = app.playableCards[2]
            if event.x > 360 and event. x < 450:
                app.troopBeingPlaced = app.playableCards[3]
        # this is used if a card is selected and the mouse is clicked on field
        elif (event.y < 650 and app.troopBeingPlaced != "" and 
            (app.troopBeingPlaced in app.playableCards) and notOnTower(event.x, event.y)):  # change 360 because spells can go father
            troop = findTroop(app, app.troopBeingPlaced) # procures object troop
            if troop.elixir <= app.elixir:
                onTower, targetTower = onEnemyTower(event.x, event.y, "cpu")
                if isinstance(troop, spell) and onTower:
                    if troop.name == "Fireball":
                        sprite = app.fireballSprite
                        cx = event.x
                        cy = event.y
                        app.sprites.append((sprite, cx, cy, 0))
                    elif troop.name == "Zap":
                        sprite = app.zapSprite
                        cx = event.x
                        cy = event.y
                        app.sprites.append((sprite, cx, cy, 0))
                    targetTower.health -= troop.damage
                    if targetTower.health <= 0:
                        if targetTower.name == "princess0":
                            app.leftEnem = False
                        elif targetTower.name == "princess1":
                            app.rightEnem = False
                        elif targetTower.name == "enemPrincess0":
                            app.left = False
                        elif targetTower.name == "enemPrincess1":
                            app.right = False 
                    app.elixir -= troop.elixir
                    index = app.playableCards.index(app.troopBeingPlaced)
                    app.playableCards[index] = app.deck[3]
                    app.deck.remove(app.troopBeingPlaced)
                    app.deck.insert(0, app.troopBeingPlaced)
                    app.oppKnowledge.add(troop)
                elif event.y > 360:
                    troop.cx = event.x
                    troop.cy = event.y
                    if event.x > app.width/2 and app.right == False:
                        pass
                    elif event.x < app.width/2 and app.left == False:
                        pass
                    else:
                        app.troops.append(troop)
                        app.elixir -= troop.elixir
                        index = app.playableCards.index(app.troopBeingPlaced)
                        app.playableCards[index] = app.deck[3]
                        app.deck.remove(app.troopBeingPlaced)
                        app.deck.insert(0, app.troopBeingPlaced)
                        app.oppKnowledge.add(troop)
    
def onEnemyTower(x, y, enemy):
    if enemy == "cpu": # the user is placing a spell
        if enemPrincess0.xRange[0] < x < enemPrincess0.xRange[1] and enemPrincess0.yRange[0] < y < enemPrincess0.yRange[1]:
            return True, enemPrincess0
        elif enemPrincess1.xRange[0] < x < enemPrincess1.xRange[1] and enemPrincess1.yRange[0] < y < enemPrincess1.yRange[1]:
            return True, enemPrincess1
        else:
            return False, None
    else: # fill this code in for AI using spell on our towers
        pass

def notOnTower(x, y):
    if princess0.xRange[0] < x < princess0.xRange[1] and princess0.yRange[0] < y < princess0.yRange[1]:
        return False
    elif princess1.xRange[0] < x < princess1.xRange[1] and princess1.yRange[0] < y < princess1.yRange[1]:
        return False
    #elif king.xRange[0] < x < king.xRange[1] and king.yRange[0] < y < king.yRange[1]:
    #    return False
    return True
        
            
# this will return the troop as an object so that it can be drawn on the board
def findTroop(app, troopName):
    for troop in app.definedTroops:
        if troop.name == troopName:
            newTroop = copy.deepcopy(troop)
            return newTroop
    return None

# Checks if the troop a user has attempted to add is already in their deck
def contains(app, troop):
    for r in range(len(app.deck)):
        for c in range(len(app.deck[0])):
            if app.deck[r][c] == troop:
                return True
    return False

# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
def pointInGrid(x, y, topOfGrid):
    return ((0 <= x <= 450) and (topOfGrid <= y <= 750))
    
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
def getCell(app, x, y, topOfGrid, colNum):
    if (not pointInGrid(x, y, topOfGrid)):
        return (-1, -1)
    cellWidth  = app.width / 4
    cellHeight = (app.height - topOfGrid) / colNum
    row = int((y - topOfGrid) / cellHeight)
    col = int(x / cellWidth)
    return (row, col)

# Taken from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
def getCellBounds(app, row, col):
    margin = app.height/2
    cellWidth = app.width / 4
    cellHeight =  app.height / 4
    x0 = col * cellWidth
    x1 = (col+1) * cellWidth
    y0 = margin + row * cellHeight
    y1 = margin + (row+1) * cellHeight
    return (x0, y0, x1, y1)

def redrawAll(app, canvas):
    # make game state false when ready to start game
    if app.gameState == False:
        # Play button and cards available listed if game hasn't started
        canvas.create_rectangle(0, 0, 450, 750, fill = "royal blue")
        canvas.create_image(225, 115, image=ImageTk.PhotoImage(app.playButton))
        canvas.create_text(225, 115, text = "BATTLE", font = "comic 36 bold")
        canvas.create_text(225, 265, text = "Click on the grid slots and choose cards from the list below!", font = "comic 11 bold")
        i = 0
        for r in range(4):
            for c in range(3):
                canvas.create_text(75 + 100*r, 300 + 20*c, text = app.cardsAvailable[i], font = "comic 9 bold")
                i += 1
        # Deck builder Image at bottom
        for row in range(2):
            for col in range(4):
                (x0, y0, x1, y1) = getCellBounds(app, row, col)
                canvas.create_rectangle(x0, y0, x1, y1, width = 3)
        # stops user from entering game without full deck
        if app.deckBuilt == False:
            canvas.create_text(225, 230, text = "Create a deck of 8 cards before going into battle!",
                                                                                        font = "comic 12 bold")
        # displays current deck user has built
        for r in range(len(app.deck)):
            for c in range(len(app.deck[0])):
                if app.deck[r][c] != "":
                    canvas.create_rectangle(c*app.width/4, app.height/2 + r*app.height/4, c*app.width/4 + app.width/4, app.height/2 + r*app.height/4 + app.height/4, fill = "goldenrod") 
                    canvas.create_text(app.width/8 + c*app.width/4, 5*app.height/8 + r*app.height/4, text = app.deck[r][c], font = "comic 11 bold")
    else:
        playGame(app, canvas)   
    
runApp(width=450, height=750)