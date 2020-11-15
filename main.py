import math
import pygame
import time
pygame.init()
pygame.font.init()
pixelFont = pygame.font.Font('Pixeled.ttf',5)
width = 800
height = 600
window = pygame.display.set_mode((width,height))
pygame.display.set_caption('Broke College Student Simulator: An Introduction To Financial Literacy')
clock = pygame.time.Clock()
dTime = time.time()
elapsedTime=0
playerCycleTime=0

movementSpeed=5

lost=False
selectedDue=0
tutorial1=False
tutorial2=False
tutorial3=False
tutorial4=False
startCountdown=False
timeStarted=time.time()
timeRemaining=300
exited = False
canMove=False
movingLeft=False
movingRight=False
inDuesMenu=False
inPaymentMenu=False
inAtmMenu=False
toolTipOn=False
interactionObj={}
room=0
balance=0
debitBalance=0
creditDebt=0
bottles=0
bottleChart=[1,1,1]
dueChart=[300,500,2000]
due1Paid=False
due2Paid=False
due3Paid=False
currentTimeLimit=300

black = (0,0,0)
white = (255,255,255)
background = (175,175,175)

#Images
plr1=pygame.image.load('Images/idle1.png')
plr2=pygame.image.load('Images/idle2.png')
plr3=pygame.image.load('Images/run1.png')
plr4=pygame.image.load('Images/run2.png')
plrImg=plr2

dormImg=pygame.image.load('Images/dorm.png')
wall1Img=pygame.image.load('Images/wall1.png')
wall2Img=pygame.image.load('Images/wall2.png')
doorImg=pygame.image.load('Images/door.png')
elevatorImg=pygame.image.load('Images/elevator.png')
blueBinImg=pygame.image.load('Images/blueBin.png')
atmImg=pygame.image.load('Images/atm.png')
vendingMachineImg=pygame.image.load('Images/vendingMachine.png')
recyclingMachineImg=pygame.image.load('Images/recyclingMachine.png')
storeFrontImg=pygame.image.load('Images/storeFront.png')

dorm={'img':wall1Img,'offsetX':0,'offsetY':0,'offsetScaleX':0.5,'offsetScaleY':0.5}
wall1={'img':wall1Img,'offsetX':0,'offsetY':0,'offsetScaleX':0.5,'offsetScaleY':0.5}
wall2={'img':wall2Img,'offsetX':0,'offsetY':0,'offsetScaleX':0.5,'offsetScaleY':0.5}
door={'img':doorImg,'offsetX':0,'offsetY':0,'offsetScaleX':0.5,'offsetScaleY':1}
elevator={'img':elevatorImg,'msg':'Elevator','offsetX':0,'offsetY':0,'offsetScaleX':0.5,'offsetScaleY':1}
blueBin={'img':blueBinImg,'msg':'Blue Bin','offsetX':0,'offsetY':0,'offsetScaleX':0.5,'offsetScaleY':1}
atm={'img':atmImg,'msg':'ATM','offsetX':0,'offsetY':0,'offsetScaleX':0,'offsetScaleY':0}
vendingMachine={'img':vendingMachineImg,'msg':'Vending Machine','offsetX':0,'offsetY':0,'offsetScaleX':0,'offsetScaleY':0}
recyclingMachine={'img':recyclingMachineImg,'msg':'Recycling Machine','offsetX':0,'offsetY':0,'offsetScaleX':0.5,'offsetScaleY':1}
storeFront={'img':storeFrontImg,'msg':'Work','offsetX':0,'offsetY':0,'offsetScaleX':0.5,'offsetScaleY':1}

x = 700
y = 300
scroll=0
minScroll=0#-350
maxScroll=0#350
minX=0
maxX=800

def updateMoney(amt):
    global balance,moneyText,tutorial4,tipText
    balance+=amt
    if balance>200:
        balance=200
        if tutorial4==False:
            tutorial4=True
            tipText = generateText('$200 MAX CASH, IT\'S BETTER TO SAVE YOUR MONEY IN A BANK ACCOUNT',2,(246, 247, 94))
    if balance<0:
        moneyText=generateText("$"+str(balance),5,(255,100,100))
    else:
        moneyText=generateText("$"+str(balance),5,(255,255,255))

