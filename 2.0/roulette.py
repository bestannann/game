import random

class Roulette:
    def __init__(self,*rolls):
        self.Roll = []
        for roll in rolls:
            self.Roll.append(self.nodelist(roll))
        self.number = 4 #每個輪胎顯示出的個數

    def nodelist(self,roll):
        if type(roll[0]) == type(Node()):
            return roll
        else:
            for i in range(len(roll)):
                roll[i] = Node(roll[i])
            for i in range(len(roll)):
                if i != len(roll) - 1:
                    roll[i].next = roll[i+1]
                else:
                    roll[i].next = roll[0]
            return roll



    def roll_all(self):
        def roll(roll,number):
            x = random.choice(roll)
            i = 0
            result = []
            while i < number:
                result.append(x.data)
                x = x.next
                i += 1
            return result
        return [roll(self.Roll[i],self.number) for i in range(len(self.Roll))]

class Node:
    def __init__(self,data=None,next=None):
        self.data = data
        self.next = next

