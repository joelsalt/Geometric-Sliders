# Joel Milligan, 2014

import pygame, random, sys, time
from pygame.locals import *

FPS = 15
WINWIDTH = 1200
WINHEIGHT = 600
BOXSIZE = 30
NEWENEMYTIME = 5 #(seconds). Make a new enemy after this amount of time
MOVETIME = 0.5 #(seconds). Move the enemy after this amount of time
INVULTIME = 1.5 #(seconds). Make the player vulnerable after this amount of time
BULLETTIME = 0.5#(seconds). Make a new bullet after this time
assert WINWIDTH % BOXSIZE == 0, 'Window width must be a multiple of boxsize'
assert WINHEIGHT % BOXSIZE == 0, 'Window height must be a multiple of boxsize'
GRIDWIDTH = int(WINWIDTH / BOXSIZE)
GRIDHEIGHT = int(WINHEIGHT / BOXSIZE)
#...

#colors       R    G    B
WHITE      = (255, 255, 255)
BLACK      = (  0,   0,   0)
LIGHTGREY  = ( 80,  80,  80)
GREY       = ( 40,  40,  40)
DARKGREY   = ( 20,  20,  20)
RED        = (255,   0,   0)
DARKRED    = (100,   0,   0)
YELLOW     = (255, 255,   0)
MEDYELLOW  = (150, 150,   0)
DARKYELLOW = (100, 100,   0)
GREEN      = (  0, 255,   0)
MEDGREEN   = (  0, 170,   0)
DARKGREEN  = (  0, 100,   0)
LIGHTBLUE  = (  0, 255, 255)
MEDBLUE    = (  0, 170, 170)
BLUE       = (  0,   0, 255)
DARKBLUE   = (  0,   0, 100)
PURPLE     = (255,   0, 255)
DARKPURPLE = (100,   0, 100)
#...

#Set up color names
BGCOLOR = BLACK
LINECOLOR = LIGHTGREY
RECTICLECOLOR = PURPLE

LIGHTCOLORS = [RED, YELLOW, GREEN, BLUE, PURPLE]
DARKCOLORS  = [DARKRED, DARKYELLOW, DARKGREEN, DARKBLUE, DARKPURPLE]
assert len(LIGHTCOLORS) == len(DARKCOLORS), 'LIGHTCOLORS and DARKCOLORS must be the same length'

#Set up sound effects
pygame.mixer.pre_init(frequency=22050, size=-16, channels=16, buffer=512)
pygame.mixer.init()
upgradePickupSound = pygame.mixer.Sound('upgradepickupsound.wav')
#startScreenSound = pygame.mixer.Sound('startscreensound.wav')
#startScreenSound.set_volume(0.4)
startGameSound = pygame.mixer.Sound('startgamesound.wav')
channel1 = pygame.mixer.Channel(0)
enemyDeathSound = pygame.mixer.Sound('enemydeathsound.wav')
turret2EnergySound = pygame.mixer.Sound('turret2energy.wav')
turret2EnergySound.set_volume(0.5)
channel3 = pygame.mixer.Channel(3)
turret3BounceSound = pygame.mixer.Sound('turret3bounce.wav')
turret4ChargeSound = pygame.mixer.Sound('turret4charge.wav')
turret4LazerSound = pygame.mixer.Sound('turret4lazer.wav')
playerBulletSound = pygame.mixer.Sound('playerbulletsound.wav')
channel2 = pygame.mixer.Channel(2)
playerBulletSound.set_volume(0.7)
healthDamageSound = pygame.mixer.Sound('healthdamagesound.wav')
healthDamageSound.set_volume(0.45)
forwardSound = pygame.mixer.Sound('forwardsound.wav')
forwardSound.set_volume(0.7)
backwardSound = pygame.mixer.Sound('backwardsound.wav')
backwardSound.set_volume(0.5)
deathSound = pygame.mixer.Sound('deathsound.wav')
shipDamageSound = pygame.mixer.Sound('shipdamage.wav')

pygame.mixer.music.load('theGreatVoid.mp3')
pygame.mixer.music.set_volume(0.6)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'


def main():
    global fpsClock, windowSurface, GAMEFONT, BIGFONT, SMALLFONT, \
           TINYFONT, playerRect, newPlayerImage, \
           hBulletImage1, vBulletImage1, hBulletImage2, vBulletImage2, \
           hBulletImage3, vBulletImage3, hBulletImage4, vBulletImage4, \
           turret1Bullet, turret3Bullet, turret4Bullet,\
           firstTurretImage, secondTurretImage, thirdTurretImage, fourthTurretImage, \
           energyUpgrade, turretUpgrade, shipUpgrade, healthUpgrade, speedUpgrade, spawnUpgrade, \
           energyRect, turretRect, shipRect, healthRect, speedRect, spawnRect, \
           upImage, upgradeImage, topImage, bottomImage, \
           topGreyImage, bottomGreyImage, topRect, bottomRect
    
    #Set up images/imgRects
    playerImage = loadImage('newspaceship.png')
    newPlayerImage = pygame.transform.scale(playerImage, (BOXSIZE, BOXSIZE))
    playerRect = newPlayerImage.get_rect()

    turret1Bullet = loadImage('bullet1.png')
    turret3Bullet = loadImage('bullet3.png')
    turret4Bullet = loadImage('bullet4.png')

    hBulletImage1 = loadImage('playerbullet.png')
    hBulletImage2 = loadImage('playerbullet2.png')
    hBulletImage3 = loadImage('playerbullet3.png')
    hBulletImage4 = loadImage('playerbullet4.png')
    vBulletImage1 = pygame.transform.rotate(hBulletImage1, 90)
    vBulletImage2 = pygame.transform.rotate(hBulletImage2, 90)
    vBulletImage3 = pygame.transform.rotate(hBulletImage3, 90)
    vBulletImage4 = pygame.transform.rotate(hBulletImage4, 90)

    firstTurretImage = loadImage('turret1.png')
    secondTurretImage = loadImage('turret2.png')
    thirdTurretImage = loadImage('turret3.png')
    fourthTurretImage = loadImage('turret4.png')

    upImage = loadImage('upgrade.png')
    upgradeImage = pygame.transform.scale(upImage, (BOXSIZE, BOXSIZE))

    top = loadImage('tophalfupgrade.png')
    bottom = loadImage('bottomhalfupgrade.png')
    topGrey = loadImage('tophalfgreyupgrade.png')
    bottomGrey = loadImage('bottomhalfgreyupgrade.png')

    topImage = pygame.transform.scale(top, (BOXSIZE*4, BOXSIZE*2))
    bottomImage = pygame.transform.scale(bottom, (BOXSIZE*4, BOXSIZE*2))
    topGreyImage = pygame.transform.scale(topGrey, (BOXSIZE*4, BOXSIZE*2))
    bottomGreyImage = pygame.transform.scale(bottomGrey, (BOXSIZE*4, BOXSIZE*2))

    topRect = topImage.get_rect()
    bottomRect = bottomImage.get_rect()

    topRect.midbottom = (1110, (WINHEIGHT / 2))
    bottomRect.midtop = (1110, (WINHEIGHT / 2) + 1)

    energyUpgrade = loadImage('energyupgrade.png')
    turretUpgrade = loadImage('turretupgrade.png')
    shipUpgrade = loadImage('shipupgrade.png')
    healthUpgrade = loadImage('healthupgrade.png')
    speedUpgrade = loadImage('speedupgrade.png')
    spawnUpgrade = loadImage('spawnupgrade.png')

    energyRect = energyUpgrade.get_rect()
    turretRect = turretUpgrade.get_rect()
    shipRect = shipUpgrade.get_rect()
    healthRect = energyUpgrade.get_rect()
    speedRect = speedUpgrade.get_rect()
    spawnRect = spawnUpgrade.get_rect()

    energyRect.center = (1110, (3*BOXSIZE)-(BOXSIZE/2))
    turretRect.center = (1110, (5*BOXSIZE)-(BOXSIZE/2))
    shipRect.center = (1110, (7*BOXSIZE)-(BOXSIZE/2))
    healthRect.center = (1110, ((GRIDHEIGHT-6)*BOXSIZE)-(BOXSIZE/2))
    speedRect.center = (1110, ((GRIDHEIGHT-4)*BOXSIZE)-(BOXSIZE/2))
    spawnRect.center = (1110, ((GRIDHEIGHT-2)*BOXSIZE)-(BOXSIZE/2))

    

    pygame.init()
    fpsClock = pygame.time.Clock()
    windowSurface = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
    GAMEFONT = pygame.font.SysFont('coure', 40)
    BIGFONT = pygame.font.SysFont('coure', 80)
    SMALLFONT = pygame.font.SysFont('coure', 20)
    TINYFONT = pygame.font.SysFont('coure', 50)
    pygame.display.set_caption('Geometric Sliders')
    pygame.mouse.set_visible(False)


    startScreen()


