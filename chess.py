#Matthew Oley
#chess program
#final project

#TODO


import tkinter as tk
import time
import datetime

#determine who starts and method for passing turn
turn="w"
def changeTurn():
  ch={"w":"b","b":"w",None:None}
  global turn
  turn=ch[turn]

#routing method for determining what profile to use
def showPossibleMoves(peice,posx,posy):
  showCheck()
  switch={"r":rook,"k":knight,"b":bishop,"q":queen,"K":king,"p":pawn}
  if peice!="  " and peice[0]==turn and won==False:showRed(switch[peice[1]](posx,posy,pieces,peice[0]),str(posx)+str(posy))
  else: showCheck()

#general function to display peices and register lambda listeners
def printBoard():
  showCheck()
  key = {"r":"\u265C","k":"\u265E","b":"\u265D","K":"\u265A","q":"\u265B","p":"\u265F"," ":" "}
  for i in range(8):
    for j in range(8):
      if(pieces[i][j][0]=="w"):textColor="white"
      else:textColor="black"
      board[str(i)+str(j)]["text"]=key[pieces[i][j][1]]
      board[str(i)+str(j)]["fg"]=textColor
      board[str(i)+str(j)]["font"]=("Arial",26)
      board[str(i)+str(j)]["command"]=lambda arg1=pieces[i][j], arg2=i, arg3=j :showPossibleMoves(arg1, arg2, arg3)

#uses a list of positions to display red possible moves
def showRed(squares,org):
  for i in squares:
    board[str(i)]["bg"]="red"
    board[str(i)]["command"]=lambda arg1=str(org), arg2=str(i) :movePeice(arg1, arg2)

#resets board to the checked pattern/ removes red
def showCheck():
  for i in range(8):
    for j in range(8):
      if (i+j)%2==0:color="grey"
      else:color="blue"
      board[str(i)+str(j)]["bg"]=color

#used to actually move peice, also stores taken peices and determines if the game has been won
def movePeice(org,fin):
  key = {"r":"\u265C","k":"\u265E","b":"\u265D","K":"\u265A","q":"\u265B","p":"\u265F"," ":" "}
  passantCheck=pieces[int(fin[0])][int(fin[1])]=="  "
  if board[str(fin)]["bg"]!="red":
    #if the user clicks on an empty sqare clear the red
    showCheck()
    return
  if pieces[int(fin[0])][int(fin[1])][1]!=" ":
    #takes note of captured peices
    if turn=="b":wdisqual["text"]=wdisqual["text"]+key[pieces[int(fin[0])][int(fin[1])][1]]
    if turn=="w":bdisqual["text"]=bdisqual["text"]+key[pieces[int(fin[0])][int(fin[1])][1]]
  if pieces[int(fin[0])][int(fin[1])][1]=="K":gameWon()
  #check if the game has been won
  pieces[int(fin[0])][int(fin[1])]=pieces[int(org[0])][int(org[1])]
  pieces[int(org[0])][int(org[1])]="  "
  if int(fin[0])==0 and turn=="w" and pieces[int(fin[0])][int(fin[1])][1]=="p":menuPawnChange(fin)
  if int(fin[0])==7 and turn=="b" and pieces[int(fin[0])][int(fin[1])][1]=="p":menuPawnChange(fin)
  #check for passant
  try:
    if passantCheck and turn=="w" and pieces[int(fin[0])+1][int(fin[1])][1]=="p" and pieces[int(fin[0])][int(fin[1])][1]=="p":
      pieces[int(fin[0])+1][int(fin[1])]="  "
      bdisqual["text"]+="\u265F"
    if passantCheck and turn=="b" and pieces[int(fin[0])-1][int(fin[1])][1]=="p" and pieces[int(fin[0])][int(fin[1])][1]=="p":
      pieces[int(fin[0])-1][int(fin[1])]="  "
      wdisqual["text"]+="\u265F"
  except:pass
  #check for castling
  if abs(int(org[1])-int(fin[1]))==2 and pieces[int(fin[0])][int(fin[1])][1]=="K":
    dec={"02":["00","03"],"06":["07","05"],"72":["70","73"],"76":["77","75"]}
    changeTurn()
    movePeice(dec[fin][0],dec[fin][1])
  changeTurn()
  printBoard()