def updateTime():
    global timerText,timeRemaining,timeStarted,startCountdown,lost
    if startCountdown==False:
        return
    timeRemaining=currentTimeLimit-int(time.time()-timeStarted)
    #print(timeStarted)
    if timeRemaining>=60:
        timerText=generateText(str(timeRemaining),10,(255,255,255))
    else:
        timerText=generateText(str(timeRemaining),10,(255,100,100))
    if timeRemaining<=0:
        lost=True

def generateText(txt,size,color):
    tempText = pixelFont.render(txt,0,color,None)
    tempText = pygame.transform.scale(tempText,(tempText.get_rect().size[0]*size,tempText.get_rect().size[1]*size))
    return tempText

def generateRect(w,h,color):
    tempRect=pygame.draw.rect(window,(255,255,255),(500,0,0,0))
    tempBox=pygame.Surface((tempRect.width,tempRect.height))
    tempBox.fill(color)
    tempBox=pygame.transform.scale(tempBox,(w,h))
    return tempBox

def newObj(obj,x,y):
    obj['offsetX']=x
    obj['offsetY']=y
    return obj

def drawObjects(l):
    for i in l:
        window.blit(i['img'],(i['offsetX']-i['img'].get_rect().size[0]*i['offsetScaleX']-scroll,i['offsetY']-i['img'].get_rect().size[1]*i['offsetScaleY']))
        #print(i['img'].get_rect().size)

def getInteraction(l):
    global toolTipOn,interactionObj
    for i in l:
        if i['img'].get_rect().move(i['offsetX']-i['img'].get_rect().size[0]*i['offsetScaleX']-scroll,i['offsetY']-i['img'].get_rect().size[1]*i['offsetScaleY']).collidepoint(pygame.mouse.get_pos()):
            if 'msg' in i:
                toolTipOn=True
                interactionObj=i
                newInteraction(i)
                return
    toolTipOn=False

def newInteraction(obj):
    global toolTipBox, toolTipText
    toolTipText = generateText(obj['msg'],2,(255,255,255))
    toolTipBox = generateRect(toolTipText.get_rect().size[0]+10,30,(242, 178, 60))

def work(obj):
    global timeStarted
    updateMoney(75)
    timeStarted-=30

def openATM(obj):
    global inAtmMenu,balanceText,debtText,balance,creditDebt
    inAtmMenu=True
    balanceText=generateText('BALANCE: $'+str(debitBalance),4,(0, 0, 0))
    debtText=generateText('DEBT: $'+str(creditDebt),4,(255, 100, 100))

def debitPayment():
    global balanceText,debtText,currentTimeLimit,timeStarted,selectedDue,dueChart,debitBalance,due1Paid,due2Paid,due3Paid,inPaymentMenu,duePay1Box,duePay2Box,duePay3Box
    if debitBalance>=dueChart[selectedDue]:
        debitBalance-=dueChart[selectedDue]
        if selectedDue==0:
            due1Paid=True
            duePay1Box=generateRect(100,60,(100,100,100))
            currentTimeLimit=500
            timeStarted=time.time()
        elif selectedDue==1:
            due2Paid=True
            duePay2Box=generateRect(100,60,(100,100,100))
            currentTimeLimit=1000
            timeStarted=time.time()
        else:
            due3Paid=True
            duePay3Box=generateRect(100,60,(100,100,100))
    inPaymentMenu=False
    balanceText=generateText('BALANCE: $'+str(debitBalance),4,(0, 0, 0))
    debtText=generateText('DEBT: $'+str(creditDebt),4,(255, 100, 100))