def runGame():
    #Set up the player start point
    startx = random.randint(30, 37)
    starty = random.randint(3, GRIDHEIGHT - 3)
    playerCoords = {'x': startx, 'y': starty}

    drawBox = False

    health = 15
    energy = 100
    maxEnergy = 100

    #Set up the variables the player can upgrade
    variables  = [3,             0.4,         1,            1,           0.5,      3]            
    #variables = [energyPerKill, bulletSpeed, playerDamage, enemyHealth, MOVETIME, spawnRate]

    playerBulletImages = [[hBulletImage1, vBulletImage1], [hBulletImage2, vBulletImage2], \
                          [hBulletImage3, vBulletImage3], [hBulletImage4, vBulletImage4]]
    currentBullet = 0

    wave = 1
    level = 1
    waveTime = time.time()
    secondsBetweenWaves = 5
    numOfWavesInLevel = 5
    waveHasStarted = False
    enemiesMade = 0
    maxNumOfEnemies = 0

    firstTurretCost = 15
    secondTurretCost = 0
    thirdTurretCost = 40
    fourthTurretCost = 55

    upgradeCoords = {'x': 7, 'y': (random.randint(0, (GRIDHEIGHT-1)))}
    upgradeRect = pygame.Rect(upgradeCoords['x']*BOXSIZE, \
                                upgradeCoords['y']*BOXSIZE, \
                                BOXSIZE, BOXSIZE)

    makeBullet = False
    upgradeOnScreen = False
    pickedUpUpgrade = False
    showPlayer = True
    invulnerable = False
    invulStartTime = 0

    enemies = []
    bullets = []
    turrets = []
    turretBullets = []

    makeEnemyTime = time.time()
    moveEnemyTime = time.time()
    nextBulletTime = time.time()

    moveLeft = False
    moveRight = False
    moveUp = False
    moveDown = False

    devMode = False

    currentDir = UP

    while True:
        if health <= 0:
            gameOver()

        energyPerKill = variables[0]
        bulletSpeed = variables[1] #(Seconds)
        playerDamage = variables[2] #Amount of health (in units) that the player bullets do
        enemyHealth = variables[3]
        MOVETIME = variables[4]    
        spawnRate = variables[5]
        
        if invulnerable and time.time() - invulStartTime > INVULTIME:
            invulnerable = False
            showPlayer = True

        maxNumOfEnemies = calculateNumOfEnemies(wave, level)
        
        checkForQuit()
        #Set up keyboard input
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key in (K_UP, K_w):
                    moveDown = False
                    moveUp = True
                elif event.key in (K_DOWN, K_s):
                    moveUp = False
                    moveDown = True
                elif event.key in (K_LEFT, K_a):
                    moveRight = False
                    moveLeft = True
                elif event.key in (K_RIGHT, K_d):
                    moveLeft = False
                    moveRight = True
                elif event.key == K_SPACE:
                    makeBullet = True

                # devMode buttons
                #Add a 'speed up' button
                elif event.key == K_x and devMode:
                    MOVETIME = 0

            elif event.type == KEYUP:
                if event.key in (K_UP, K_w):
                    moveUp = False
                elif event.key in (K_DOWN, K_s):
                    moveDown = False
                elif event.key in (K_LEFT, K_a):
                    moveLeft = False
                elif event.key in (K_RIGHT, K_d):
                    moveRight = False
                elif event.key == K_SPACE:
                    makeBullet = False

                elif event.key in (K_ESCAPE, K_TAB):
                    pauseScreen()
                    if not waveHasStarted:
                        waveTime = time.time()
                    
                elif event.key == K_F7:
                    devMode = not devMode

                elif event.key == K_1:
                    if energy >= firstTurretCost:
                        energy -= addTurret(turrets, playerCoords, 1, bulletSpeed, firstTurretCost)
                elif event.key == K_2:
                    energy -= addTurret(turrets, playerCoords, 2, bulletSpeed, secondTurretCost)
                elif event.key == K_3:
                    if energy >= thirdTurretCost:
                        energy -= addTurret(turrets, playerCoords, 3, bulletSpeed, thirdTurretCost)
                elif event.key == K_4:
                    if energy >= fourthTurretCost:
                        turret4ChargeSound.play()
                        energy -= addTurret(turrets, playerCoords, 4, bulletSpeed, fourthTurretCost)

                # devMode buttons
                #Add a 'spawn enemy' button
                elif event.key == K_z and devMode:
                    makeEnemy(enemies, enemyHealth)
                #Reset 'speed up'
                elif event.key == K_x and devMode:
                    MOVETIME = 0.5
                #Add a 'reset health' button
                elif event.key == K_c and devMode:
                    health = 10
                #Add a 'reset energy' button
                elif event.key == K_v and devMode:
                    energy = 100
                elif event.key == K_n and devMode:
                    if not waveHasStarted:
                        wave += 1
                    else:
                        enemies = []
                        enemiesMade = maxNumOfEnemies
                        waveTime = time.time()
                elif event.key == K_l and devMode:
                    level += 1
                    enemies = []
                elif event.key == K_p and devMode:
                    firstSelection = []
                    secondSelection = []

        #Move the player and face them in a new direction
        if moveUp and playerCoords['y'] > 0:
            playerCoords['y'] -= 1
            currentDir = UP
        if moveDown and playerCoords['y'] < GRIDHEIGHT - 1:
            playerCoords['y'] += 1
            currentDir = DOWN
        if moveLeft and playerCoords['x'] > 0:
            playerCoords['x'] -= 1
            currentDir = LEFT
        if moveRight and playerCoords['x'] < GRIDWIDTH - 1:
            playerCoords['x'] += 1
            currentDir = RIGHT
            
        #Make the bullets
        if makeBullet and not invulnerable and time.time() - nextBulletTime > BULLETTIME:
            channel2.play(playerBulletSound)
            newBullet = {'x': playerCoords['x'],
                        'y': playerCoords['y'],
                         'type': 0,
                        'dir': currentDir}
            if newBullet['dir'] == UP:
                newBullet['surface'] = pygame.transform.flip(playerBulletImages[currentBullet][1], False, True)
            elif newBullet['dir'] == DOWN:
                newBullet['surface'] = playerBulletImages[currentBullet][1]
            elif newBullet['dir'] == RIGHT:
                newBullet['surface'] = pygame.transform.flip(playerBulletImages[currentBullet][0], True, False)
            else:
                newBullet['surface'] = playerBulletImages[currentBullet][0]
            bullets.append(newBullet)
            #Add a 'rect' and a 'surface' when drawing the bullet
            nextBulletTime = time.time()

        #Remove enemies that go past the edge/damage the player
        for e in enemies:
            if e['x'] > GRIDWIDTH - 1:
                healthDamageSound.play()
                enemies.remove(e)
                health -= 1
            #Remove turrets if an enemy hits them
            for t in turrets:
                if e['x'] == t['x'] and e['y'] == t['y']:
                    turrets.remove(t)
            #Remove the bullets as they come into contact with the enemies
            for b in bullets:
                if (b['x'] == e['x'] and b['y'] == e['y']) or \
                   ((b['x'] - 1) == e['x'] and b['y'] == e['y']):
                    e['health'] -= playerDamage
                    if b in bullets:
                        bullets.remove(b)
            #Remove the turret bullets if they contact the enemies
            for t in turretBullets:
                #Type 1 bullets. Remove as they come into contact with the enemy
                if t['type'] == 1:
                    if (t['x'] == e['x'] and t['y'] == e['y']) or \
                       ((t['x'] - 1) == e['x'] and t['y'] == e['y']):
                        e['health'] -= 1
                        if t in turretBullets:
                            turretBullets.remove(t)
                #Type 3 bullets. Bounce the enemy 6 squares back
                if t['type'] == 3:
                    if (t['x'] - 1) == e['x'] and t['y'] == e['y']:
                        turret3BounceSound.play()
                        e['x'] -= 15
                #Type 4 bullets. Damage all squares in contact  
                if t['type'] == 4:
                    if t['x'] == e['x'] and t['y'] == e['y']:
                        e['health'] -= 1
            #Remove any "dead" enemies
            if e['health'] <= 0:
                enemyDeathSound.play()
                enemies.remove(e)
                if energy < 100:
                    energy += ((e['color'] - 1) + energyPerKill)
            #The player has been hit. Flash the image
            if (playerCoords['x'] == e['x'] and playerCoords['y'] == e['y']) and not invulnerable:
                shipDamageSound.play()
                invulnerable = True
                invulStartTime = time.time()
                if energy <= 10:
                    energy = 0
                else:
                    energy -= 10
        for t in turrets:
            if t['bullettype'] == 2:
                if time.time() - t['lastbullet'] > t['newbullet']:
                    drawBox = not drawBox
                    t['lastbullet'] = time.time()
                    if (playerCoords['x'] == t['x'] and playerCoords['y'] == t['y']):
                        if energy < 100:
                            channel3.play(turret2EnergySound)
                            energy += 2

        #Check if the player made it past wave 3
        if len(enemies) == 0 and wave == 3 and enemiesMade == maxNumOfEnemies \
           and waveHasStarted and not pickedUpUpgrade:
            upgradeOnScreen = True

        #The player has picked up the upgrade, show the upgrade screen
        if playerCoords['x'] == upgradeCoords['x'] and playerCoords['y'] == upgradeCoords['y'] and \
           upgradeOnScreen:
            upgradePickupSound.play()
            upgradeOnScreen = False
            pickedUpUpgrade = True
            firstSelection = []
            secondSelection = []

        #Check if the player has survived the wave 
        if len(enemies) == 0 and enemiesMade == maxNumOfEnemies and \
           waveHasStarted and not pickedUpUpgrade:
            if not upgradeOnScreen:
                channel1.play(startGameSound)
                waveHasStarted = False
                waveTime = time.time()
                enemiesMade = 0
                wave += 1
                if wave > 3:
                    wave = 1
                    level += 1

        windowSurface.fill(BGCOLOR)

        drawBullet(bullets)
        drawBullet(turretBullets)
        #Draw the 'charge bar' for the lazer turrets
        for t in turrets:
            if t['bullettype'] == 4:
                if not t['fullcharge']:
                    if time.time() - t['chargetime'] > t['charge']:
                        t['fullcharge'] = True
                        turret4LazerSound.play()
                    else:
                        pygame.draw.line(windowSurface, YELLOW, \
                                ((t['x']*BOXSIZE)+1, (t['y']*BOXSIZE)+1),
                                ((t['x']*BOXSIZE)+((time.time() - t['chargetime'])*10), \
                                 (t['y']*BOXSIZE)+1), 1)
                else:
                    pygame.draw.line(windowSurface, YELLOW, \
                                ((t['x']*BOXSIZE)+1, (t['y']*BOXSIZE)+1),
                                ((t['x']*BOXSIZE)+30, (t['y']*BOXSIZE)+1), 1)
        if upgradeOnScreen:
            windowSurface.blit(upgradeImage, upgradeRect)
        drawTurret(turrets, turretBullets)
        drawGrid()

        if devMode:
            devText, devRect = makeText('devMode:ON', SMALLFONT, BLUE, BLACK)
            devRect.midleft = (15, WINHEIGHT - 15)
            windowSurface.blit(devText, devRect)
        
        drawRecticle(playerCoords)

        if time.time() - waveTime > secondsBetweenWaves:
            if time.time() - makeEnemyTime > (NEWENEMYTIME - (wave/spawnRate)) and enemiesMade < maxNumOfEnemies:
                makeEnemy(enemies, enemyHealth)
                enemiesMade += 1
                makeEnemyTime = time.time()
                waveHasStarted = True
        else:
            #Draw the bar that increases until the next wave
            HALFWINWIDTH = WINWIDTH / 2
                
            pygame.draw.rect(windowSurface, GREY, (HALFWINWIDTH - 56, \
                                                    WINHEIGHT - 22, 112, 18), 3)
            pygame.draw.rect(windowSurface, LIGHTGREY, \
                            (HALFWINWIDTH - 53, WINHEIGHT - 20, 106, 14), 3)
            pygame.draw.rect(windowSurface, RED, \
                            (HALFWINWIDTH - 50, WINHEIGHT - 18, (time.time() - waveTime)*20, 10))
            pygame.draw.rect(windowSurface, DARKRED, \
                            (HALFWINWIDTH - 50, WINHEIGHT - 11, (time.time() - waveTime)*20, 3))
            pygame.draw.line(windowSurface, WHITE, \
                             (HALFWINWIDTH - 45, WINHEIGHT - 17), (HALFWINWIDTH + 42, WINHEIGHT - 17), 1)

        if time.time() - moveEnemyTime > MOVETIME:
            moveEnemy(enemies)
            moveEnemyTime = time.time()

        #Toggle drawing the player if they've been hit
        if invulnerable:
            showPlayer = not showPlayer

        if drawBox:
            for t in turrets:
                if t['bullettype'] == 2:
                    pygame.draw.rect(windowSurface, LIGHTBLUE, \
                                 (t['x']*BOXSIZE, t['y']*BOXSIZE, BOXSIZE+1, BOXSIZE+1), 1)
            
        drawEnemy(enemies)
        turnedPlayerImage = turnPlayer(currentDir)
        drawPlayer(playerCoords, turnedPlayerImage, showPlayer)
        drawWaveAndLevel(wave, level)
        drawHealth(health)
        drawEnergy(energy, maxEnergy)

        #Draw the upgrade screen until the player makes two choices
        if pickedUpUpgrade:
            pickedUpUpgrade, currentBullet = drawUpgradeScreen(playerCoords, bullets, currentBullet, variables, firstSelection, secondSelection)
            if not pickedUpUpgrade:
                wave += 1
                

        pygame.display.update()
        fpsClock.tick(FPS)


