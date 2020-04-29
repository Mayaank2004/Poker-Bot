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
print(d)


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


def dealToPlayer ( deck: list = None, player: Player = None, cards_num=2 ):
	for t in range(0, cards_num):
		rnum = rand.randint(0, len(deck) - 1)
		'''try:
			print(rnum,deck[rnum])
		except:
			print(rnum/100,len(deck))'''
		player.cards.append(deck[rnum])
		deck.pop(rnum)
	return deck


def deal_to_Table ( deck ):
	table = []
	for n in range(0, 5):
		rnum = rand.randint(0, len(deck) - 1)
		table.append(deck[rnum])
		deck.pop(rnum)
	return deck, table


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


# dbl pair,pair,high


def compareHands ( pList ):
	rankList = [n.rank for n in pList]
	winRank = []
	for n in range(len(rankList)):
		if rankList[n] == max(rankList):
			winRank.append(pList[n])
	if len(winRank) == 1:
		winner = winRank[0]
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
			winner = winsubRank[0]
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
				winner = winKicker[0]
			else:
				winner = None
	return winner


if __name__ == "__main__":

	time0 = time.perf_counter()

	mega = {}  # mega ={card:[[[[p2 hand],[table],[winner]],[rep]],[win P1,winP2,tie]]}

	numP = 2
	length = 0

	suit1 = ['S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'S11', 'S12', 'S13', 'S14']
	suit2 = ['C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14']

	ties = 0

	for t in range(10**length):

		r = []
		r = setupPlayers(numP)  # sets up players

		decknow = deckOG.copy()
		rand.shuffle(decknow)
		# print(decknow)
		r[0].cards = ["S2", "S3"]
		r[1].cards = ["S4", "S5"]
		table = ["S6", "S7", "S8", "S9", "S11"]
		decknow.remove(r[0].cards[0])
		decknow.remove(r[0].cards[1])
		# for n in r[1:]:
		#	decknow = dealToPlayer(decknow, n)
		# decknow, table = deal_to_Table(decknow)

		for n in r:
			n.tot_cards = n.cards + table
			n.tot_cards.sort()
			setValue(n)

		winner = compareHands(r)

	# if t % 5000 == 0:
	# print(t / (10**length)
	print(winner.num)
	print(time.perf_counter() - time0)
