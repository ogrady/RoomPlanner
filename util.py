from typing import List, Tuple
from planning import Student, RoomInfo


CSV_SEPARATOR = ","


def generate_mock_students(length: int) -> List[Student]:
    ''' mockup method '''
    names = ("Abraham", "Allan", "Alsop", "Anderson", "Arnold", "Avery", "Bailey",
             "Baker", "Ball", "Bell", "Berry", "Black", "Blake", "Bond", "Bower",
             "Brown", "Buckland", "Burgess", "Butler", "Cameron", "Campbell", "Carr",
             "Chapman", "Churchill", "Clark", "Clarkson", "Coleman", "Cornish", "Davidson",
             "Davies", "Dickens", "Dowd", "Duncan", "Dyer", "Edmunds", "Ellison", "Ferguson",
             "Fisher", "Forsyth", "Fraser", "Gibson", "Gill", "Glover", "Graham", "Grant", "Gray",
             "Greene", "Hamilton", "Hardacre", "Harris", "Hart", "Hemmings", "Henderson",
             "Hill", "Hodges", "Howard", "Hudson", "Hughes", "Hunter", "Ince", "Jackson",
             "James", "Johnston", "Jones", "Kelly", "Kerr", "King", "Knox", "Lambert",
             "Langdon", "Lawrence", "Lee", "Lewis", "Lyman", "MacDonald",
             "Mackay", "Mackenzie", "MacLeod", "Manning", "Marshall", "Martin", "Mathis", "May", "McDonald", "McLean", "McGrath", "Metcalfe", "Miller", "Mills", "Mitchell", "Morgan", "Morrison", "Murray", "Nash", "Newman", "Nolan", "North", "Ogden", "Oliver", "Paige", "Parr", "Parsons", "Paterson", "Payne", "Peake", "Peters", "Piper", "Poole", "Powell", "Pullman", "Quinn", "Rampling", "Randall", "Rees", "Reid", "Roberts", "Robertson", "Ross", "Russell", "Rutherford", "Sanderson", "Scott", "Sharp", "Short", "Simpson", "Skinner", "Slater", "Smith", "Springer", "Stewart", "Sutherland", "Taylor", "Terry", "Thomson", "Tucker", "Turner", "Underwood", "Vance", "Vaughan", "Walker", "Wallace", "Walsh", "Watson", "Welch", "White", "Wilkins", "Wilson", "Wright", "Young")

    students = []
    for i in range(length):
        students.append(
            Student(names[i % len(names)], names[i % len(names)], 123456))
    return students


def distinct_prefix(s1: str, s2: str) -> str:
    '''
    Determines a distinct prefix to tell
    s1 apart from s2.
    s1: the first string.
    s2: the second string.
    returns: the common prefix of s1 and s2
                plus one letter to tell them apart from each other.
    '''
    if len(s1) == 0:
        return ""

    prefix = s1[0]
    i = 0
    while i < len(s1) - 1 and s1[i] == s2[i]:
        i += 1
        prefix += s1[i]
    return prefix


def load_file(file, separator, consumer):
    objects = []
    with open(file, "r") as fh:
        for line in fh.read().split("\n"):
            tokens = [t.strip() for t in line.split(separator)]
            objects.append(consumer(tokens))
    return objects


def load_room_infos(file) -> List[RoomInfo]:
    return load_file(file, CSV_SEPARATOR, lambda ts: RoomInfo(ts[0], int(ts[1]), int(ts[2])))


def load_students(file) -> List[Student]:
    return load_file(file, CSV_SEPARATOR, lambda ts: Student(firstname=ts[0], lastname=ts[1], matrikel=ts[2]))


def load_available_rooms(file) -> List[Tuple[str, int]]:
    return load_file(file, CSV_SEPARATOR, lambda ts: (ts[0], int(ts[1])))
