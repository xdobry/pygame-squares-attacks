# Attacken haben einen Namen
# und liste mit zeit verzögerung t (wie time) und l (wie lane) kind (normal, shield) mit platzierungen der Gegner
# "w0": [{"t":400,"l":3}],
# alternativ
# i wie item mit position und kind
# ist eine Attacke mit dem Namen "w0"
# nach 400 Zeit kommt ein Gegner auf dem Spur 3

attacks = {
   "w0": [{"t":400,"l":3}],
   # immer 1 in der spalte
   "s0": [{"t": 300, "l": 4},{"t": 200, "l":3}],
   "s1": [{"t": 300, "l": 3},{"t": 200, "l":2}],
   "s3": [{"t": 300, "l": 4},{"t": 200, "l":3},{"t": 200, "l":5},{"t": 200, "l":2}],
   # 2 parallel
   "d0": [{"t": 300, "l": [4,2]},{"t": 200, "l": [1,3]}],
   "d1": [{"t": 300, "l": [1,3]},{"t": 200, "l": [2,4]}],
   "d2": [{"t": 300, "l": [0,2]},{"t": 200, "l": [1,3]}],
   "d3": [{"t": 300, "l": [3,5]},{"t": 200, "l": [2,4]}],
   # langsam und danach schnell
   "l1": [{"t": 100, "l": 3, "kind": "slow"}],
   "l03": [{"t": 200, "l": 2, "kind": "slow"},{"t": 50, "l": 2},{"t": 50, "l": 2}],
   "l23": [{"t": 200, "l": [3,4], "kind": "slow"},{"t": 50, "l": [3,4]},{"t": 50, "l": [3,4]}],
   "lflangen5": [{"t": 200, "l":[0,2,5],"kind":"slow"},{"t": 50, "l":[0,2,5]},{"t": 50, "l":[0,2,5]},{"t": 50, "l":[0,2,5]},{"t": 50, "l":[0,2,5]}],
   # Sterne oder Kreuze
   "f0": [{"t": 300, "l": [2,4]},{"t": 50, "l": [3]},{"t": 50, "l": [2,4]}],
   "f1": [{"t": 300, "l": [0,2]},{"t": 50, "l": [1]},{"t": 50, "l": [0,2]}],
   "f2": [{"t": 300, "l": [3,5]},{"t": 50, "l": [4]},{"t": 50, "l": [3,5]}],
   # Formationen
   "pfeil": [{"t": 200, "l":3},{"t": 80, "l":[2,4]},{"t": 80, "l":[1,5]}],
   "revPfeil": [{"t": 200, "l":[1,5]},{"t": 80, "l":[2,4]},{"t": 80, "l":3}],
   "wall": [{"t": 200, "l": [0,1,2,3,4,5]},{"t":500,"l":[]}],
   "s_wall": [{"t": 200, "l": [0,1,2,3,4,5], "kind":"slow"},{"t":500,"l":[]}],
   "wall2": [{"t": 200, "l": [0,1,2,3,4,5]},{"t":50,"l":[0,1,2,3,4,5]}],
   "super": [{"t": 200, "l": [0,1,4,5]},{"t": 50, "l": [1,2,3,4]},{"t": 50, "l": [0,1,4,5]},{"t":500,"l":[]}],
   "rect": [{"t": 200, "l":[1,2,3,4]},{"t": 120, "l":[1,4]},{"t": 120, "l":[1,2,3,4]}],
   "flanken": [{"t": 200, "l":[0,5]},{"t": 200, "l":[0,5]}],
   "flanken5": [{"t": 200, "l":[0,5]},{"t": 120, "l":[0,5]},{"t": 120, "l":[0,5]},{"t": 120, "l":[0,5]},{"t": 120, "l":[0,5]}],
   "mitte3x2": [{"t": 200, "l":[2,3]},{"t": 50, "l":[2,3]},{"t": 50, "l":[2,3]}],
   "z0": [{"t": 200, "l":1},{"t": 100, "l":2},{"t": 100, "l":1},{"t": 100, "l":2},{"t": 100, "l":1},{"t": 100, "l":2},{"t": 100, "l":1},{"t": 100, "l":2}],
   "z1": [{"t": 200, "l":2},{"t": 100, "l":3},{"t": 100, "l":2},{"t": 100, "l":3},{"t": 100, "l":2},{"t": 100, "l":3},{"t": 100, "l":2},{"t": 100, "l":3}],
   "z2": [{"t": 200, "l":3},{"t": 100, "l":4},{"t": 100, "l":3},{"t": 100, "l":4},{"t": 100, "l":3},{"t": 100, "l":4},{"t": 100, "l":3},{"t": 100, "l":4}],
   "z3": [{"t": 200, "l":4},{"t": 100, "l":5},{"t": 100, "l":4},{"t": 100, "l":5},{"t": 100, "l":4},{"t": 100, "l":5},{"t": 100, "l":4},{"t": 100, "l":5}],
   # mit Schild
   "sh0": [{"t":200,"l":2, "kind":"shield"},{"t":50,"l":2},{"t":200,"l":4, "kind":"shield"},{"t":50,"l":4}],
   "sh1": [{"t":300,"l":[2,3,4],"kind":"shield"},{"t":120,"l":[1,2,4,5]}],
   "sh3": [{"t":300,"l":4,"kind":"shield"},{"t":50,"l":0},{"t":120,"l":4,"kind":"shield"},{"t":50,"l":0},{"t":120,"l":4,"kind":"shield"},{"t":50,"l":0}],
   "ws": [{"t":300,"l":[0,1,2,3,4,5],"kind":"shield"}],
   "ws2": [{"t":300,"l":[0,1,2,3,4,5],"kind":"shield"},{"t":100,"l":[0,1,2,3,4,5],"kind":"shield"}],
   # pausen
   "pause3": [{"t": 300}],
   "pause5": [{"t": 500}],
   # Items
   "speed": [{"t":10,"i": {"pos": (20,30),"kind":"speedShot"}}],
   "speed2": [{"t":10,"i": {"pos": (700,350),"kind":"speedShot"}}],
   "bomb": [{"t":10,"i": {"pos": (120,250),"kind":"bomb"}}],
   "bombNE": [{"t":10,"i": {"pos": (700,50),"kind":"bomb"}}],
   "fireball": [{"t":10,"i": {"pos": (520,150),"kind":"fireball"}}],
}

