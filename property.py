class property:
    #state: house or hotel or railroad
    #color: has different # or properties for monopoly or rent depends on color
    propertyColors = ["brown", "light blue", "pink", "orange", "red", "yellow", "green", "dark blue"]
    propertyName = ["Baird", "Clements", "Baldy", "Jacobs", "Park","O'Brian","Norton","Knox","Bonner","Talbert","Hochstetter","Cooke","Fronczak","NSC","Ketter","Slee","Furnas","The Commons","Center for the Arts","Alumni Arena", "Davis", "Jarvis"]
    def __init__(self,name, state, color, buildings):
        self.name = name
        self.state = state
        self.color = color
        self.buildings = buildings

    def rent(self):
        if self.state == "house":
            if self.name == property.propertyName[0]: #Baird
                    if self.buildings == 0:
                        return 2
                    elif self.buildings == 1:
                        return 10
                    elif self.buildings == 2:
                        return 30
                    elif self.buildings == 3:
                        return 90
                    elif self.buildings == 4:
                        return 160
            elif self.name == property.propertyName[1]: #Clements
                    if self.buildings == 0:
                        return 4
                    elif self.buildings == 1:
                        return 20
                    elif self.buildings == 2:
                        return 60
                    elif self.buildings == 3:
                        return 180
                    elif self.buildings == 4:
                        return 320
            elif self.name == property.propertyName[2]: #Baldy
                    if self.buildings == 0:
                        return 6
                    elif self.buildings == 1:
                        return 30
                    elif self.buildings == 2:
                        return 90
                    elif self.buildings == 3:
                        return 270
                    elif self.buildings == 4:
                        return 400
            elif self.name == property.propertyName[3]: #Jacobs
                    if self.buildings == 0:
                        return 6
                    elif self.buildings == 1:
                        return 30
                    elif self.buildings == 2:
                        return 90
                    elif self.buildings == 3:
                        return 270
                    elif self.buildings == 4:
                        return 400
            elif self.name == property.propertyName[4]: #Park
                    if self.buildings == 0:
                        return 8
                    elif self.buildings == 1:
                        return 40
                    elif self.buildings == 2:
                        return 100
                    elif self.buildings == 3:
                        return 300
                    elif self.buildings == 4:
                        return 450
            elif self.name == property.propertyName[5]: #O'Brian
                    if self.buildings == 0:
                        return 8
                    elif self.buildings == 1:
                        return 40
                    elif self.buildings == 2:
                        return 100
                    elif self.buildings == 3:
                        return 300
                    elif self.buildings == 4:
                        return 450
            elif self.name == property.propertyName[6]: #Norton
                    if self.buildings == 0:
                        return 8
                    elif self.buildings == 1:
                        return 40
                    elif self.buildings == 2:
                        return 100
                    elif self.buildings == 3:
                        return 300
                    elif self.buildings == 4:
                        return 450
            elif self.name == property.propertyName[7]: #Knox
                    if self.buildings == 0:
                        return 10
                    elif self.buildings == 1:
                        return 50
                    elif self.buildings == 2:
                        return 150
                    elif self.buildings == 3:
                        return 450
                    elif self.buildings == 4:
                        return 625
            elif self.name == property.propertyName[8]: #Bonner
                    if self.buildings == 0:
                        return 10
                    elif self.buildings == 1:
                        return 50
                    elif self.buildings == 2:
                        return 150
                    elif self.buildings == 3:
                        return 450
                    elif self.buildings == 4:
                        return 625
            elif self.name == property.propertyName[9]: #Talbert
                    if self.buildings == 0:
                        return 10
                    elif self.buildings == 1:
                        return 50
                    elif self.buildings == 2:
                        return 150
                    elif self.buildings == 3:
                        return 450
                    elif self.buildings == 4:
                        return 625
            elif self.name == property.propertyName[10]: #Hochstetter
                    if self.buildings == 0:
                        return 12
                    elif self.buildings == 1:
                        return 60
                    elif self.buildings == 2:
                        return 180
                    elif self.buildings == 3:
                        return 500
                    elif self.buildings == 4:
                        return 700
            elif self.name == property.propertyName[11]: #Cooke
                    if self.buildings == 0:
                        return 22
                    elif self.buildings == 1:
                        return 110
                    elif self.buildings == 2:
                        return 330
                    elif self.buildings == 3:
                        return 800
                    elif self.buildings == 4:
                        return 1000
            elif self.name == property.propertyName[12]: #Fronczak
                    if self.buildings == 0:
                        return 22
                    elif self.buildings == 1:
                        return 110
                    elif self.buildings == 2:
                        return 330
                    elif self.buildings == 3:
                        return 800
                    elif self.buildings == 4:
                        return 1000
            elif self.name == property.propertyName[13]: #NSC
                    if self.buildings == 0:
                        return 24
                    elif self.buildings == 1:
                        return 120
                    elif self.buildings == 2:
                        return 360
                    elif self.buildings == 3:
                        return 850
                    elif self.buildings == 4:
                        return 1050
            elif self.name == property.propertyName[14]: #Ketter
                    if self.buildings == 0:
                        return 24
                    elif self.buildings == 1:
                        return 120
                    elif self.buildings == 2:
                        return 360
                    elif self.buildings == 3:
                        return 850
                    elif self.buildings == 4:
                        return 1050
            elif self.name == property.propertyName[15]: #Slee
                    if self.buildings == 0:
                        return 26
                    elif self.buildings == 1:
                        return 130
                    elif self.buildings == 2:
                        return 390
                    elif self.buildings == 3:
                        return 900
                    elif self.buildings == 4:
                        return 1100
            elif self.name == property.propertyName[16]: #Furnas
                    if self.buildings == 0:
                        return 26
                    elif self.buildings == 1:
                        return 130
                    elif self.buildings == 2:
                        return 390
                    elif self.buildings == 3:
                        return 900
                    elif self.buildings == 4:
                        return 1100
            elif self.name == property.propertyName[17]: #The Commons
                    if self.buildings == 0:
                        return 28
                    elif self.buildings == 1:
                        return 150
                    elif self.buildings == 2:
                        return 450
                    elif self.buildings == 3:
                        return 1000
                    elif self.buildings == 4:
                        return 1200
            elif self.name == property.propertyName[18]: #Center for the Arts
                    if self.buildings == 0:
                        return 28
                    elif self.buildings == 1:
                        return 150
                    elif self.buildings == 2:
                        return 450
                    elif self.buildings == 3:
                        return 1000
                    elif self.buildings == 4:
                        return 1200
            elif self.name == property.propertyName[19]: #Alumni Arena
                    if self.buildings == 0:
                        return 30
                    elif self.buildings == 1:
                        return 160
                    elif self.buildings == 2:
                        return 500
                    elif self.buildings == 3:
                        return 1100
                    elif self.buildings == 4:
                        return 1300
            elif self.name == property.propertyName[20]: #Davis
                    if self.buildings == 0:
                        return 35
                    elif self.buildings == 1:
                        return 175
                    elif self.buildings == 2:
                        return 500
                    elif self.buildings == 3:
                        return 1200
                    elif self.buildings == 4:
                        return 1400
            elif self.name == property.propertyName[21]: #Jarvis
                    if self.buildings == 0:
                        return 50
                    elif self.buildings == 1:
                        return 200
                    elif self.buildings == 2:
                        return 600
                    elif self.buildings == 3:
                        return 1400
                    elif self.buildings == 4:
                        return 1700 
                                      
        elif self.state == "hotel":
                if self.name == property.propertyName[0]: #Baird
                    return 250
                elif self.name == property.propertyName[1]: #Clements
                    return 450
                elif self.name == property.propertyName[2]: #Baldy
                    return 550
                elif self.name == property.propertyName[3]: #Jacobs
                    return 550
                elif self.name == property.propertyName[4]: #Park
                    return 600
                elif self.name == property.propertyName[5]: #O'Brian
                    return 600
                elif self.name == property.propertyName[6]: #Norton
                    return 600
                elif self.name == property.propertyName[7]: #Knox
                    return 750
                elif self.name == property.propertyName[8]: #Bonner
                    return 750
                elif self.name == property.propertyName[9]: #Talbert
                    return 750
                elif self.name == property.propertyName[10]: #Hochstetter
                    return 750
                elif self.name == property.propertyName[11]: #Cooke
                    return 900
                elif self.name == property.propertyName[12]: #Fronczak
                    return 900
                elif self.name == property.propertyName[13]: #NSC
                    return 950
                elif self.name == property.propertyName[14]: #Ketter
                    return 950
                elif self.name == property.propertyName[15]: #Slee
                    return 1000
                elif self.name == property.propertyName[16]: #Furnas
                    return 1000
                elif self.name == property.propertyName[17]: #The Commons
                    return 1050
                elif self.name == property.propertyName[18]: #Center for the Arts
                    return 1050
                elif self.name == property.propertyName[19]: #Alumni Arena
                    return 1100
                elif self.name == property.propertyName[20]: #Davis
                    return 1200
                elif self.name == property.propertyName[21]: #Jarvis
                    return 1400
            
        elif self.state == "railroad":
            if self.buildings == 1:
                return 25
            elif self.buildings == 2:
                return 50
            elif self.buildings == 3:
                return 100
            elif self.buildings == 4:
                return 200

