import random as rand
import time
from collections import Counter

deckOG = []
d = {}
t = 0
for s in ['S', 'C', 'D', 'H']:  # setup deck of cards
	for num in range(2, 15):
		deckOG.append(s + str(num))
		d[t] = s + str(num)
		t += 1
# print(deckOG)
del s, num


class Player:
	def __init__ ( self, n ):
		self.num = n
		self.cards = []
		self.tot_cards = []
		self.val_cards = []
		self.suits = []
		self.values = []
		self.rank = -1
		self.subRank = 0
		self.kicker = []


def setupPlayers ( num_players ):
	playerList = []
	for n in range(0, num_players):
		playerList.append(Player(n))
	return playerList


def setValue ( player: Player = None ):  # ranks the hand

	for n in player.tot_cards:
		player.suits.append(n[0])
		player.values.append(int(n[1:]))

	listCards = player.values.copy()
	listCards = list(dict.fromkeys(listCards))
	listCards.sort()

	def checkFlush ( player ):
		flush = False
		for n in ["S", "C", "D", "H"]:
			if player.suits.count(n) >= 5:
				flush = True
				flush_suit = n
				break
		if flush == True:
			return True, flush_suit
		else:
			return False, None

	def checkStraight ( cards ):
		straight = False
		subStraight = []
		diff = []
		cards = [int(n[1:]) for n in cards]
		listCards = list(dict.fromkeys(cards.copy()))
		listCards.sort()

		for n in range(len(listCards) - 1):
			diff.append(listCards[n + 1] - listCards[n])
		for n in range(len(diff) - 3):
			if diff[n] == 1 and diff[n + 1] == 1 and diff[n + 2] == 1 and diff[n + 3] == 1:
				straight = True
				# print("straight",straight)
				subStraight = listCards[n]
		return straight, subStraight

	straight, subStraight = checkStraight(player.tot_cards)
	flush, flush_suit = checkFlush(player)

	count = Counter(player.values)

	if flush and straight:
		cardList = [x for x in player.tot_cards if x[0] == flush_suit]
		# print(cardList)
		newStraight, newSubStraight = checkStraight(cardList)
		if newStraight:
			player.rank = 9
			player.subRank = [newSubStraight]

	if player.rank == -1:
		for n in listCards:
			if count[n] == 4:
				player.rank = 8  # four of a kind
				player.subRank = [n]
				l = listCards.copy()
				l.remove(n)
				player.kicker = [max(l)]
				del l
	if player.rank == -1:
		for n in listCards:
			if count[n] == 3:
				l = listCards.copy()
				l.remove(n)
				for m in l:
					if count[m] >= 2:
						player.rank = 7  # full house
						player.subRank = [n, m]

	if player.rank == -1:
		if flush:
			player.rank = 6  # flush
			t = []
			l = player.tot_cards.copy()
			for n in l:
				if n[0] == flush_suit:
					t.append(n)
			t.sort(reverse=True)
			player.subRank = t
			del t
	if player.rank == -1:
		if straight:
			player.rank = 5  # straight
			player.subRank = [subStraight]
	if player.rank == -1:
		for n in listCards:
			if count[n] == 3:
				li = []
				player.rank = 4  # 3 of a kind
				player.subRank = [n]
				l = player.values.copy()
				l = [t for t in l if t != n]
				li.append(max(l))
				l.remove(max(l))
				li.append(max(l))
				player.kicker = li
	if player.rank == -1:
		for n in listCards:
			if count[n] == 2:
				li = [t for t in listCards.copy() if t != n]
				for m in li:
					if count[m] == 2:
						player.rank = 3  # dbl pair
						player.subRank = [n, m]
						lt = [t for t in player.values.copy() if t not in [n, m]]
						player.kicker = [max(lt)]
						player.subRank.sort(reverse=True)
	if player.rank == -1:
		for n in listCards:
			if count[n] == 2:
				li = []
				player.rank = 2  # pair
				player.subRank = [n]
				l = [t for t in player.values.copy() if t != n]
				li.append(max(l))
				l.remove(max(l))
				li.append(max(l))
				l.remove(max(l))
				li.append(max(l))

				player.kicker = li
	if player.rank == -1:
		li = []
		player.rank = 1  # high card
		l = [t for t in player.values.copy()]
		li.append(max(l))
		l.remove(max(l))

		li.append(max(l))
		l.remove(max(l))

		li.append(max(l))
		l.remove(max(l))

		li.append(max(l))
		l.remove(max(l))

		li.append(max(l))

		player.kicker = li


def compareHands ( pList ):
	rankList = [n.rank for n in pList]
	winRank = []
	for n in range(len(rankList)):
		if rankList[n] == max(rankList):
			winRank.append(pList[n])
	if len(winRank) == 1:
		winner = winRank[0].num
	else:
		subRankcheck = -1
		winsubRank = []
		for n in winRank:
			if subRankcheck == -1:
				subRankcheck = n.subRank
			elif n.subRank > subRankcheck:
				subRankcheck = n.subRank
		for n in winRank:
			if n.subRank == subRankcheck:
				winsubRank.append(n)
		if len(winsubRank) == 1:
			winner = winsubRank[0].num
		else:
			kickerCheck = -1
			winKicker = []
			for n in winsubRank:
				if kickerCheck == -1:
					kickerCheck = n.kicker
				elif n.kicker > kickerCheck:
					kickerCheck = n.kicker
			for n in winsubRank:
				if n.kicker == kickerCheck:
					winKicker.append(n)
			if len(winKicker) == 1:
				winner = winKicker[0].num
			else:
				winner = -1
	return winner


class Eval():
	def __init__ ( self, length=10**5 ):

		time0 = time.perf_counter()

		Dump = {}  # Dump ={card:[[[[p2 hand],[table],[self.winner]],[rep]],[win P1,winP2,tie]]}

		numP = 2
		self.length = length

		self.suit1 = ['S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'S11', 'S12', 'S13', 'S14']
		self.suit2 = ['C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14']

		for t in range(length):

			self.r = setupPlayers(numP)  # sets up players

			self.deckNow = deckOG.copy()
			rand.shuffle(self.deckNow)
			# print(decknow)
			self.table = []
			for n in self.r:
				self.dealToPlayer(n)
			# for n in r[1:]:
			#	decknow = dealToPlayer(decknow, n)
			table = self.deal_to_Table()

			for n in self.r:
				n.tot_cards = n.cards + self.table
				n.tot_cards.sort()
				setValue(n)

			self.winner = compareHands(self.r)

		print(time.perf_counter() - time0)

	def dealToPlayer ( self, player: Player = None, cards_num=2 ):
		for t in range(0, cards_num):
			rnum = rand.randint(0, len(self.deckNow) - 1)
			player.cards.append(self.deckNow[rnum])
			self.deckNow.pop(rnum)

	def deal_to_Table ( self, ):
		table = []
		for n in range(0, 5):
			rnum = rand.randint(0, len(self.deckNow) - 1)
			self.table.append(self.deckNow[rnum])
			self.deckNow.pop(rnum)


x = Eval()
