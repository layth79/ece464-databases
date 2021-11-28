# ECE-464 Assignment 2: queries on scraped data
# Layth Yassin
# Professor Sokolov

from pymongo import MongoClient

# querying data scraped from nba.com containing traditional basketball stats for the all-time leaders.
# the data includes 1309 players and 21 stats for each player.

# connect to mongoDB
client = MongoClient("mongodb+srv://m001-student:m001-mongodb-basics@sandbox.p6etn.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
f = open("queries.txt", "w")

# query 1
q1 = client['nbaStats']['playerStats'].aggregate([
    {
        '$sort': {
            'pts': -1
        }
    }, {
        '$limit': 10
    }
])
print("Query 1: Top 10 all-time total points scored\n")
f.write("Query 1: Top 10 all-time total points scored\n\n")
for i, player in enumerate(list(q1)):
    output = f"Rank {i + 1} : {player['name']} {player['pts']} career points"
    print(output)
    f.write(output + '\n')
f.write('\n\n') 
print("\n\n")

# query 2
q2 = client['nbaStats']['playerStats'].aggregate([
    {
        '$addFields': {
            'ppg': {
                '$trunc': [
                    {
                        '$divide': [
                            '$pts', '$gp'
                        ]
                    }, 3
                ]
            }
        }
    }, {
        '$sort': {
            'ppg': -1
        }
    }, {
        '$limit': 10
    }
])
print("Query 2: Top 10 all-time points per game\n")
f.write("Query 2: Top 10 all-time points per game\n\n")
for i, player in enumerate(list(q2)):
    output = f"Rank {i + 1} : {player['name']} {player['ppg']} points per game"
    print(output)
    f.write(output + '\n')
f.write('\n\n')
print("\n\n")

# query 3
q3 = client['nbaStats']['playerStats'].aggregate([
    {
        '$sort': {
            'fg%': -1
        }
    }, {
        '$limit': 10
    }
])
print("Query 3: Top 10 field goal percentage\n")
f.write("Query 3: Top 10 field goal percentage\n\n")
for i, player in enumerate(list(q3)):
    output = f"Rank {i + 1} : {player['name']} {player['fg%']}%"
    print(output)
    f.write(output + '\n')
f.write('\n\n')
print("\n\n")

# query 4
q4 = client['nbaStats']['playerStats'].aggregate([
    {
        '$sort': {
            '3pm': -1
        }
    }, {
        '$limit': 10
    }
])
print("Query 4: Effective field goal percentage of 10 players with most 3-pointers made\n")
f.write("Query 4: Effective field goal percentage of 10 players with most 3-pointers made\n\n")
for i, player in enumerate(list(q4)):
    output = f"Rank {i + 1} : {player['name']} efg% - {player['efg%']}%, fg% - {player['fg%']}%"
    print(output)
    f.write(output + '\n')
f.write('\n\n')
print("\n\n")

# query 5
q5 = client['nbaStats']['playerStats'].aggregate([
    {
        '$sort': {
            '3pm': 1
        }
    }, {
        '$limit': 10
    }
])
print("Query 5: Field goal percentage of 10 players with least 3-pointers made\n")
f.write("Query 5: Field goal percentage of 10 players with least 3-pointers made\n\n")
for i, player in enumerate(list(q5)):
    output = f"Rank {i + 1} : {player['name']} {player['fg%']}%"
    print(output)
    f.write(output + '\n')
f.write('\n\n')
print("\n\n")

# query 4 shows that the best shooters have an impressive efg%, which is the fg% taking
# into account the fact that 3-pointers are worth more than 2-pointers. The best shooters
# have noticeably higher efg% than those who made the least 3-pointers. However, shooters
# still have significantly lower efg% than the fg% of those with the highest fg%. Despite this,
# it is clear that the best shooters have impressive efg%, which coupled with the need for 3-pointers,
# show how valuable shooters are. 

# query 6
q6 = client['nbaStats']['playerStats'].aggregate([
    {
        '$sort': {
            '3pm': -1
        }
    }, {
        '$limit': 10
    }
])
print("Query 6: Top 10 highest 3-pointers made and their 3-point field goal percentage\n")
f.write("Query 6: Top 10 highest 3-pointers made and their 3-point field goal percentage\n\n")
for i, player in enumerate(list(q6)):
    output = f"Rank {i + 1} : {player['name']} 3pm - {player['3pm']}, 3p% - {player['3p%']}%"
    print(output)
    f.write(output + '\n')
f.write('\n\n')
print("\n\n")

# query 7
q7 = client['nbaStats']['playerStats'].aggregate([
    {
        '$addFields': {
            'bpg': {
                '$trunc': [
                    {
                        '$divide': [
                            '$blk', '$gp'
                        ]
                    }, 3
                ]
            },
            'rpg': {
                '$trunc': [
                    {
                        '$divide': [
                            '$reb', '$gp'
                        ]
                    }, 3
                ]
            }
        }
    }, {
        '$sort': {
            'bpg': -1
        }
    }, {
        '$limit': 10
    }
])
print("Query 7: Top 10 all-time blocks per game and their rebounds per game\n")
f.write("Query 7: Top 10 all-time blocks per game and their rebounds per game\n\n")
for i, player in enumerate(list(q7)):
    output = f"Rank {i + 1} : {player['name']} bpg - {player['bpg']}, rpg - {player['rpg']}"
    print(output)
    f.write(output + '\n')
f.write('\n\n')
print("\n\n")

# query 8
q8 = client['nbaStats']['playerStats'].aggregate([
    {
        '$addFields': {
            'rpg': {
                '$trunc': [
                    {
                        '$divide': [
                            '$reb', '$gp'
                        ]
                    }, 3
                ]
            }
        }
    }, {
        '$sort': {
            'rpg': -1
        }
    }, {
        '$limit': 10
    }
])
print("Query 8: Top 10 all-time rebounds per game\n")
f.write("Query 8: Top 10 all-time rebounds per game\n\n")
for i, player in enumerate(list(q8)):
    output = f"Rank {i + 1} : {player['name']} {player['rpg']} rebounds per game"
    print(output)
    f.write(output + '\n')
f.write('\n\n')
print("\n\n")
# query 7 and 8 show that contrary to what most think, the best shot blockers are
# not the best rebounders. query 8 shows the best rebounders have significantly
# better rpg

# query 9
q9 = client['nbaStats']['playerStats'].aggregate([
    {
        '$addFields': {
            'apg': {
                '$trunc': [
                    {
                        '$divide': [
                            '$ast', '$gp'
                        ]
                    }, 3
                ]
            },
            'tpg': {
                '$trunc': [
                    {
                        '$divide': [
                            '$tov', '$gp'
                        ]
                    }, 3
                ]
            }
        }
    }, {
        '$sort': {
            'apg': -1
        }
    }, {
        '$limit': 10
    }
])
print("Query 9: Top 10 all-time assists per game and their turnovers per game\n")
f.write("Query 9: Top 10 all-time assists per game and their turnovers per game\n\n")
for i, player in enumerate(list(q9)):
    output = f"Rank {i + 1} : {player['name']} apg - {player['apg']}, tpg - {player['tpg']}"
    print(output)
    f.write(output + '\n')
f.write('\n\n')
print("\n\n")

# query 10
q10 = client['nbaStats']['playerStats'].aggregate([
    {
        '$addFields': {
            'tpg': {
                '$trunc': [
                    {
                        '$divide': [
                            '$tov', '$gp'
                        ]
                    }, 3
                ]
            }
        }
    }, {
        '$sort': {
            'tpg': -1
        }
    }, {
        '$limit': 10
    }
])
print("Query 10: Top 10 all-time turnovers per game\n")
f.write("Query 10: Top 10 all-time turnovers per game\n\n")
for i, player in enumerate(list(q10)):
    output = f"Rank {i + 1} : {player['name']} {player['tpg']} turnovers per game"
    print(output)
    f.write(output + '\n')
f.write('\n\n')
print("\n\n")
# query 9 and 10 show that those who pass the most (i.e., high assists per game), tend
# to turnover the ball the most. As for the few players who did not appear in both queries
# they are known to be very ball-dominant so the results of these queries verify what most 
# would think

# query 11
q11 = client['nbaStats']['playerStats'].aggregate([
    {
        '$sort': {
            'ft%': -1
        }
    }, {
        '$limit': 10
    }
])
print("Query 11: Top 10 free throw percentage and their 3-point percentage\n")
f.write("Query 11: Top 10 free throw percentage and their 3-point percentage\n\n")
for i, player in enumerate(list(q11)):
    output = f"Rank {i + 1} : {player['name']} ft% - {player['ft%']}%, 3p% - {player['3p%']}%"
    print(output)
    f.write(output + '\n')
f.write('\n\n')
print("\n\n")
# query 4 and 11 confirm that the best free throw shooters are also usually among 
# the best 3-point shooters

# query 12
q12 = client['nbaStats']['playerStats'].aggregate([
    {
        '$addFields': {
            'mpg': {
                '$trunc': [
                    {
                        '$divide': [
                            '$min', '$gp'
                        ]
                    }, 3
                ]
            }
        }
    }, {
        '$sort': {
            'mpg': -1
        }
    }, {
        '$limit': 10
    }
])
print("Query 12: Top 10 all-time minutes per game\n")
f.write("Query 12: Top 10 all-time minutes per game\n\n")
for i, player in enumerate(list(q12)):
    output = f"Rank {i + 1} : {player['name']} {player['mpg']} minutes per game"
    print(output)
    f.write(output + '\n')

f.close()
