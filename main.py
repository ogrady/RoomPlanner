import sys
import planning
import markdeep as md
import util


DEBUG = False


def print_attendence_list(room: planning.RoomUsage):
    doc = md.MarkdeepDocument()

    i = 0
    step = 20
    while i < len(room.students):
        doc.append("\n# Raum %s – %s (%d/%d)\n" % (room.name, room.room_sign, room.usage, room.capacity))
        doc.append("\n\n" + md.generate_student_list(room.students[i:(i + step)]))
        doc.append("\n+++++")
        i += step
    doc.to_file("output/%d_room_%s.md.html" % (room.id, room.name,))


def main(args):
    rooms = util.load_room_infos("rooms.csv")
    planner = planning.RoomPlanner(rooms)
    students = util.generate_mock_students(364) if DEBUG else util.load_students("students.csv")
    seats = util.load_available_rooms("available_rooms.csv")

    distribution = planner.plan(seats, students)

    for d in distribution:
        print_attendence_list(d)


if __name__ == "__main__":
    main(sys.argv[1:])
