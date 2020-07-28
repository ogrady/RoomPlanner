# Room Planner
This utility was built to distribute students over a number of available rooms. The tool will try to use as few rooms as possible and distribute the students evenly across the rooms.
Also generates attendence lists in Markdeep format and signs for the doors.

# Setup
This tool has no dependencies. But it needs several input files to be present in the root directory of the project.

## rooms.csv
Should contain a list of generally available rooms. This list can be extensive and contain rooms that are not available for the exam. Each line contains the name of the room, followed by two integers denoting the number of available seats. Note that this tool was created during the COVID19 outbreak, so rooms had two seat capacities that were alternated between exams, thus the two integers.

Example:

```
N1, 16, 16
N2, 20, 10
Auditorium, 60, 70
```

## available_rooms.csv
The rooms that are actually available for the exam. Should be a subset of what was specified in `rooms.csv`. The format is the name of the room, followed by `1` or `2` to denote, which capacity should be used.

Example:

```
N1, 1
Auditorium, 2
```

## students.csv
List of students that should be distributed. Format is firstname, lastname, matrikel.

Example:

```
Foo, Bar, 123456
Alice, Smith, 234567
Bob, Miller, 345678
```

## config.json
Additional information needed to generate the door signs.

```
{
	"exam_info": {
		"title": "Main Exam Math III",
		"date": "20.04.2020",
		"start": "16:00",
		"end": "17:00"
	}
}
```