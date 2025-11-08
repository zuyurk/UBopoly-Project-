class player:
  def __init__(self, name, money, properties, chance, communityCards, jail, bankrupt):
    self.name = name #String name
    self.money = money  #Int money
    self.properties = properties  #List properties
    self.chance = chance #List chance cards
    self.communityCards = communityCards #List community cards
    self.jail = False #Bool in jail
    self.bankrupt = False #Bool if bankrupt

  #Get name
  def getName(self):
    return self.name
  
  #Returns list of properties owned
  def getProperties(self):
    if not self.properties:
      return "No Properties Owned"
    
    return self.properties;

  #Returns int of amount of money
  def getMoney(self):
    if self.money < 0 and len(self.property) <= 0:
      self.bankrupt = True;
    
    return self.money;

  #Return list of all chance cards they own
  def getChanceCards(self):
    if not self.chance:
      return "No Chance Cards Owned"
    
    return self.chance;

  #Return list of all community cards they own
  def getCommunityCards(self):
    if not self.communityCardsOwned:
      return "No Community Cards Owned"
    
    return self.communityCards

  #Boolean if they are in jail or not
  def getJailStatus(self):
    return self.jail
  
  #Boolean if they are bankrupt or not
  def getBankruptStatus(self):
    return self.bankrupt