def terminate():
    pygame.mixer.quit()
    pygame.quit()
    sys.exit()


def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
        pygame.event.post(event)


def waitForKeyPress():
    while True:
        checkForQuit()
        for event in pygame.event.get():
            if event.type == KEYUP:
                return


def loadImage(name): #Next time, add the following line: image.get_rect()
                     # and return the rect
    image = pygame.image.load(name)
    image.set_colorkey(BGCOLOR)
    return image


def makeText(text, font, color, bgcolor=None):
    if bgcolor == None:
        surf = font.render(text, True, color)
    else:
        surf = font.render(text, True, color, bgcolor)
    return surf, surf.get_rect()


def calculateNumOfEnemies(wave, level):
    return ((wave + level) + 5)


def drawUpgradeScreen(playerCoords, bullets, currentBullet, variables, firstSelection, secondSelection):
    #Draw the upgrade screen
    pygame.draw.rect(windowSurface, BLACK, (1020, BOXSIZE, 180, WINHEIGHT-60))

    upgrades = [energyRect, turretRect, shipRect, healthRect, speedRect, spawnRect]
    changes = [1, -0.1, 2, 1, -0.1, -1]

    #Draw a recticle around the players choice
    for u in upgrades:
        if ((playerCoords['y']*BOXSIZE)+(BOXSIZE/2)) == u.centery and \
           u.top < WINHEIGHT/2 and not firstSelection:
            pygame.draw.rect(windowSurface, DARKBLUE, \
                             (u.left - 5, u.top - 5, u.width + 10, u.height + 10), 4)

        if ((playerCoords['y']*BOXSIZE)+(BOXSIZE/2)) == u.centery and \
           u.top > WINHEIGHT/2 and not secondSelection:
            pygame.draw.rect(windowSurface, DARKRED, \
                             (u.left - 5, u.top - 5, u.width + 10, u.height + 10), 4)
        #Add the player's choices to a list
        for b in bullets:
            if b in bullets:
                if b['rect'].colliderect(u) and u.top < WINHEIGHT/2 and not firstSelection:
                    firstSelection.append(u)
                if b['rect'].colliderect(u) and u.top > WINHEIGHT/2 and not secondSelection:
                    secondSelection.append(u)

    #Draw the colored in upgrade if the player hasn't made a choice
    if not firstSelection and not secondSelection:
        windowSurface.blit(topImage, topRect)
        windowSurface.blit(bottomImage, bottomRect)
    elif firstSelection and not secondSelection:
        windowSurface.blit(topGreyImage, topRect)
        windowSurface.blit(bottomImage, bottomRect)
    elif not firstSelection and secondSelection:
        windowSurface.blit(topImage, topRect)
        windowSurface.blit(bottomGreyImage, bottomRect)
    #The player has made their choices
    elif firstSelection and secondSelection:
        windowSurface.blit(topGreyImage, topRect)
        windowSurface.blit(bottomGreyImage, bottomRect)

        okayText, okayRect = makeText('Apply These Upgrades?', GAMEFONT, WHITE)
        okayRect.topright = ((GRIDWIDTH-6)*BOXSIZE, BOXSIZE)

        yesText, yesRect = makeText('Yes', TINYFONT, BLUE)
        yesRect.topright = ((GRIDWIDTH-6)*BOXSIZE, 7*BOXSIZE)

        noText, noRect = makeText('No', TINYFONT, RED)
        noRect.topright = ((GRIDWIDTH-6)*BOXSIZE, 12*BOXSIZE)

        #Draw the question to the screen
        windowSurface.blit(okayText, okayRect)
        windowSurface.blit(yesText, yesRect)
        windowSurface.blit(noText, noRect)

        #Check for the player's decision
        for b in bullets:
            if b in bullets:
                if b['rect'].colliderect(yesRect):
                    #Change the variables based on the player's input
                    if firstSelection[0] == upgrades[0]:
                        variables[0] += changes[0]
                    if firstSelection[0] == upgrades[1]:
                        variables[1] += changes[1]
                    if firstSelection[0] == upgrades[2]:
                        variables[2] += changes[2]
                        currentBullet += 1
                        if currentBullet > 3:
                            currentBullet = 3
                    if secondSelection[0] == upgrades[3]:
                        variables[3] += changes[3]
                        if variables[3] > 5:
                            variables[3] = 5
                    if secondSelection[0] == upgrades[4]:
                        variables[4] += changes[4]
                    if secondSelection[0] == upgrades[5]:
                        variables[5] += changes[5]
                    
                    return False, currentBullet
                if b['rect'].colliderect(noRect):
                    del firstSelection[0]
                    del secondSelection[0]
                    bullets.remove(b)
        
    pygame.draw.line(windowSurface, YELLOW, (1020, WINHEIGHT/2), (WINWIDTH, WINHEIGHT/2), 3)
    pygame.draw.rect(windowSurface, BLUE, (1020, BOXSIZE, 180, WINHEIGHT-60), 5)
    pygame.draw.rect(windowSurface, LIGHTBLUE, (1024, BOXSIZE+4, 172, WINHEIGHT - 68), 5)

    windowSurface.blit(energyUpgrade, energyRect)
    windowSurface.blit(turretUpgrade, turretRect)
    windowSurface.blit(shipUpgrade, shipRect)
    windowSurface.blit(healthUpgrade, healthRect)
    windowSurface.blit(speedUpgrade, speedRect)
    windowSurface.blit(spawnUpgrade, spawnRect)

    if firstSelection:
        pygame.draw.rect(windowSurface, BLUE, \
        (firstSelection[0].left - 5, firstSelection[0].top - 5, \
         firstSelection[0].width + 10, firstSelection[0].height + 10), 4)
    if secondSelection:
        pygame.draw.rect(windowSurface, RED, \
        (secondSelection[0].left - 5, secondSelection[0].top - 5, \
         secondSelection[0].width + 10, secondSelection[0].height + 10), 4)

    return True, currentBullet