def creditPayment():
    global tipText,balanceText,debtText,currentTimeLimit,timeStarted,selectedDue,dueChart,debitBalance,due1Paid,due2Paid,due3Paid,inPaymentMenu,creditDebt,duePay1Box,duePay2Box,duePay3Box
    if selectedDue==0:
        due1Paid=True
        duePay1Box=generateRect(100,60,(100,100,100))
        currentTimeLimit=500
        timeStarted=time.time()
    elif selectedDue==1:
        due2Paid=True
        duePay2Box=generateRect(100,60,(100,100,100))
        currentTimeLimit=1000
        timeStarted=time.time()
    else:
        due3Paid=True
        duePay3Box=generateRect(100,60,(100,100,100))
    creditDebt+=dueChart[selectedDue]
    inPaymentMenu=False
    balanceText=generateText('BALANCE: $'+str(debitBalance),4,(0, 0, 0))
    debtText=generateText('DEBT: $'+str(creditDebt),4,(255, 100, 100))
    tipText = generateText('UNPAID DEBT CAN HURT YOUR CREDIT SCORE, MAKE YOUR PAYMENTS ON TIME',2,(246, 247, 94))
def payDue(due):
    global selectedDue,inPaymentMenu,inDuesMenu
    if due==0:
        if due1Paid==False:
            selectedDue=0
            inPaymentMenu=True
            inDuesMenu=False
    elif due==1:
        if due2Paid==False:
            selectedDue=1
            inPaymentMenu=True
            inDuesMenu=False
    elif due==2:
        if due3Paid==False:
            selectedDue=2
            inPaymentMenu=True
            inDuesMenu=False
def entrance(obj):
    global room,minScroll,maxScroll,scroll,x,startCountdown,timeStarted,tutorial3,tipText
    if room==0:
        room=1
        minScroll=-350
        maxScroll=350
        scroll=350
        x=750
        timeStarted=time.time()
        startCountdown=True
        if tutorial3==False:
            tutorial3=True
            tipText = generateText('EARN MONEY TO PAY YOUR FIRST DUE',5,(246, 247, 94))
    elif room==1:
        room=2
    else:
        room=1

def renderFrame(delta):
    window.fill(background)
    global x,y,scroll
    if movingLeft:
        if scroll>minScroll:
            if x>400:
                x-=movementSpeed
                if x<minX:
                    x=minX
            else:
                scroll-=movementSpeed
        else:
            x-=movementSpeed
            scroll=minScroll
    if movingRight:
        if scroll<maxScroll:
            if x<400:
                x+=movementSpeed
                if x>maxX:
                    x=maxX
            else:
                scroll+=movementSpeed
        else:
            x+=movementSpeed
            scroll=maxScroll
    #print(scroll)
    #window.blit(carImg, (x,y))
    drawObjects(game[room])
    getInteraction(game[room])
    window.blit(plrImg,(x-plrImg.get_rect().size[0]/2,y))
    window.blit(moneyText,(20,0))

    window.blit(duesBox,((660,15)))
    window.blit(duesText,(675,0))

    window.blit(timerText,(400-timerText.get_rect().size[0]/2,0))

    window.blit(tipText,(400-tipText.get_rect().size[0]/2,520))

    if toolTipOn:
        window.blit(toolTipBox,(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]-30))
        window.blit(toolTipText,(pygame.mouse.get_pos()[0]+5,pygame.mouse.get_pos()[1]-30))
    if inDuesMenu:
        window.blit(duesMenu,(100,100))
        window.blit(due1,(110,100))
        window.blit(due2,(110,200))
        window.blit(due3,(110,300))

        window.blit(duePay1Box,(590,110))
        window.blit(duePay2Box,(590,210))
        window.blit(duePay3Box,(590,310))
        window.blit(duePayText,(600,100))
        window.blit(duePayText,(600,200))
        window.blit(duePayText,(600,300))
    if inPaymentMenu:
        window.blit(paymentMenu,(200,200))
        window.blit(debitButton,(225,300))
        window.blit(creditButton,(425,300))
        window.blit(debitText,(250,300))
        window.blit(creditText,(435,300))
    if inAtmMenu:
        window.blit(atmMenu,(200,200))
        window.blit(depositButton,(225,210))
        window.blit(withdrawButton,(415,210))
        window.blit(depositText,(250,210))
        window.blit(withdrawText,(430,210))
        window.blit(balanceText,(225,275))
        window.blit(debtText,(225,325))
    if lost:
        window.fill((255,0,0))