# Ein level wird durch directory mit felder
# attacks - liste mit attack namen
# obstacles - liste mit koordintaten der Hinderlnisse. Koordinaten sind liste mit tupel Position und Größe
# "boden","boden2","crystal_wall06","hive1","marble_wall1","pebble_red0","sandstone_wall0","slime0","stone_brick1","wall_yellow_rock0"
# 800x600
# Höhe 600-32=568
# lane hight = 769 / 6 = 95
# 

levels = [
    # 1
    {
        "attacks": ["s0","s3","pause3","s1","d0"],
        "obstacles": [[(780,100),(16,128)],[(780,400),(16,128)],[(500,0),(128,8)],[(500,592-32),(128,8)]],
        "background": "boden"
    },
    # 2
    {
        "attacks": ["l1","d0","f0","bombNE","d2","l23"],
        "obstacles": [[(780,100),(16,128)],[(780,400),(16,128)],[(500,0),(64,8)],[(500,592-32),(64,8)]],
        "background": "hive1"
    },
    # 3
    {
        "attacks": ["pfeil","pause3","d1","speed","d0","d3"],
        "obstacles": [[(650,100),(16,80)],[(650,400),(16,80)]],
        "background": "wall_yellow_rock0"
    },
    # 4
    {
        "attacks": ["revPfeil","pause3","sh3","mitte3x2","speed","pause3","mitte3x2"],
        "obstacles": [[(500,100),(16,64)],[(500,400),(16,64)]],
        "background": "pebble_red0"
    },
    # 5
    {
        "attacks": ["pfeil","pause3","sh3","l23","speed","pause3","mitte3x2"],
        "obstacles": [[(540,284-8-95),(64,16)],[(540,284-8+95),(64,16)]],
        "background": "boden"
    },
    # 6
    {
        "attacks": ["fireball","s0","flanken5","pause5","revPfeil","pfeil"],
        "obstacles": [[(780,100),(16,128)],[(780,400),(16,128)],[(100,0),(128,8)],[(100,592-32),(128,8)]],
        "background": "stone_brick1"
    },
    # 7
    {
        "attacks": ["fireball","flanken","speed","pause5","z3","z2","z1","z0"],
        "obstacles": [[(780,100),(16,128)],[(780,400),(16,128)],[(500,0),(128,8)],[(500,592-32),(128,8)],[(150,280),(128,8)]],
        "background": "wall_yellow_rock0"
    },
    # 8
    {
        "attacks": ["fireball","revPfeil","pause5","speed2","z3","z2","z2","z1"],
        "obstacles": [[(780,100),(16,128)],[(780,400),(16,128)],[(150,280-95),(128,8)],[(150,280+95),(128,8)]],
        "background": "boden"
    },
    # 9
    {
        "attacks": ["bomb","sh0","s_wall","pause5","sh3","f2","sh1","lflangen5","pause5","speed","pause3","ws"],
        "obstacles": [[(780,100),(16,128)],[(780,400),(16,128)],[(500,0),(64,8)],[(500,592-32),(64,8)]],
        "background": "crystal_wall06"
    },
    # 10
    {
        "attacks": ["pfeil","fireball","wall","super","pause5","ws","pause5","super","pause5","s0","ws2"],
        "obstacles": [[(780,100),(16,64)],[(780,400),(16,64)]],
        "background": "boden2"
    }
]