def checkCastle():
  #used to determine if a castling move can be made
  possible=[{"00":"br","01":"  ","02":"  ","03":"  ","04":"bK"},
            {"04":"bK","05":"  ","06":"  ","07":"br"},
            {"70":"wr","71":"  ","72":"  ","73":"  ","74":"wK"},
            {"74":"wK","75":"  ","76":"  ","77":"wr"}]
  enc={0:["02","b"],1:["06","b"],2:["72","w"],3:["76","w"]}
  send=[]
  for k,i in enumerate(possible):
    works=True
    for j in i:
      if pieces[int(j[0])][int(j[1])]!=i[j]:works=False
    if works==True and turn == enc[k][1]:send.append(enc[k][0])
  return send
  pass
def rook(x,y,pieces,color):
  #logic for determinig possible moves for the rook
  safe = []
  for i in range(-1,2,2):
    for j in range(-1,2,2):
      ex=x
      ey=y
      cont=True
      while cont:
        if i<0:ex+=j
        if i>0:ey+=j
        try:val=pieces[ex][ey]
        except:val="  "
        if val!="  " or ex>=8 or ex<0 or ey>=8 or ey<0:
          if val[0]!=turn and ex<8 and ex>=0 and ey<8 and ey>=0:
            safe.append(str(ex)+str(ey))
          cont=False
        else:
          safe.append(str(ex)+str(ey))
  return safe

def pawn(x,y,pieces,color):
  global passant
  #logic for determinig possible moves for the pawn
  safe = []
  for k in range(-1,2,2):
    for i in range(-1,2,2):
      for j in range(-1,2,2):
        ex=x
        ey=y
        cont=True
        while cont:
          if k<0:
            if i<0:
              if color=="w":ex-=1
              if color=="b":ex+=1
              ey+=j
            if i>0:
              if color=="w":ex-=1
              if color=="b":ex+=1
              ey+=j
          if k>0:
            if color=="w":ex-=1
            if color=="b":ex+=1
            #if i<0:ex+=j
            #if i>0:ey+=j
          try:val=pieces[ex][ey]
          except:val="  "
          if val!="  " or ex>=8 or ex<0 or ey>=8 or ey<0:
            if val[0]!=turn and ex<8 and ex>=0 and ey<8 and ey>=0 and ey!=y and abs(ex-x)<2:
              safe.append(str(ex)+str(ey))
            cont=False
          else:
            if ey==y:
              safe.append(str(ex)+str(ey))
            if str(ex)+str(ey)==passant and ex==5 and turn=="b":
              safe.append(str(ex)+str(ey))
            if str(ex)+str(ey)==passant and ex==2 and turn=="w":
              safe.append(str(ex)+str(ey))
            if ex!=5 and color=="w":cont=False
            elif ex==x-1 and ey==y:passant=str(ex)+str(ey)
            if ex!=2 and color=="b":cont=False
            elif ex==x+1 and ey==y:passant=str(ex)+str(ey)
            print(passant)
  return safe

def bishop(x,y,pieces,color):
  #logic for determinig possible moves for the bishop
  safe = []
  for i in range(-1,2,2):
    for j in range(-1,2,2):
      ex=x
      ey=y
      cont=True
      while cont:
        if i<0:
          ex+=i
          ey+=j
        if i>0:
          ex+=i
          ey+=j
        try:val=pieces[ex][ey]
        except:val="  "
        if val!="  " or ex>=8 or ex<0 or ey>=8 or ey<0:
          if val[0]!=turn and ex<8 and ex>=0 and ey<8 and ey>=0:
            safe.append(str(ex)+str(ey))
          cont=False
        else:
          safe.append(str(ex)+str(ey))
  return safe

def queen(x,y,pieces,color):
  #logic for determinig possible moves for the queen
  safe = []
  for k in range(-1,2,2):
    for i in range(-1,2,2):
      for j in range(-1,2,2):
        ex=x
        ey=y
        cont=True
        while cont:
          if k<0:
            if i<0:
              ex+=i
              ey+=j
            if i>0:
              ex+=i
              ey+=j
          if k>0:
            if i<0:ex+=j
            if i>0:ey+=j
          try:val=pieces[ex][ey]
          except:val="  "
          if val!="  " or ex>=8 or ex<0 or ey>=8 or ey<0:
            if val[0]!=turn and ex<8 and ex>=0 and ey<8 and ey>=0:
              safe.append(str(ex)+str(ey))
            cont=False
          else:
            safe.append(str(ex)+str(ey))
  return safe