#print(blueBin)
#print(newObj(blueBin,0.5,0.5))
dorm=[{'img':dormImg,'offsetX':400,'offsetY':300,'offsetScaleX':0.5,'offsetScaleY':0.5},{'img':doorImg,'msg':'LEAVE DORM','func':'entrance','offsetX':60,'offsetY':430,'offsetScaleX':0.5,'offsetScaleY':1}]
hallway=[{'img':wall1Img,'offsetX':400,'offsetY':300,'offsetScaleX':0.5,'offsetScaleY':0.5},{'img':elevatorImg,'msg':'FIRST FLOOR','func':'entrance','offsetX':-115,'offsetY':430,'offsetScaleX':0.5,'offsetScaleY':1},{'img':doorImg,'offsetX':200,'offsetY':430,'offsetScaleX':0.5,'offsetScaleY':1},{'img':doorImg,'offsetX':500,'offsetY':430,'offsetScaleX':0.5,'offsetScaleY':1},{'img':doorImg,'offsetX':800,'offsetY':430,'offsetScaleX':0.5,'offsetScaleY':1},{'img':doorImg,'offsetX':1100,'offsetY':430,'offsetScaleX':0.5,'offsetScaleY':1},{'img':blueBinImg,'offsetX':350,'offsetY':430,'offsetScaleX':0.5,'offsetScaleY':1},{'img':blueBinImg,'offsetX':950,'offsetY':430,'offsetScaleX':0.5,'offsetScaleY':1}]
lobby=[{'img':wall2Img,'offsetX':400,'offsetY':300,'offsetScaleX':0.5,'offsetScaleY':0.5},{'img':elevatorImg,'msg':'SECOND FLOOR','func':'entrance','offsetX':-115,'offsetY':430,'offsetScaleX':0.5,'offsetScaleY':1},{'img':blueBinImg,'offsetX':75,'offsetY':430,'offsetScaleX':0.5,'offsetScaleY':1},{'img':vendingMachineImg,'offsetX':250,'offsetY':430,'offsetScaleX':0.5,'offsetScaleY':1},{'img':recyclingMachineImg,'offsetX':400,'offsetY':430,'offsetScaleX':0.5,'offsetScaleY':1},{'img':atmImg,'msg':'USE ATM','func':'openATM','offsetX':550,'offsetY':430,'offsetScaleX':0.5,'offsetScaleY':1},{'img':storeFrontImg,'msg':'WORK ($75)','func':'work','offsetX':875,'offsetY':430,'offsetScaleX':0.5,'offsetScaleY':1}]
game=[dorm,hallway,lobby]

moneyText=generateText("$"+str(balance),5,(255,255,255))
duesText=generateText("DUES",5,(255,255,255))

duesBox = generateRect(130,50,(255,150,150))
duesMenu = generateRect(600,400,(255,255,255))

toolTipBox = generateRect(100,25,(242, 178, 60))
toolTipText = generateText('',2,(255,255,255))

timerText = generateText('',10,(255,255,255))

tipText = generateText('CLICK THE \'DUES\' BUTTON',5,(246, 247, 94))
due1=generateText('TEXTBOOKS: $300',5,(255, 100, 100))
due2=generateText('INSURANCE: $900',5,(255, 100, 100))
due3=generateText('STUDENT DEBT: $2000',5,(255, 100, 100))
duePay1Box=generateRect(100,60,(100,255,100))
duePay2Box=generateRect(100,60,(100,255,100))
duePay3Box=generateRect(100,60,(100,255,100))
duePayText=generateText('PAY',5,(255,255,255))

paymentMenu = generateRect(400,200,(255,255,255))
debitButton = generateRect(150,60,(100,100,255))
creditButton = generateRect(150,60,(100,255,100))
debitText = generateText('DEBIT',5,(255,255,255))
creditText = generateText('CREDIT',5,(255,255,255))