def drawWaveAndLevel(wave, level):
    if wave == 4:
        wave = 'Test Wave'
    waveText, waveRect = makeText('Wave:%s' % (wave), SMALLFONT, WHITE)
    waveRect.bottomright = (WINWIDTH - 5, WINHEIGHT - 5)

    levelText, levelRect = makeText('Level:%s' % (level), SMALLFONT, WHITE)
    levelRect.bottomright = (WINWIDTH - 5, WINHEIGHT - 25)

    windowSurface.blit(waveText, waveRect)
    windowSurface.blit(levelText, levelRect)


def turnPlayer(currentDir):
    facingRight = pygame.transform.rotate(newPlayerImage, -90)
    facingLeft = pygame.transform.rotate(newPlayerImage, 90)
    facingDown = pygame.transform.flip(newPlayerImage, False, True)

    if currentDir == UP: #Reutrn the unchanged image in the 'UP' position
        return newPlayerImage
    if currentDir == DOWN:
        return facingDown
    if currentDir == LEFT:
        return facingLeft
    if currentDir == RIGHT:
        return facingRight


def drawPlayer(playerCoords, turnedPlayerImage, showPlayer):
    playerRect.left = playerCoords['x'] * int(BOXSIZE)
    playerRect.top = playerCoords['y'] * int(BOXSIZE)
    playerRect.width = BOXSIZE + 1
    playerRect.height = BOXSIZE + 1
    
    if showPlayer:
        windowSurface.blit(turnedPlayerImage, playerRect)

    pygame.draw.rect(windowSurface, RECTICLECOLOR, (playerRect.left, playerRect.top, playerRect.width, playerRect.height), 1)


def makeEnemy(enemies, enemyHealth):
    #Choose a random color for the enemy
    color = random.randint(0, enemyHealth-1)

    #Choose a random row to make the enemies on
    row = random.randint(0, GRIDHEIGHT-1)
    
    #Iterate through a random length and make a dict for each enemy square
    for i in range(random.randint(3, 5)):
        enemySquare = {'x':          -(i + 1),
                       'y':          row,
                       'lightcolor': LIGHTCOLORS[color],
                       'darkcolor':  DARKCOLORS[color],
                       'color':      color + 1,
                       'health':     (color + 1) * 5,
                       'size':       BOXSIZE
                       }
        enemies.append(enemySquare)


def moveEnemy(enemies):
    for e in enemies:
        e['x'] += 1


def drawEnemy(enemies):
    for e in enemies:
        xPos = e['x'] * BOXSIZE
        yPos = e['y'] * BOXSIZE

        pygame.draw.rect(windowSurface, e['darkcolor'], \
                        (xPos, yPos, e['size'], e['size']))
        pygame.draw.rect(windowSurface, e['lightcolor'], \
                        (xPos + 5, yPos + 5, \
                        e['size'] - 10, e['size'] - 10))


def drawHealth(health):
    color = GREEN
    darkColor = MEDGREEN
    #Draw the grey outline
    pygame.draw.rect(windowSurface, GREY, (WINWIDTH - 126, 4, 112, 18), 3)
    #Draw the inner outline
    pygame.draw.rect(windowSurface, LIGHTGREY, (WINWIDTH - 123, 6, 106, 14), 3)
    #Draw the health
    if health <= 9 and health >= 5:
        color = YELLOW
        darkColor = MEDYELLOW
    if health <= 4:
        color = RED
        darkColor = DARKRED
    if health <= 0:
        health = 0
    pygame.draw.rect(windowSurface, color, (WINWIDTH - 120, 8, (health*6.66), 10))
    pygame.draw.rect(windowSurface, darkColor, (WINWIDTH - 120, 15, (health*6.66), 3))

    #Draw the 'reflection'
    pygame.draw.line(windowSurface, WHITE, (WINWIDTH - 115, 10), (WINWIDTH - 100, 10), 1)


def drawEnergy(energy, maxEnergy):
    #Draw the grey outline
    pygame.draw.rect(windowSurface, GREY, (15, 4, maxEnergy + 12, 18), 3)
    #Draw the inner outline
    pygame.draw.rect(windowSurface, LIGHTGREY, (18, 6, maxEnergy + 6, 14), 3)
    #Draw the energy
    if energy <= 0:
        energy = 0
    pygame.draw.rect(windowSurface, LIGHTBLUE, (20, 8, energy, 10))
    pygame.draw.rect(windowSurface, MEDBLUE, (20, 15, energy, 3))

    #Draw the 'reflection'
    pygame.draw.line(windowSurface, WHITE, (100, 10), (115, 10), 1)