def king(x,y,pieces,color):
  #logic for determinig possible moves for the king
  exeptions = checkCastle()
  safe = []
  for k in range(-1,2,2):
    for i in range(-1,2,2):
      for j in range(-1,2,2):
        ex=x
        ey=y
        if k<0:
          if i<0:
            ex+=i
            ey+=j
          if i>0:
            ex+=i
            ey+=j
        if k>0:
          if i<0:ex+=j
          if i>0:ey+=j
        try:val=pieces[ex][ey]
        except:val="  "
        if val!="  " or ex>=8 or ex<0 or ey>=8 or ey<0:
          if val[0]!=turn and ex<8 and ex>=0 and ey<8 and ey>=0:
            safe.append(str(ex)+str(ey))
        else:
          safe.append(str(ex)+str(ey))
  for i in exeptions:
    safe.append(str(i))
  return safe

def knight(x,y,pieces,color):
  #logic for determinig possible moves for the knight
  safe = []
  for i in range(-1,2,2):
    for j in range(-2,3,4):
      for k in range(-1,2,2):
        ex=x
        ey=y
        if i<0:
          ex+=j
          ey+=k
        if i>0:
          ex+=k
          ey+=j
        try:val=pieces[ex][ey]
        except:val="  "
        if val!="  " or ex>=8 or ex<0 or ey>=8 or ey<0:
          if val[0]!=turn and ex<8 and ex>=0 and ey<8 and ey>=0:
            safe.append(str(ex)+str(ey))
        else:
          safe.append(str(ex)+str(ey))
  return safe
  
def gameWon():
  #called if the game is won
  menuClear()
  menuGameWin()
  global won
  won = True

def timer(window,timerFrame):
  #sets up the game timer
  whiteTimer = 0
  blackTimer = 0
  past = time.time()//1
  timerArea = tk.Frame(timerFrame)
  black = tk.Label(timerArea,text=timerFormat(0))
  black.grid(row=0,column=0)
  white = tk.Label(timerArea,text=timerFormat(0))
  white.grid(row=1,column=0)
  timerArea["bg"]="white"
  global pause
  pause=True
  def playPause():
    global pause
    if pause:
      pause=False
      pauseButton["text"]="Stop"
    else:
      pause=True
      pauseButton["text"]="Start"
  pauseButton = tk.Button(timerArea,text="Start")
  pauseButton["command"]=lambda: playPause()
  pauseButton.grid(column=1,row=0,rowspan=2)
  timerArea.grid(row=0,column=0)
  while not won:
    #special while to update both the timer and tkinter assets
    if turn=="w":timerArea["bg"]="white"
    if turn=="b":timerArea["bg"]="black"
    window.update_idletasks()
    window.update()
    if time.time()//1 != past and pause==False:
      past = time.time()//1
      if turn=="w":whiteTimer+=1
      if turn=="b":blackTimer+=1
      white["text"]=timerFormat(whiteTimer)
      black["text"]=timerFormat(blackTimer)

def timerFormat(num):
  #simple formatting call for the time values
  return str(datetime.timedelta(seconds=num))

def menuPawnChange(piece):
  #invoked when a pawn reaches the other side of the board
  #creates and facilitates the side diolgue to change pawn
  menuClear()
  global turn
  turnSav = turn
  turn = None
  infoWidgets["morphLabel"]["text"]="Your pawn has reached the\n end choose a new peice for\nit to become:"
  infoWidgets["morphLabel"].pack()
  infoWidgets["morphFrame"].pack()
  def changeDec(udec):
    pieces[int(piece[0])][int(piece[1])]=udec
    global turn
    turn = turnSav
    changeTurn()
    printBoard()
    menuClear()
  key = {"\u265B":"q","\u265C":"r","\u265D":"b","\u265E":"k"}
  for i,j in enumerate(infoWidgets["morphBtns"]):
    j["command"]=lambda arg1=turnSav+key[j["text"]]:changeDec(arg1)
    j.grid(row=0,column=i)
  
    
