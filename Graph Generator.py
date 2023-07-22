import json, os, math
import matplotlib.pyplot as plt
import os.path

NAME = 0
AGE = 1
TOUCHTYPER = 2
RULERSCORE = 3
COLOUR = 4
SEQUENCE = 5
SEQUENCE1 = 5
SEQUENCE2 = 6
GROUP = 4

TEST_COLOUR = 0
TEST_TOTAL = 1
TEST_SEQUENCE = 2

BW_FIRST = 0
CL_FIRST = 1

def Sort(sub_li):

    # print(sub_li)

    l = len(sub_li)
     
    for i in range(0, l):
        for j in range(0, l-i-1):
             
            if (sub_li[j][1] > sub_li[j + 1][1]):
                tempo = sub_li[j]
                sub_li[j] = sub_li[j + 1]
                sub_li[j + 1] = tempo

    # print(sub_li)
     
    return sub_li

def PutTogetherDataSequences(sequences):
    newSequences = []
    for sequence in sequences:
        for letter in sequence[TEST_SEQUENCE]:
            newSequences.append(letter)

    # print(newSequences)
    newSequences = Sort(newSequences)
    return newSequences

def importJson(dataName):
    with open(os.path.join(os.path.dirname(__file__), f"{dataName}.json"), 'r') as f:
        newData = json.load(f)
        return newData

def makeNewSequence(entry, group):
    newSubject = []
    newSubject.append(entry[NAME])
    newSubject.append(entry[AGE])
    newSubject.append(entry[TOUCHTYPER])
    newSubject.append(entry[RULERSCORE])
    newSubject.append(group)
    newSubject.append(prepSequenceToJoin(entry))
    return newSubject

def prepSequenceToJoin(entry):
    newSequence = []
    newSequence.append(entry[COLOUR])
    newSequence.append(len(entry[SEQUENCE]))
    newSequence.append(entry[SEQUENCE])
    return newSequence

def sortData(BW_FIRST_DATA, CL_FIRST_DATA):
    allData = []

    entryUsed = False

    for entry in BW_FIRST_DATA:
        entryUsed = False

        if len(allData) == 0:
            allData.append(makeNewSequence(entry, BW_FIRST))
            entryUsed = True

        if entryUsed:
            continue

        for sequence in allData:
            if entry[NAME] == sequence[NAME]:
                sequence.append(prepSequenceToJoin(entry))
                entryUsed = True

            if entryUsed:
                break
        
        if not entryUsed:
            allData.append(makeNewSequence(entry, BW_FIRST))

    for entry in CL_FIRST_DATA:
        entryUsed = False

        if len(allData) == 0:
            allData.append(makeNewSequence(entry, CL_FIRST))
            entryUsed = True

        if entryUsed:
            continue

        for sequence in allData:
            if entry[NAME] == sequence[NAME]:
                sequence.append(prepSequenceToJoin(entry))
                entryUsed = True

            if entryUsed:
                break
        
        if not entryUsed:
            allData.append(makeNewSequence(entry, CL_FIRST))

    return allData

def graphEntry(entry):
    fig, ax = plt.subplots()

    name = f"Results of a {'Black-and-White' if entry[GROUP] == BW_FIRST else 'Colour'} Tested First, {entry[AGE]} Years Old, {'Touch Typer' if entry[TOUCHTYPER][0].lower() == 'y' else 'Sight Typer' if entry[TOUCHTYPER][0].lower == 'n' else ''} With Ruler Score {entry[RULERSCORE]}"

    a = graphSequence(ax, entry[SEQUENCE1])
    b = graphSequence(ax, entry[SEQUENCE2])

    ax.set_title(name)
    ax.axis([0, 30, 0, 70])

    ax.set_xlabel("Time (seconds)")
    ax.set_ylabel("Total Letter Count")

    ax.text(0.4, 63.59, f"Red: Coloured Round. Score: {len(entry[SEQUENCE2][TEST_SEQUENCE]) if entry[SEQUENCE2][TEST_COLOUR] else len(entry[SEQUENCE1][TEST_SEQUENCE])}\nBlack: Black and White Round. Score: {len(entry[SEQUENCE2][TEST_SEQUENCE]) if entry[SEQUENCE1][TEST_COLOUR] else len(entry[SEQUENCE1][TEST_SEQUENCE])}", bbox={'pad': 5, 'facecolor': 'white'})

    if not os.path.exists(f"_{name}.png"):
        fig.savefig(f"_{name}.png", dpi=200)
    else:
        notSaved = True
        count = 2
        while notSaved:
            if not os.path.exists(f"_{name} {count}.png"):
                fig.savefig(f"_{name} {count}.png", dpi=200)
                notSaved = False
            count += 1
    plt.close(fig)

