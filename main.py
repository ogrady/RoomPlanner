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
        start, end = room.name_range
        doc.append("\n# Raum %s. %s – %s (%d/%d)\n" % (room.name, start, end, room.usage, room.capacity))
        doc.append("\n\n" + md.generate_student_list(room.students[i:(i + step)]))
        doc.append("\n+++++")
        i += step
    doc.to_file("output/%d_room_%s.md.html" % (room.id, room.name,))


def print_room_signs(room: planning.RoomUsage, title, date, start_time, end_time):
    doc = md.MarkdeepDocument(slides=True)
    doc.append("\n# %s" % (title,))
    doc.append("\n<center>")
    doc.append("\n<p>%s, %s – %s Uhr</p>" % (date, start_time, end_time))
    doc.append("\n<p>%s</p>" % (room.name,))
    doc.append("\n<p>**Bitte nicht stören**</p>")
    doc.append("\n</center>")
    doc.append("\n## Namen: %s – %s" % room.name_range)
    doc.to_file("output/%d_door_%s.md.html" % (room.id, room.name,))


def main(args):
    rooms = util.load_room_infos("rooms.csv")
    planner = planning.RoomPlanner(rooms)
    students = util.generate_mock_students(364) if DEBUG else util.load_students("students.csv")
    seats = util.load_available_rooms("available_rooms.csv")

    distribution = planner.plan(seats, students)

    for room in distribution:
        print_attendence_list(room)
        print_room_signs(room, "Hauptklausur Informatik 2", "31.07.2020", "14:00", "16:00")


if __name__ == "__main__":
    main(sys.argv[1:])