def addTurret(turrets, playerCoords, turretNum, bulletSpeed, cost):
    if turretNum == 1:
        newTurret = {}
        newTurret['x'] = playerCoords['x']
        newTurret['y'] = playerCoords['y']
        for t in turrets:
            if newTurret['x'] == t['x'] and newTurret['y'] == t['y']:
                del newTurret
                return 0
        newTurret['surface'] = firstTurretImage
        newTurret['bullettype'] = 1
        newTurret['bulletimage'] = turret1Bullet
        newTurret['lastbullet'] = time.time()
        newTurret['newbullet'] = bulletSpeed #(seconds)
        newTurret['turretstart'] = time.time()
        newTurret['turretend'] = 15 #(seconds)

        turrets.append(newTurret)
        return cost

    elif turretNum == 2:
        newTurret = {}
        newTurret['x'] = playerCoords['x']
        newTurret['y'] = playerCoords['y']
        for t in turrets:
            if newTurret['x'] == t['x'] and newTurret['y'] == t['y']:
                del newTurret
                return 0
            if t['bullettype'] == 2:
                del newTurret
                return 0
        newTurret['surface'] = secondTurretImage
        newTurret['bullettype'] = 2
        newTurret['lastbullet'] = time.time()
        newTurret['newbullet'] = 1 #(seconds)
        newTurret['turretstart'] = time.time()
        newTurret['turretend'] = 15 #(seconds)

        turrets.append(newTurret)
        return cost

    elif turretNum == 3:
        newTurret = {}
        newTurret['x'] = playerCoords['x']
        newTurret['y'] = playerCoords['y']
        for t in turrets:
            if newTurret['x'] == t['x'] and newTurret['y'] == t['y']:
                del newTurret
                return 0
        newTurret['surface'] = thirdTurretImage
        newTurret['bullettype'] = 3
        newTurret['bulletimage'] = turret3Bullet
        newTurret['lastbullet'] = time.time()
        newTurret['newbullet'] = bulletSpeed #(seconds)
        newTurret['turretstart'] = time.time()
        newTurret['turretend'] = 15 #(seconds)

        turrets.append(newTurret)
        return cost
    
    elif turretNum == 4:
        newTurret = {}
        newTurret['x'] = playerCoords['x']
        newTurret['y'] = playerCoords['y']
        for t in turrets:
            if newTurret['x'] == t['x'] and newTurret['y'] == t['y']:
                del newTurret
                return 0
        newTurret['surface'] = fourthTurretImage
        newTurret['bullettype'] = 4
        newTurret['bulletimage'] = turret4Bullet
        newTurret['lastbullet'] = time.time()
        newTurret['newbullet'] = bulletSpeed #(seconds)
        newTurret['turretstart'] = time.time()
        newTurret['turretend'] = 10 #(seconds)
        newTurret['charge'] = 3 #(seconds)
        newTurret['chargetime'] = time.time()
        newTurret['fullcharge'] = False

        turrets.append(newTurret)
        return cost


def drawTurret(turrets, turretBullets):
    for t in turrets:
        if t['bullettype'] == 1:
            #Shoot the next bullet when it is time
            if time.time() - t['lastbullet'] > t['newbullet']:
                turretBullets.append({'x': t['x'],
                                  'y': t['y'],
                                  'type': t['bullettype'],
                                  'dir': LEFT,
                                  'surface': t['bulletimage']})
                t['lastbullet'] = time.time()

        if t['bullettype'] == 3:
            #Make the 'bouncing' bullets
            if time.time() - t['lastbullet'] > t['newbullet'] * 4:
                turretBullets.append({'x': t['x'],
                                      'y': t['y'] - 1,
                                      'startcoord': t['y'],
                                      'type': t['bullettype'],
                                      'dir': UP,
                                      'lastmove': time.time(),
                                      'move': t['newbullet'] * 4,
                                      'surface': t['bulletimage']})
                turretBullets.append({'x': t['x'],
                                      'y': t['y'] + 1,
                                      'startcoord': t['y'],
                                      'type': t['bullettype'],
                                      'dir': DOWN,
                                      'lastmove': time.time(),
                                      'move': t['newbullet'] * 4,
                                      'surface': t['bulletimage']})
                t['lastbullet'] = time.time()
                
        if t['bullettype'] == 4 and t['fullcharge']:
            #Make the lazer bullets
            turretBullets.append({'x': t['x'],
                                  'y': t['y'],
                                  'type': t['bullettype'],
                                  'dir': LEFT,
                                  'surface': t['bulletimage']})
                
        #Remove the turret if it has been out for too long
        if time.time() - t['turretstart'] > t['turretend']:
            turrets.remove(t)

        xPos = t['x'] * BOXSIZE
        yPos = t['y'] * BOXSIZE

        t['rect'] = pygame.Rect(xPos, yPos, BOXSIZE, BOXSIZE)

        windowSurface.blit(t['surface'], t['rect'])


def drawBullet(bullets):
    for b in bullets:

        if b['type'] != 3:
            if b['dir'] == UP:
                b['y'] -= 1
            elif b['dir'] == DOWN:
                b['y'] += 1
            elif b['dir'] == LEFT:
                b['x'] -= 1
            elif b['dir'] == RIGHT:
                b['x'] += 1

        elif b['type'] == 3:
            if time.time() - b['lastmove'] > b['move']:
                b['lastmove'] = time.time()
                if b['dir'] == UP:
                    b['y'] -= 1
                    if b['y'] < b['startcoord'] - 3:
                        bullets.remove(b)
                if b['dir'] == DOWN:
                    b['y'] += 1
                    if b['y'] > b['startcoord'] + 3:
                        bullets.remove(b)

        bulletX = b['x'] * BOXSIZE
        bulletY = b['y'] * BOXSIZE
    
        if b['x'] < 0 or b['x'] > GRIDWIDTH or b['y'] < 0 or b['y'] > GRIDHEIGHT:
            if b in bullets:
                bullets.remove(b)

        if b in bullets:
            b['rect'] = pygame.Rect(bulletX, bulletY, BOXSIZE, BOXSIZE)
     
            windowSurface.blit(b['surface'], b['rect'])


def drawGrid():
    for x in range(0, WINWIDTH+1, BOXSIZE): #Vertical lines
        pygame.draw.line(windowSurface, LINECOLOR, (x, 0), (x, WINHEIGHT))
    for y in range(0, WINHEIGHT+1, BOXSIZE): #Horizontal lines
        pygame.draw.line(windowSurface, LINECOLOR, (0, y), (WINWIDTH, y))


def drawRecticle(playerCoords):
    gridSizeX = playerCoords['x'] * BOXSIZE
    gridSizeY = playerCoords['y'] * BOXSIZE
        
    #Vertical color line
    pygame.draw.line(windowSurface, RECTICLECOLOR, (0, (gridSizeY) + (BOXSIZE / 2)), \
                     ((GRIDWIDTH*BOXSIZE), (gridSizeY) + (BOXSIZE / 2)))

    #Horizontal color line
    pygame.draw.line(windowSurface, RECTICLECOLOR, ((gridSizeX) + (BOXSIZE / 2), 0), \
                     ((gridSizeX) + (BOXSIZE / 2), (GRIDHEIGHT*BOXSIZE)))


def pauseScreen():
    pygame.mixer.music.pause()
    pauseText, pauseRect = makeText('Paused', BIGFONT, random.choice(LIGHTCOLORS))
    pauseRect.center = (WINWIDTH/2, WINHEIGHT/3)

    windowSurface.blit(pauseText, pauseRect)
    pygame.display.update()
    waitForKeyPress()
    pygame.mixer.music.unpause()