def graphSequence(ax, sequence):
    times = []
    letters = []
    count = 0

    for i in sequence[TEST_SEQUENCE]:
        count += 1
        times.append(i[1])
        letters.append(count)

    ax.plot(times, letters, "r-" if sequence[TEST_COLOUR] else "k-")

    return len(letters)

def getAllRanges(data):
    BWFIRST_TOUCHTYPER_R1 = []
    BWFIRST_TOUCHTYPER_R2 = []
    CLFIRST_TOUCHTYPER_R1 = []
    CLFIRST_TOUCHTYPER_R2 = []
    CLFIRST_SIGHTTYPER_R2 = []
    BWFIRST_SIGHTTYPER_R1 = []
    BWFIRST_SIGHTTYPER_R2 = []
    CLFIRST_SIGHTTYPER_R1 = []

    for entry in data:
        if entry[GROUP] == BW_FIRST:
            if entry[TOUCHTYPER][0].lower() == "y":
                BWFIRST_TOUCHTYPER_R1.append(entry[SEQUENCE1][TEST_TOTAL])
                BWFIRST_TOUCHTYPER_R2.append(entry[SEQUENCE2][TEST_TOTAL])
            else:
                BWFIRST_SIGHTTYPER_R1.append(entry[SEQUENCE1][TEST_TOTAL])
                BWFIRST_SIGHTTYPER_R2.append(entry[SEQUENCE2][TEST_TOTAL])
        else:
            if entry[TOUCHTYPER][0].lower() == "y":
                CLFIRST_TOUCHTYPER_R1.append(entry[SEQUENCE1][TEST_TOTAL])
                CLFIRST_TOUCHTYPER_R2.append(entry[SEQUENCE2][TEST_TOTAL])
            else:
                CLFIRST_SIGHTTYPER_R1.append(entry[SEQUENCE1][TEST_TOTAL])
                CLFIRST_SIGHTTYPER_R2.append(entry[SEQUENCE2][TEST_TOTAL])

    print("BWFIRST_TOUCHTYPER_R1 Range: " + str(max(BWFIRST_TOUCHTYPER_R1)-min(BWFIRST_TOUCHTYPER_R1)) + " Max: " + str(max(BWFIRST_TOUCHTYPER_R1)) + " Min: " + str(min(BWFIRST_TOUCHTYPER_R1)))
    print("BWFIRST_TOUCHTYPER_R2 Range: " + str(max(BWFIRST_TOUCHTYPER_R2)-min(BWFIRST_TOUCHTYPER_R2)) + " Max: " + str(max(BWFIRST_TOUCHTYPER_R2)) + " Min: " + str(min(BWFIRST_TOUCHTYPER_R2)))
    print("BWFIRST_SIGHTTYPER_R1 Range: " + str(max(BWFIRST_SIGHTTYPER_R1)-min(BWFIRST_SIGHTTYPER_R1)) + " Max: " + str(max(BWFIRST_SIGHTTYPER_R1)) + " Min: " + str(min(BWFIRST_SIGHTTYPER_R1)))
    print("BWFIRST_SIGHTTYPER_R2 Range: " + str(max(BWFIRST_SIGHTTYPER_R2)-min(BWFIRST_SIGHTTYPER_R2)) + " Max: " + str(max(BWFIRST_SIGHTTYPER_R2)) + " Min: " + str(min(BWFIRST_SIGHTTYPER_R2)))
    print("CLFIRST_TOUCHTYPER_R1 Range: " + str(max(CLFIRST_TOUCHTYPER_R1)-min(CLFIRST_TOUCHTYPER_R1)) + " Max: " + str(max(CLFIRST_TOUCHTYPER_R1)) + " Min: " + str(min(CLFIRST_TOUCHTYPER_R1)))
    print("CLFIRST_TOUCHTYPER_R2 Range: " + str(max(CLFIRST_TOUCHTYPER_R2)-min(CLFIRST_TOUCHTYPER_R2)) + " Max: " + str(max(CLFIRST_TOUCHTYPER_R2)) + " Min: " + str(min(CLFIRST_TOUCHTYPER_R2)))
    print("CLFIRST_SIGHTTYPER_R1 Range: " + str(max(CLFIRST_SIGHTTYPER_R1)-min(CLFIRST_SIGHTTYPER_R1)) + " Max: " + str(max(CLFIRST_SIGHTTYPER_R1)) + " Min: " + str(min(CLFIRST_SIGHTTYPER_R1)))
    print("CLFIRST_SIGHTTYPER_R2 Range: " + str(max(CLFIRST_SIGHTTYPER_R2)-min(CLFIRST_SIGHTTYPER_R2)) + " Max: " + str(max(CLFIRST_SIGHTTYPER_R2)) + " Min: " + str(min(CLFIRST_SIGHTTYPER_R2)))

