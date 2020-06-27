import sys
from planning import RoomPlanner, RoomUsage
import util
from markdeep import MarkdeepDocument, generate_student_list


DEBUG = True


def print_attendence_list(room: RoomUsage):
    md = MarkdeepDocument()
    md.append("# Raum %s\n" % (room.name,))
    md.append(generate_student_list(room.students))
    md.to_file("room_%s.md.html" % (room.name,))


def main(args):
    rooms = util.load_room_infos("rooms.csv")
    planner = RoomPlanner(rooms)
    students = util.generate_mock_students(200) if DEBUG else util.load_students("students.csv")
    seats = util.load_available_rooms("available_rooms.csv")

    distribution = planner.plan(seats, students)

    for d in distribution:
        print_attendence_list(d)


if __name__ == "__main__":
    main(sys.argv[1:])