def setupScreen(playerCoords, currentDir, enemies):
    #Turn the player based on the next possible direction
    lastPlayerMove = time.time()
    if currentDir == UP and playerCoords['y'] > 0:
        playerCoords['y'] -= 0.5
    elif currentDir == DOWN and playerCoords['y'] < GRIDHEIGHT-1:
        playerCoords['y'] += 0.5
    elif currentDir == LEFT and playerCoords['x'] > 0:
        playerCoords['x'] -= 0.5
    elif currentDir == RIGHT and playerCoords['x'] < GRIDWIDTH-1:
        playerCoords['x'] += 0.5
        
    #Set up the screen by drawing the background        
    windowSurface.fill(BGCOLOR)
    drawGrid()
    drawRecticle(playerCoords)
    drawEnemy(enemies)
    pygame.draw.rect(windowSurface, BGCOLOR, \
                    (BOXSIZE+1, BOXSIZE+1, \
                    (WINWIDTH-(BOXSIZE*2))-1, (WINHEIGHT-(BOXSIZE*2))-1))
    turnedPlayerImage = turnPlayer(currentDir)
    drawPlayer(playerCoords, turnedPlayerImage, True)


def startScreen():
    playerCoords = {'x': 0, 'y': 0}
    currentDir = RIGHT
    enemies = []
    COLOR1 = BLACK
    COLOR2 = random.choice(DARKCOLORS)
    lastEnemyTime = time.time()
    changeColorTime = time.time()
    NEWENEMYTIME = 1
    NEWCOLORTIME = 0.55
    choice = 1
    titleColor = random.choice(LIGHTCOLORS)
    startColor = random.choice(LIGHTCOLORS)

    start = True
    howToPlay = False
    options = False

    pygame.mixer.music.play(-1, 0.0)
    while True:
        checkForQuit()
        
        #if time.time() - changeColorTime > NEWCOLORTIME:
         #   COLOR1, COLOR2 = COLOR2, COLOR1
          #  changeColorTime = time.time()

        if not howToPlay:
            for event in pygame.event.get():
                if event.type == KEYUP:
                    if start:
                        #startScreenSound.play()
                        forwardSound.play()
                        start = False
                    elif event.key in (K_UP, K_w) and not start and choice > 1:
                        backwardSound.play()
                        choice -= 1
                    elif event.key in (K_DOWN, K_s) and not start and choice < 3:
                        forwardSound.play()
                        choice += 1
                    elif event.key in (K_RETURN, K_SPACE):
                        if choice == 1:
                            startGameSound.play()
                            runGame()
                        elif choice == 2:
                            howToPlay = True
                            choice = 1
                        elif choice == 3:
                            terminate()

        #Change player direction if they reach the edge
        if currentDir == UP and (playerCoords['x'] == 0 and playerCoords['y'] == 0):
            currentDir = RIGHT
        if currentDir == RIGHT and (playerCoords['x'] == GRIDWIDTH-1 and playerCoords['y'] == 0):
            currentDir = DOWN
        if currentDir == DOWN and (playerCoords['x'] == GRIDWIDTH-1 and playerCoords['y'] == GRIDHEIGHT-1):
            currentDir = LEFT
        if currentDir == LEFT and (playerCoords['x'] == 0 and playerCoords['y'] == GRIDHEIGHT-1):
            currentDir = UP

        #Add a new enemy at a random location
        if time.time() - lastEnemyTime > NEWENEMYTIME:
            color = random.randint(0, len(LIGHTCOLORS)-1)
            enemySquare = {'x':          random.randint(0, GRIDWIDTH-1),
                       'y':          random.randint(0, GRIDHEIGHT-1),
                       'lightcolor': LIGHTCOLORS[color],
                       'darkcolor':  DARKCOLORS[color],
                       'health':     (color + 1) * 5,
                       'size':       BOXSIZE
                       }
            enemies.append(enemySquare)
            lastEnemyTime = time.time()

        for e in enemies:
            if playerCoords['x'] == e['x'] and playerCoords['y'] == e['y']:
                titleColor = e['lightcolor']
                startColor = e['lightcolor']
                if COLOR1 != BLACK:
                    COLOR1 = e['darkcolor']
                else:
                    COLOR2 = e['darkcolor']
                enemies.remove(e)

        #Also draws the background
        setupScreen(playerCoords, currentDir, enemies)
            
        titleText, titleRect = makeText('GEOMETRIC SLIDERS', BIGFONT, titleColor, BLACK)
        titleRect.center = (WINWIDTH / 2, WINHEIGHT / 3)
        if not howToPlay:
            windowSurface.blit(titleText, titleRect)

        if start:
            drawPressStart(startColor, COLOR1)
        elif not start and not howToPlay:
            drawChoices(choice, startColor, COLOR1)
        elif not start and howToPlay:
            howToPlay, choice = drawHowToPlay(choice, startColor)
            if not howToPlay:
                choice = 1
            
        

        pygame.display.update()
        fpsClock.tick(FPS)
    #...


def drawPressStart(startColor, COLOR1):
    startText, startRect = makeText('- SPACEBAR -', GAMEFONT, startColor, COLOR1)
    startRect.center = (WINWIDTH / 2, (WINHEIGHT*3)/4)
    windowSurface.blit(startText, startRect)


def drawChoices(choice, startColor, COLOR1):
    if choice == 1:
        playGameText, playGameRect   = makeText('-  Play Game  -', GAMEFONT, BLUE, COLOR1)
        howToPlayText, howToPlayRect = makeText('  How To Play  ', GAMEFONT, LIGHTBLUE, BLACK)
        quitText, quitRect           = makeText('     Quit      ', GAMEFONT, GREEN, BLACK)
    elif choice == 2:
        playGameText, playGameRect   = makeText('   Play Game   ', GAMEFONT, BLUE, BLACK)
        howToPlayText, howToPlayRect = makeText('- How To Play -', GAMEFONT, LIGHTBLUE, COLOR1)
        quitText, quitRect = makeText('     Quit      ', GAMEFONT, GREEN, BLACK)
    elif choice == 3:
        playGameText, playGameRect = makeText('   Play Game   ', GAMEFONT, BLUE, BLACK)
        howToPlayText, howToPlayRect = makeText('  How To Play  ', GAMEFONT, LIGHTBLUE, BLACK)
        quitText, quitRect = makeText('-    Quit     -', GAMEFONT, GREEN, COLOR1)

    playGameRect.center = (WINWIDTH/2, WINHEIGHT - (WINHEIGHT/4) - 50)
    howToPlayRect.center = (WINWIDTH/2, WINHEIGHT - WINHEIGHT/4)
    quitRect.center = (WINWIDTH/2, WINHEIGHT - (WINHEIGHT/4) + 50)

    windowSurface.blit(playGameText, playGameRect)
    windowSurface.blit(howToPlayText, howToPlayRect)
    windowSurface.blit(quitText, quitRect)