def graphAverages(data):
    BWFIRST_TOUCHTYPER_R1 = []
    BWFIRST_TOUCHTYPER_R2 = []
    CLFIRST_TOUCHTYPER_R1 = []
    CLFIRST_TOUCHTYPER_R2 = []
    CLFIRST_SIGHTTYPER_R2 = []
    BWFIRST_SIGHTTYPER_R1 = []
    BWFIRST_SIGHTTYPER_R2 = []
    CLFIRST_SIGHTTYPER_R1 = []

    BWFIRST_TOUCHTYPER_ENTRIES = 0
    CLFIRST_TOUCHTYPER_ENTRIES = 0
    BWFIRST_SIGHTTYPER_ENTRIES = 0
    CLFIRST_SIGHTTYPER_ENTRIES = 0

    for entry in data:
        if entry[GROUP] == BW_FIRST:
            if entry[TOUCHTYPER][0].lower() == "y":
                BWFIRST_TOUCHTYPER_R1.append(entry[SEQUENCE1])
                BWFIRST_TOUCHTYPER_R2.append(entry[SEQUENCE2])
                BWFIRST_TOUCHTYPER_ENTRIES += 1
            else:
                BWFIRST_SIGHTTYPER_R1.append(entry[SEQUENCE1])
                BWFIRST_SIGHTTYPER_R2.append(entry[SEQUENCE2])
                BWFIRST_SIGHTTYPER_ENTRIES += 1
        else:
            if entry[TOUCHTYPER][0].lower() == "y":
                CLFIRST_TOUCHTYPER_R1.append(entry[SEQUENCE1])
                CLFIRST_TOUCHTYPER_R2.append(entry[SEQUENCE2])
                CLFIRST_TOUCHTYPER_ENTRIES += 1
            else:
                CLFIRST_SIGHTTYPER_R1.append(entry[SEQUENCE1])
                CLFIRST_SIGHTTYPER_R2.append(entry[SEQUENCE2])
                CLFIRST_SIGHTTYPER_ENTRIES += 1

    BWFIRST_TOUCHTYPER_R1 = PutTogetherDataSequences(BWFIRST_TOUCHTYPER_R1)
    BWFIRST_TOUCHTYPER_R2 = PutTogetherDataSequences(BWFIRST_TOUCHTYPER_R2)
    CLFIRST_TOUCHTYPER_R1 = PutTogetherDataSequences(CLFIRST_TOUCHTYPER_R1)
    CLFIRST_TOUCHTYPER_R2 = PutTogetherDataSequences(CLFIRST_TOUCHTYPER_R2)
    BWFIRST_SIGHTTYPER_R1 = PutTogetherDataSequences(BWFIRST_SIGHTTYPER_R1)
    BWFIRST_SIGHTTYPER_R2 = PutTogetherDataSequences(BWFIRST_SIGHTTYPER_R2)
    CLFIRST_SIGHTTYPER_R1 = PutTogetherDataSequences(CLFIRST_SIGHTTYPER_R1)
    CLFIRST_SIGHTTYPER_R2 = PutTogetherDataSequences(CLFIRST_SIGHTTYPER_R2)

    fig, ax = plt.subplots()

    graphSequenceAverages(ax, BWFIRST_TOUCHTYPER_R1, 'b', BWFIRST_TOUCHTYPER_ENTRIES)
    graphSequenceAverages(ax, BWFIRST_TOUCHTYPER_R2, 'g', BWFIRST_TOUCHTYPER_ENTRIES)
    graphSequenceAverages(ax, CLFIRST_TOUCHTYPER_R1, 'r', CLFIRST_TOUCHTYPER_ENTRIES)
    graphSequenceAverages(ax, CLFIRST_TOUCHTYPER_R2, 'y', CLFIRST_TOUCHTYPER_ENTRIES)
    graphSequenceAverages(ax, BWFIRST_SIGHTTYPER_R1, 'k', BWFIRST_SIGHTTYPER_ENTRIES)
    graphSequenceAverages(ax, BWFIRST_SIGHTTYPER_R2, 'xkcd:gray', BWFIRST_SIGHTTYPER_ENTRIES)
    graphSequenceAverages(ax, CLFIRST_SIGHTTYPER_R1, 'c', CLFIRST_SIGHTTYPER_ENTRIES)
    graphSequenceAverages(ax, CLFIRST_SIGHTTYPER_R2, 'xkcd:purple', CLFIRST_SIGHTTYPER_ENTRIES)

    name = "All Scores - Averages"

    ax.set_title(name)
    ax.axis([0, 30, 0, 50])

    ax.text(0.4, 38.25, "Blue: Black and White First Touch Typers Round 1\nBlack: Black and White First Sight Typers Round 1\nGray: Black and White First Sight Typers Round 2\nGreen: Black and White First Touch Typers Round 2\nRed: Colour First Touch Typers Round 1\nYellow: Colour First Touch Typers Round 2\nCyan: Colour First Sight Typers Round 1\nPurple: Colour First Sight Typers Round 2", bbox={'pad': 5, 'facecolor': 'white'}, fontsize=6)

    ax.set_xlabel("Time (seconds)")
    ax.set_ylabel("Total Letter Count")

    fig.savefig(f"_{name}.png", dpi=200)

    print("BWFIRST_TOUCHTYPER_R1 Average Total Score: " + str(len(BWFIRST_TOUCHTYPER_R1)/BWFIRST_TOUCHTYPER_ENTRIES))
    print("BWFIRST_TOUCHTYPER_R2 Average Total Score: " + str(len(BWFIRST_TOUCHTYPER_R2)/BWFIRST_TOUCHTYPER_ENTRIES))
    print("BWFIRST_SIGHTTYPER_R1 Average Total Score: " + str(len(BWFIRST_SIGHTTYPER_R1)/BWFIRST_SIGHTTYPER_ENTRIES))
    print("BWFIRST_SIGHTTYPER_R2 Average Total Score: " + str(len(BWFIRST_SIGHTTYPER_R2)/BWFIRST_SIGHTTYPER_ENTRIES))
    print("CLFIRST_TOUCHTYPER_R1 Average Total Score: " + str(len(CLFIRST_TOUCHTYPER_R1)/CLFIRST_TOUCHTYPER_ENTRIES))
    print("CLFIRST_TOUCHTYPER_R2 Average Total Score: " + str(len(CLFIRST_TOUCHTYPER_R2)/CLFIRST_TOUCHTYPER_ENTRIES))
    print("CLFIRST_SIGHTTYPER_R1 Average Total Score: " + str(len(CLFIRST_SIGHTTYPER_R1)/CLFIRST_SIGHTTYPER_ENTRIES))
    print("CLFIRST_SIGHTTYPER_R2 Average Total Score: " + str(len(CLFIRST_SIGHTTYPER_R2)/CLFIRST_SIGHTTYPER_ENTRIES))

def graphSequenceAverages(ax, sequence, colour, entries):
    times = []
    letters = []
    count = 0

    for i in sequence:
        count += 1
        times.append(i[1])
        letters.append(count/entries)

    ax.plot(times, letters, colour)

    return len(letters)

DATASTRUCTURE = [[NAME, AGE, TOUCHTYPER, RULERSCORE, ['COLOUR1', ['SEQUENCE1']], ['COLOUR2', ['SEQUENCE2']]],[NAME, AGE, TOUCHTYPER, RULERSCORE, ['COLOUR1', ['SEQUENCE1']], ['COLOUR2', ['SEQUENCE2']]]]

data1 = importJson("results")

sortedData = sortData(data1, [])

getAllRanges(sortedData)
graphAverages(sortedData)

for entry in sortedData:
    graphEntry(entry)
