from __future__ import annotations
import collections
from typing import List, Tuple


RoomInfo = collections.namedtuple("Room", "name capacity1 capacity2")
RoomCapacity = collections.namedtuple("RoomCapacity", "name capacity")
Student = collections.namedtuple("Student", "firstname lastname matrikel")


class RoomUsage(object):
    def __init__(self, name: str, capacity: int, students: List[Student]):
        self.name = name
        self.capacity = capacity
        self.students = students

    def __str__(self):
        return "%s %d/%d (%d%%)" % (self.name, self.usage, self.capacity, self.percentage)

    def __repr__(self):
        return str(self)

    @property
    def usage(self) -> int:
        ''' Used number of seats '''
        return len(self.students)

    @property
    def remaining_capacity(self) -> int:
        ''' Remaining number of seats '''
        return self.capacity - self.usage

    @property
    def percentage(self) -> int:
        ''' percentage 0 - 100 '''
        return self.usage * 100 / self.capacity

    @property
    def room_sign(self):
        ''' Creates the room sign '''
        return "%s – %s" % (_distinct_prefix(self.students[0].lastname,
                                             self.students[1].lastname),
                            _distinct_prefix(self.students[-2].lastname,
                                             self.students[-1].lastname))

    def pop_front_student(self) -> Student:
        '''
        Pops a student from the front of the list.
        returns: poped student or None, if list was empty.
        '''
        if self.usage > 0:
            s = self.students[0]
            self.students = self.students[1:]
        return s

    def pop_back_student(self) -> Student:
        '''
        Pops a student from the front of the list.
        returns: poped student or None, if list was empty.
        '''
        if self.usage > 0:
            s = self.students[-1]
            self.students = self.students[:-1]
        return s

    def add_student(self, student: Student):
        '''
        Adds a student to the list of students.
        List will be sorted afterwards.
        student: student to add.
        '''
        if student is not None:
            self.students.append(student)
            self.students.sort(key=lambda s: (s.lastname, s.firstname))
        if self.usage > self.capacity:
            raise Exception("Room %s is overburdened (%d/%d)" %
                            (self.name, self.usage, self.capacity))

    def compare(self, other: RoomUsage) -> int:
        '''
        Compares this RoomUsage to another. That is,
        if self contains a student with lower lexicographic
        order than other, -1 will be returned, else 1 is returned.
        returns: -1 or 1
        '''
        if self.usage == 0 or other.usage == 0:
            raise Exception("can not compare unused rooms")
        return -1 if self.students[0].lastname < other.students[0].lastname else 1

    def funnel_into(self, other: RoomUsage, amount: int = 1):
        '''
        Removes students from self into other.
        Depending on the relative order of the two rooms
        students will either be removed from the front
        or the back of self. Should only be used with
        adjacent rooms, to avoid breaking the overall order.
        other: the other RoomUsage to funnel students into.
        amount: number of Students to funnel.
        '''
        pop = lambda u: u.pop_back_student()
        if self.compare(other) < 0:
            pop = lambda u: u.pop_back_student()

        for i in range(amount):
            other.add_student(pop(self))

    def balance(self, other: RoomUsage, delta_percentage: int = 10) -> int:
        '''
        Balances two rooms in terms of usage.
        The more populated room will funnel students
        into the other room until their percentages are about even.
        other: other RoomUsage to balance self with.
        delta_percentage: percentage the two rooms can differ
                            before funneling is stopped.
        returns: number of funnels that have been done.
        '''
        if self.percentage > other.percentage:
            source = self
            destination = other
        else:
            source = other
            destination = self

        funnels = 0
        while source.percentage - other.percentage > delta_percentage:
            source.funnel_into(destination)
            funnels += 1
        return funnels


class RoomPlanner(object):
    def __init__(self, room_infos):
        self.room_infos = room_infos

    def _get_seats(self, available: List[Tuple[str, int]]) -> List[RoomCapacity]:
        '''
        Gets the list of available seats.
        available: list of pairs, where the first element is the name of the room,
                    the second is the specifier for the exam (1 or 2)
        returns: list of pairs, where the first element is
                    the name of the room, the second is the number of available seats.
                    This list is ordered by capacity (descending).
        '''
        rooms = []
        for available_name, available_exam in available:
            r = next((room for room in self.room_infos if room.name == available_name), None)
            rooms.append(RoomCapacity(
                r.name, r.capacity1 if available_exam == 1 else r.capacity2))
        return rooms

    def _distribute(self, students: List[Student], rooms: List[RoomCapacity]) -> List[RoomCapacity]:
        '''
        Distributes the students onto the rooms.
        Larger rooms will be preferred over small rooms.
        Rooms will be filled to the last seat.
        students: list of students to distribute.
        rooms: the available rooms to distribute the students on.
        returns: a list of capacities for all used rooms.
                    This list may be shorter than the overall capacity
                    if some rooms go unused.
        '''
        students = sorted(students, key=lambda s: (s.lastname, s.firstname))
        rooms = sorted(rooms, key=lambda r: r[1], reverse=True)
        used_rooms = []

        i = 0
        for room_name, capacity in rooms:
            room_students = students[i:(i + capacity)]
            i += capacity
            used_rooms.append(RoomUsage(room_name, capacity, room_students))

        return [r for r in used_rooms if len(r.students) > 0]

    def _balance(self, distribution: List[RoomUsage], delta_percentage: int = 10) -> List[RoomUsage]:
        '''
        Balances a list of RoomUsages by shifting students between adjacent
        rooms until balance has been achieved, which is measured by no two rooms being
        more than delta_percentage percent apart in terms of their usage.
        distribution: rooms to balance.
        delta_percentage: percentile below which the difference of two adjacent rooms
                            is considered to be balanced. Ie if two adjacent rooms
                            have percentiles 20 and 80, they are not balanced,
                            while they would be for 50 and 60, given that
                            the delta_percentage is 10.
        '''
        changed = True
        while changed:
            changed = False
            for i in range(len(distribution) - 1):
                d1 = distribution[i]
                d2 = distribution[i + 1]
                changed = changed or d1.balance(d2, delta_percentage) > 0

    def plan(self, available_rooms: List[Tuple[str, int]], students: List[Student]) -> List[RoomUsage]:
        seats = self._get_seats(available_rooms)
        distribution = self._distribute(students, seats)
        self._balance(distribution)
        return distribution