def drawHowToPlay(choice, startColor):
    rightArrowColor = WHITE
    leftArrowColor = WHITE
    for event in pygame.event.get(KEYUP):
        if event.key in (K_RIGHT, K_d) and choice < 5:
            forwardSound.play()
            choice += 1
            rightArrowColor = BLUE
        elif event.key in (K_LEFT, K_a) and choice > 1:
            backwardSound.play()
            choice -= 1
            leftArrowColor = RED
        elif event.key in (K_SPACE, K_RETURN) and choice == 5:
            backwardSound.play()
            return False, choice
        elif event.key in (K_ESCAPE, K_BACKSPACE):
            backwardSound.play()
            return False, choice

    if choice == 1:
    #Draw 'you' on the screen
        youText, youRect = makeText('You', GAMEFONT, BLUE)
        you1Text, you1Rect = makeText('-   You', GAMEFONT, startColor) 
        text1Text, text1Rect = makeText('We know you like science and spaceships,', GAMEFONT, startColor)
        text2Text, text2Rect = makeText('so we distilled some pure science and turned you INTO a spaceship.', GAMEFONT, startColor)
        text3Text, text3Rect = makeText('Luckily, it only takes four buttons with arrows on them to move.', GAMEFONT, startColor)
        text4Text, text4Rect = makeText('Technology sure has come far! - Team SCIENCE', GAMEFONT, startColor)
        text5Text, text5Rect = makeText('(P.S. How did you even read this?)', SMALLFONT, startColor)
 
        youRect.midbottom = (WINWIDTH/2, WINHEIGHT-45)
        you1Rect.midleft = (WINWIDTH/2, WINHEIGHT/3)
        text1Rect.center = (WINWIDTH/2, WINHEIGHT/8)
        text2Rect.center = (WINWIDTH/2, WINHEIGHT/5)
        text3Rect.center = (WINWIDTH/2, WINHEIGHT /2)
        text4Rect.center = (WINWIDTH/2, text3Rect.bottom + 30)
        text5Rect.center = (WINWIDTH/2, text4Rect.bottom + 90)

        windowSurface.blit(youText, youRect)
        windowSurface.blit(you1Text, you1Rect)
        windowSurface.blit(text1Text, text1Rect)
        windowSurface.blit(text2Text, text2Rect)
        windowSurface.blit(text3Text, text3Rect)
        windowSurface.blit(text4Text, text4Rect)
        windowSurface.blit(text5Text, text5Rect)

        turnedPlayerImage = turnPlayer(UP)
        drawPlayer({'x':(GRIDWIDTH/2)-2, 'y':(GRIDHEIGHT/2)-4}, turnedPlayerImage, True)

        pygame.draw.polygon(windowSurface, rightArrowColor, [((WINWIDTH*3)/4, WINHEIGHT - 45), ((WINWIDTH*3)/4, WINHEIGHT - 75), (((WINWIDTH*3)/4)+25, WINHEIGHT - 60)], 0)

    elif choice == 2:
    #Draw 'them' on the screen
        themText, themRect = makeText('Them', GAMEFONT, RED)
        them1Text, them1Rect = makeText('-   Them', GAMEFONT, startColor)
        text1Text, text1Rect = makeText('It gets better. There are evil non-sciencers who want our science.', GAMEFONT, startColor)
        text2Text, text2Rect = makeText('Who made them, you may ask? Well stop asking. It doesn\'t matter.', GAMEFONT, startColor)
        text3Text, text3Rect = makeText('What are you? The science police?', GAMEFONT, startColor)
        text4Text, text4Rect = makeText('Moving On.', GAMEFONT, startColor)

        themRect.midbottom = (WINWIDTH/2, WINHEIGHT-45)
        them1Rect.midleft = (WINWIDTH/2, (WINHEIGHT/3)-30)
        text1Rect.center = (WINWIDTH/2, WINHEIGHT/8)
        text2Rect.center = (WINWIDTH/2, WINHEIGHT/2)
        text3Rect.center = (WINWIDTH/2, text2Rect.bottom + 30)
        text4Rect.center = (WINWIDTH/2, text3Rect.bottom + 90)

        windowSurface.blit(themText, themRect)
        windowSurface.blit(them1Text, them1Rect)
        windowSurface.blit(text1Text, text1Rect)
        windowSurface.blit(text2Text, text2Rect)
        windowSurface.blit(text3Text, text3Rect)
        windowSurface.blit(text4Text, text4Rect)

        for y in range(3):
            pygame.draw.rect(windowSurface, DARKRED, ((WINWIDTH/2)-((y+2)*BOXSIZE), 5*BOXSIZE, BOXSIZE, BOXSIZE))
            pygame.draw.rect(windowSurface, RED, (((WINWIDTH/2)-((y+2)*BOXSIZE))+5, (5*BOXSIZE)+5, BOXSIZE-10, BOXSIZE-10))

    elif choice == 3:
    #Draw 'towers/pods' on the screen
        weaponsText, weaponsRect = makeText('Weapons', GAMEFONT, PURPLE)
        spaceText, spaceRect = makeText('Spacebar', GAMEFONT, startColor)
        numbersText, numbersRect = makeText(' 1             2             3             4', GAMEFONT, startColor)
        text1Text, text1Rect = makeText('Okay kiddo here\'s the fun part.', GAMEFONT, startColor)
        text2Text, text2Rect = makeText('We can\'t let you go out there without some weapons', GAMEFONT, startColor)
        text3Text, text3Rect = makeText('(Well, we COULD but we aren\'t that psychotic so...)', GAMEFONT, startColor)
        text4Text, text4Rect = makeText('(P.P.S. We have NO idea what these do.)', SMALLFONT, startColor) 

        weaponsRect.midbottom = (WINWIDTH/2, WINHEIGHT-45)
        spaceRect.midtop = ((WINWIDTH/2)+20, (WINHEIGHT/2)+110)
        text1Rect.center = (WINWIDTH/2, WINHEIGHT/8)
        text2Rect.center = (WINWIDTH/2, WINHEIGHT/5)
        text3Rect.center = (WINWIDTH/2, text2Rect.bottom + 30)
        text4Rect.center = (WINWIDTH/2, ((WINHEIGHT*6)/7)-30)

        pod1Rect = pygame.Rect((WINWIDTH/2)-180, (WINHEIGHT/2)-60, BOXSIZE, BOXSIZE)
        pod2Rect = pygame.Rect((WINWIDTH/2)-60, (WINHEIGHT/2)-60, BOXSIZE, BOXSIZE)
        pod3Rect = pygame.Rect((WINWIDTH/2)+60, (WINHEIGHT/2)-60, BOXSIZE, BOXSIZE)
        pod4Rect = pygame.Rect((WINWIDTH/2)+180, (WINHEIGHT/2)-60, BOXSIZE, BOXSIZE)
        bullet1Rect = pygame.Rect((WINWIDTH/2), (WINHEIGHT/2)+60, BOXSIZE, BOXSIZE)
        bullet2Rect = pygame.Rect((WINWIDTH/2)-120, bullet1Rect.top, BOXSIZE, BOXSIZE)
        numbersRect.topleft = (pod1Rect.left, pod1Rect.bottom+20)

        windowSurface.blit(weaponsText, weaponsRect)
        windowSurface.blit(spaceText, spaceRect)
        windowSurface.blit(numbersText, numbersRect)
        windowSurface.blit(text1Text, text1Rect)
        windowSurface.blit(text2Text, text2Rect)
        windowSurface.blit(text3Text, text3Rect)
        windowSurface.blit(text4Text, text4Rect)

        windowSurface.blit(firstTurretImage, pod1Rect)
        windowSurface.blit(secondTurretImage, pod2Rect)
        windowSurface.blit(thirdTurretImage, pod3Rect)
        windowSurface.blit(fourthTurretImage, pod4Rect)

        windowSurface.blit(hBulletImage1, bullet1Rect)
        windowSurface.blit(hBulletImage1, bullet2Rect)
        
        pygame.draw.rect(windowSurface, WHITE, (pod1Rect.left, pod1Rect.top+47, BOXSIZE, BOXSIZE), 2)
        pygame.draw.rect(windowSurface, WHITE, (pod2Rect.left-1, pod2Rect.top+47, BOXSIZE, BOXSIZE), 2)
        pygame.draw.rect(windowSurface, WHITE, (pod3Rect.left-2, pod3Rect.top+47, BOXSIZE, BOXSIZE), 2)
        pygame.draw.rect(windowSurface, WHITE, (pod4Rect.left-3, pod4Rect.top+47, BOXSIZE, BOXSIZE), 2)
        pygame.draw.rect(windowSurface, WHITE, (spaceRect.left-40, spaceRect.top-2, spaceRect.width+80, spaceRect.height+4), 2)

        turnedPlayerImage = turnPlayer(LEFT)
        drawPlayer({'x':(GRIDWIDTH/2)+4, 'y':(GRIDHEIGHT/2)+2}, turnedPlayerImage, True)

    elif choice == 4:
    #Draw 'upgrades' on the screen
        upgradesText, upgradesRect = makeText('Upgrades', GAMEFONT, GREEN)
        text1Text, text1Rect = makeText('With the leftover science we had,', GAMEFONT, startColor)
        text2Text, text2Rect = makeText('we found that we could send you direct upgrades through The SPEct-RUM.', GAMEFONT, startColor)
        text3Text, text3Rect = makeText('Through extensive testing(and late nights at a bar) we found that those buggers', GAMEFONT, startColor)
        text4Text, text4Rect = makeText('can intercept your upgrades. Not to worry Though.', GAMEFONT, startColor)
        text5Text, text5Rect = makeText('You can choose which upgrade we allow them to hijack.', GAMEFONT, startColor)

        upgrade1Rect = pygame.Rect((WINWIDTH/3), (WINHEIGHT/3)-25, 50, 50)
        upgrade2Rect = pygame.Rect((WINWIDTH/2)-25, (WINHEIGHT/3)-25, 50, 50)
        upgrade3Rect = pygame.Rect(((WINWIDTH*2)/3)-50, (WINHEIGHT/3)-25, 50, 50)
        upgrade4Rect = pygame.Rect((WINWIDTH/3), ((WINHEIGHT*3)/4)-25, 50, 50)
        upgrade5Rect = pygame.Rect((WINWIDTH/2)-25, ((WINHEIGHT*3)/4)-25, 50, 50)
        upgrade6Rect = pygame.Rect(((WINWIDTH*2)/3)-50, ((WINHEIGHT*3)/4)-25, 50, 50)
        
        upgradesRect.midbottom = (WINWIDTH/2, WINHEIGHT-45)
        text1Rect.center = (WINWIDTH/2, WINHEIGHT/8)
        text2Rect.center = (WINWIDTH/2, WINHEIGHT/5)
        text3Rect.center = (WINWIDTH/2, (WINHEIGHT/2)-20)
        text4Rect.center = (WINWIDTH/2, text3Rect.bottom+30)
        text5Rect.center = (WINWIDTH/2, text4Rect.bottom+30)

        windowSurface.blit(upgradesText, upgradesRect)
        windowSurface.blit(text1Text, text1Rect)
        windowSurface.blit(text2Text, text2Rect)
        windowSurface.blit(text3Text, text3Rect)
        windowSurface.blit(text4Text, text4Rect)
        windowSurface.blit(text5Text, text5Rect)

        windowSurface.blit(energyUpgrade, upgrade1Rect)
        windowSurface.blit(turretUpgrade, upgrade2Rect)
        windowSurface.blit(shipUpgrade, upgrade3Rect)
        windowSurface.blit(healthUpgrade, upgrade4Rect)
        windowSurface.blit(speedUpgrade, upgrade5Rect)
        windowSurface.blit(spawnUpgrade, upgrade6Rect)
            
    elif choice == 5:
    #Draw the 'back' button
        backText, backRect = makeText('Back', GAMEFONT, LIGHTBLUE)
        text1Text, text1Rect = makeText('You did it! You completed your training and it didn\'t even take years of work.', GAMEFONT, startColor)
        text2Text, text2Rect = makeText('You have become a true man(ship) of science!', GAMEFONT, startColor)
        text3Text, text3Rect = makeText('Now go out there and protect some scientists.', GAMEFONT, startColor)
        text4Text, text4Rect = makeText('And don\'t forget, Team SCIENCE is totally rooting for you.', GAMEFONT, startColor)

        backRect.midbottom = (WINWIDTH/2, WINHEIGHT-45)
        text1Rect.center = (WINWIDTH/2, WINHEIGHT/8)
        text2Rect.center = (WINWIDTH/2, WINHEIGHT/4)
        text3Rect.center = (WINWIDTH/2, text2Rect.bottom+60)
        text4Rect.center = (WINWIDTH/2, (WINHEIGHT*3)/4)

        windowSurface.blit(backText, backRect)
        windowSurface.blit(text1Text, text1Rect)
        windowSurface.blit(text2Text, text2Rect)
        windowSurface.blit(text3Text, text3Rect)
        windowSurface.blit(text4Text, text4Rect)

        pygame.draw.polygon(windowSurface, leftArrowColor, [(WINWIDTH/4, WINHEIGHT - 45), (WINWIDTH/4, WINHEIGHT - 75), ((WINWIDTH/4)-25, WINHEIGHT - 60)], 0)

    if choice > 1 and choice < 5:
        pygame.draw.polygon(windowSurface, leftArrowColor, [(WINWIDTH/4, WINHEIGHT - 45), (WINWIDTH/4, WINHEIGHT - 75), ((WINWIDTH/4)-25, WINHEIGHT - 60)], 0)
        pygame.draw.polygon(windowSurface, rightArrowColor, [((WINWIDTH*3)/4, WINHEIGHT - 45), ((WINWIDTH*3)/4, WINHEIGHT - 75), (((WINWIDTH*3)/4)+25, WINHEIGHT - 60)], 0)    

    return True, choice     
            
    


