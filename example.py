# Example script
# given a hand and a wcj, calculate the MinScore and MinDist metrics, run a game between two strategies

from rummy import mscore, mdist, pprint_hand, pprint_declr, RummyGame, get_hand,MinscoreAgent,MindistOpp2Agent



print("Calculate metrics of a hand: ")
# 0 represents 2 of diamonds, 1 represents 3 of diamonds, 13 represents 2 of clubs, 26 represents 2 of hearts, 39 represents 2 of spades, 52 represents joker
# hand1 = list(map(int,input("Enter the hand (As numbers 0-52): ").split()))
# wcj = int(input("Enter the wild card joker: "))


hand1 = input("Enter the hand (As 2H, 10S, JD representing 2 of hearts, 10 of spades and Jack of diamonds): ").split()
hand1 = get_hand(hand1)
wcj = input("Enter the wild card joker: ")
wcj = get_hand([wcj,])[0]

min_score = mscore(hand1,wcj=wcj,declr=True)
min_dist = mdist(hand1,wcj=wcj,declr=True)

print("min score of the hand is: ", min_score[0])
print("The optimal declaration: ", pprint_declr(min_score[1]))
print("min dist of the hand is: ", min_dist[0])
print("The closest to declaration: ", pprint_declr(min_dist[1]))


# run a game between two strategies
print("Running game between strategies MinDistOpp2Agent and MinScoreAgent")
game = RummyGame([MindistOpp2Agent(name='MindistOpp',firstfold=4),MinscoreAgent(name='MinScore')], ndeck = 1, njoker= 1, handsize= 13, seed="12345",maxround=50,logfile="out.txt")
output = game.playgame()
print(output)