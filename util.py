from typing import List, Tuple
import planning


CSV_SEPARATOR = ","


def generate_mock_students(length: int) -> List[planning.Student]:
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

    return [planning.Student(names[i % len(names)], names[i % len(names)], 123456) for i in range(length)]


def load_file(file, separator, consumer):
    objects = []
    with open(file, "r") as fh:
        for line in fh.read().split("\n"):
            tokens = [t.strip() for t in line.split(separator)]
            objects.append(consumer(tokens))
    return objects


def load_room_infos(file) -> List[planning.RoomInfo]:
    return load_file(file, CSV_SEPARATOR, lambda ts: planning.RoomInfo(ts[0], int(ts[1]), int(ts[2])))


def load_students(file) -> List[planning.Student]:
    return load_file(file, CSV_SEPARATOR, lambda ts: planning.Student(lastname=ts[0], firstname=ts[1], matrikel=ts[2]))


def load_available_rooms(file) -> List[Tuple[str, int]]:
    return load_file(file, CSV_SEPARATOR, lambda ts: (ts[0], int(ts[1])))