atmMenu = generateRect(400,200,(255,255,255))
depositButton = generateRect(150,60,(100,255,100))
withdrawButton = generateRect(150,60,(100,100,255))
depositText = generateText('DEPOSIT',3,(255,255,255))
withdrawText = generateText('WITHDRAW',3,(255,255,255))

balanceText=generateText('BALANCE: $',4,(0, 0, 0))
debtText=generateText('DEBT: $',4,(255, 100, 100))

while not exited:
    dTime=time.time()-dTime
    elapsedTime+=dTime
    playerCycleTime+=dTime
    updateTime()
    #print(int(elapsedTime%1*4))

    for event in pygame.event.get():
        #print(event)
        if event.type == pygame.QUIT:
            exited = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            if toolTipOn:
                if abs(interactionObj['offsetX']-(scroll+x)) <200:
                    globals()[interactionObj['func']](interactionObj)
            elif duesBox.get_rect().move(660,15).collidepoint(pygame.mouse.get_pos()):
                if inAtmMenu:
                    inAtmMenu=False
                if tutorial1==False:
                    tutorial1=True
                    tipText = generateText('PAY DUES BEFORE DEADLINES',5,(246, 247, 94))
                if inDuesMenu==False:
                    inDuesMenu=True
                    if inPaymentMenu:
                        inPaymentMenu=False
                        inDuesMenu=False
                        inAtmMenu=False
                else:
                    inDuesMenu=False
                    if tutorial2==False:
                        tutorial2=True
                        canMove=True
                        tipText = generateText('MOVE WITH A/D, INTERACT WITH MOUSE',5,(246, 247, 94))
            if inDuesMenu:
                if duePay1Box.get_rect().move(590,110).collidepoint(pygame.mouse.get_pos()):
                    payDue(0)
                elif duePay2Box.get_rect().move(590,210).collidepoint(pygame.mouse.get_pos()):
                    if due1Paid:
                        payDue(1)
                elif duePay2Box.get_rect().move(590,310).collidepoint(pygame.mouse.get_pos()):
                    if due2Paid:
                        payDue(2)
            elif inPaymentMenu:
                if debitButton.get_rect().move(225,300).collidepoint(pygame.mouse.get_pos()):
                    debitPayment()
                elif creditButton.get_rect().move(425,300).collidepoint(pygame.mouse.get_pos()):
                    creditPayment()
            elif inAtmMenu:
                if depositButton.get_rect().move(225,210).collidepoint(pygame.mouse.get_pos()):
                    debitBalance+=balance
                    updateMoney(balance*-1)
                elif withdrawButton.get_rect().move(415,210).collidepoint(pygame.mouse.get_pos()):
                    updateMoney(debitBalance)
                    debitBalance=0
                balanceText=generateText('BALANCE: $'+str(debitBalance),4,(0, 0, 0))
                debtText=generateText('DEBT: $'+str(creditDebt),4,(255, 100, 100))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                if canMove:
                    movingLeft=True
                    playerCycleTime-=playerCycleTime%0.5
            elif event.key == pygame.K_d:
                if canMove:
                    movingRight=True
                    playerCycleTime-=playerCycleTime%0.5
            elif event.key == pygame.K_ESCAPE:
                inAtmMenu=False
                inDuesMenu=False
                inPaymentMenu=False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                if canMove:
                    movingLeft=False
                    if not movingRight:
                        plrImg=plr2
            elif event.key == pygame.K_d:
                if canMove:
                    movingRight=False
                    if not movingLeft:
                        plrImg=plr1
    if movingLeft and not movingRight:
        if playerCycleTime%0.33<0.165:
            plrImg = plr4
        else:
            plrImg = plr2
    if movingRight and not movingLeft:
        if playerCycleTime%0.33<0.165:
            plrImg = plr3
        else:
            plrImg = plr1
    renderFrame(dTime)

    pygame.display.update()
    dTime = time.time()
    clock.tick(60)
pygame.quit()
quit()