def gameOver():
    pygame.mixer.music.stop()
    deathSound.play()
    playerCoords = {'x': 0, 'y': 0}
    currentDir = RIGHT
    enemies = []
    COLOR1 = BLACK
    COLOR2 = random.choice(DARKCOLORS)
    lastEnemyTime = time.time()
    changeColorTime = time.time()
    NEWENEMYTIME = 1
    NEWCOLORTIME = 0.55
    choice = 1
    gameOverColor = random.choice(LIGHTCOLORS)
    playAgainColor = random.choice(LIGHTCOLORS)
    quitColor = random.choice(LIGHTCOLORS)
    while True:
        checkForQuit()

        if time.time() - changeColorTime > NEWCOLORTIME:
            COLOR1, COLOR2 = COLOR2, COLOR1
            changeColorTime = time.time()

        for event in pygame.event.get(KEYUP):
            if event.key in (K_UP, K_w) and choice > 1:
                backwardSound.play()
                choice -= 1
            elif event.key in (K_DOWN, K_s) and choice < 2:
                forwardSound.play()
                choice += 1
            elif event.key == K_RETURN:
                if choice == 1:
                    pygame.event.get()
                    startGameSound.play()
                    runGame()
                elif choice == 2:
                    terminate()

        #Change player direction if they reach the edge
        if currentDir == UP and (playerCoords['x'] == 0 and playerCoords['y'] == 0):
            currentDir = RIGHT
        if currentDir == RIGHT and (playerCoords['x'] == GRIDWIDTH-1 and playerCoords['y'] == 0):
            currentDir = DOWN
        if currentDir == DOWN and (playerCoords['x'] == GRIDWIDTH-1 and playerCoords['y'] == GRIDHEIGHT-1):
            currentDir = LEFT
        if currentDir == LEFT and (playerCoords['x'] == 0 and playerCoords['y'] == GRIDHEIGHT-1):
            currentDir = UP

        #Add a new enemy at a random location
        if time.time() - lastEnemyTime > NEWENEMYTIME:
            color = random.randint(0, len(LIGHTCOLORS)-1)
            enemySquare = {'x':          random.randint(0, GRIDWIDTH-1),
                       'y':          random.randint(0, GRIDHEIGHT-1),
                       'lightcolor': LIGHTCOLORS[color],
                       'darkcolor':  DARKCOLORS[color],
                       'health':     (color + 1) * 5,
                       'size':       BOXSIZE
                       }
            enemies.append(enemySquare)
            lastEnemyTime = time.time()

        for e in enemies:
            if playerCoords['x'] == e['x'] and playerCoords['y'] == e['y']:
                gameOverColor = e['lightcolor']
                playAgainColor = e['lightcolor']
                quitColor = e['lightcolor']
                if COLOR1 != BLACK:
                    COLOR1 = e['darkcolor']
                else:
                    COLOR2 = e['darkcolor']
                enemies.remove(e)

        gameOverText, gameOverRect = makeText('GAME OVER', BIGFONT, gameOverColor, BLACK)
        gameOverRect.center = (WINWIDTH / 2, WINHEIGHT / 3)
            
        #Flash the color if the "cursor" is over an option
        if choice == 1:
            playAgainText, playAgainRect = makeText('- Play again -', GAMEFONT, playAgainColor, COLOR1)
            playAgainRect.center = (WINWIDTH / 2, WINHEIGHT - (WINHEIGHT/4))

            quitText, quitRect = makeText('     Quit     ', GAMEFONT, quitColor, BLACK)
            quitRect.center = (WINWIDTH / 2, WINHEIGHT - (WINHEIGHT/4) + 50)
        elif choice == 2:
            playAgainText, playAgainRect = makeText('  Play again  ', GAMEFONT, playAgainColor, BLACK)
            playAgainRect.center = (WINWIDTH / 2, WINHEIGHT - (WINHEIGHT/4))

            quitText, quitRect = makeText('-    Quit    -', GAMEFONT, quitColor, COLOR1)
            quitRect.center = (WINWIDTH / 2, WINHEIGHT - (WINHEIGHT/4) + 50)

        setupScreen(playerCoords, currentDir, enemies)

        windowSurface.blit(gameOverText, gameOverRect)
        windowSurface.blit(playAgainText, playAgainRect)
        windowSurface.blit(quitText, quitRect)

        pygame.display.update()
        fpsClock.tick(FPS)
        #...


if __name__ == '__main__':
    main()