def menuGameWin():
  #displays win message
  menuClear()
  key = {"w":"white","b":"black"}
  infoWidgets["victoryLabel"]["text"]=key[turn]+"\nhas\nwon!"
  infoWidgets["victoryLabel"].pack()

def menuClear():
  #function forgets assets put in side menu
  #to be called before or after menu creation to clear the board
  infoWidgets["victoryLabel"].pack_forget()
  infoWidgets["morphLabel"].pack_forget()
  for i in infoWidgets["morphBtns"]:
    i.grid_forget()
  
def main():
  #determines if the game should continue
  #won=True ends program
  global won
  won = False
  global pieces
  global passant
  passant =""
  window = tk.Tk()
  chessArea = tk.Frame(window)
  infoArea = tk.Frame(window)
  window.title("Chess")
  window.rowconfigure(0,weight=1)
  window.columnconfigure(1,weight=1)
  #dimmentions of window
  xdimm = 650
  ydimm = 550
  window.geometry("{}x{}".format(xdimm,ydimm))
  binfo = tk.Frame(infoArea)
  timerFrame = tk.Frame(infoArea)
  winfo = tk.Frame(infoArea)
  infoArea.columnconfigure(0,weight=1)
  infoArea.rowconfigure(0,weight=1)
  infoArea.rowconfigure(1,weight=0)
  #infoArea.rowconfigure(2,weight=1)

  global bdisqual
  global wdisqual
  bdisqual = tk.Label(binfo,text="black:")
  wdisqual = tk.Label(winfo,text="white:")
  bdisqual.pack()
  wdisqual.pack()
  #starting positions for chess peices
  pieces = [["br","bk","bb","bq","bK","bb","bk","br"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["  ","  ","  ","  ","  ","  ","  ","  "],
            ["  ","  ","  ","  ","  ","  ","  ","  "],
            ["  ","  ","  ","  ","  ","  ","  ","  "],
            ["  ","  ","  ","  ","  ","  ","  ","  "],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wr","wk","wb","wq","wK","wb","wk","wr"]]
  global board
  board={}
  
  #initializes the button grid and adds peices in accordance with the above list
  for i in range(8):
    for j in range(8):
      if (i+j)%2==0:color="grey"
      else:color="blue"
      btn = tk.Button(chessArea,text=j,height=1,width=2,bg=color)
      btn.grid(row=i,column=j)
      board[str(i)+str(j)]=btn
  
  #sets up framework for side panel messages
  global infoWidgets
  infoWidgets={}
  optionMenu = tk.Frame(infoArea)
  optionMenu["bg"]="lightgrey"
  optionMenu.place(x=0,y=45,relwidth=1,height=150)
  victoryLabel = tk.Label(optionMenu,text="")
  victoryLabel["bg"]="lightgrey"
  victoryLabel["font"]=("Arial",30)
  morphLabel = tk.Label(optionMenu,text="")
  morphLabel["bg"]="lightgrey"
  morphLabel["font"]=("Arial",10)
  morphFrame = tk.Frame(optionMenu)
  morphFrame["bg"]="lightgrey"
  itt=["\u265B","\u265C","\u265D","\u265E"]
  sbtn=[]
  for i in itt:
    sbtn.append(tk.Button(morphFrame,text=i))

  #saves tkinter assets to global infoWidgets
  infoWidgets["morphBtns"]=sbtn
  infoWidgets["optionMenu"]=optionMenu
  infoWidgets["victoryLabel"]=victoryLabel
  infoWidgets["morphLabel"]=morphLabel
  infoWidgets["morphFrame"]=morphFrame

  #places all boxes and containers
  chessArea.grid(row=0,column=0)
  printBoard()
  binfo.grid(row=0,column=0,sticky="nw")
  timerFrame.place(x=0,y=(ydimm/2)-22)
  winfo.grid(row=1,column=0,sticky="sw")
  infoArea.place(x=400,y=0,width=200,relheight=1)
  #call timer function that contains tkinter while
  timer(window,timerFrame)


main()

