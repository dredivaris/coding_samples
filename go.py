#!/usr/bin/env python

# Go is a 2 player board game with simple rules. Two players alternate turns
# placing stones on a grid. If a stone is surrounded on 4 sides by stones of
# the opponent, it is captured. If a group of stones are surrounded, they are
# captured.
# See http://en.wikipedia.org/wiki/Rules_of_Go#Capture for a visual explanation.

# Below is an implementation of a Go board. Please write some code in the
# move() method to check for captures and output something when a capture
# occurs. The sample moves represent a capture of two black stones.

from collections import namedtuple, deque
import operator

EMPTY = 0
BLACK = 1
WHITE = 2

surrounding = [(-1, 0), (1, 0), (0, -1), (0, 1)]
Piece = namedtuple('Piece', ['row', 'col'])


class Group(object):
    """
    Represents a group of one or more adjacent stones of a homogeneous color.
    """
    def __init__(self, piece, color):
        self.color = color
        self.pieces = set()
        self.pieces.add(piece)
        # fifo queue to handle checking surrounded status of each stone in the group
        self.unprocessed = deque()
        self.unprocessed.append(piece)

    def __contains__(self, key):
        return key in self.pieces

    def __eq__(self, other):
        return self.pieces == other.pieces and set(self.unprocessed) == set(other.unprocessed)

    def add(self, piece):
        if piece not in self.pieces:
            self.unprocessed.append(piece)
        self.pieces.add(piece)

    def get_next(self):
        if self.unprocessed:
            return self.unprocessed.popleft()
        else:
            return None

    def __repr__(self):
        return '{} Group represented by indices: {}'.format(
            {WHITE: 'White', BLACK: 'Black'}[self.color],
            ', '.join('({}, {})'.format(p.row, p.col) for p in self.pieces)
        )


class Board(object):
    def __init__(self):
        self.board = [[EMPTY] * 19 for _ in xrange(19)]  # 2d 19x19 matrix of 0's

    def __str__(self):
        s = ''
        for row in self.board:
            if s:
                s += '\n'
            for sq in row:
                if sq:
                    s += ' ' + str(sq)
                else:
                    s += ' _'
        return s

    def move(self, color, row, col):
        self.board[row][col] = color
        captured, group = self._find_first_captured_group()
        if captured:
            print 'captured: ', group

    def _find_first_captured_group(self):
        row_len, col_len = len(self.board), len(self.board[0])
        checked_groups = []
        # loop through every location on board, check for captured group at that location
        # keep a list of already tested groups to protect against redundate checks
        for row in xrange(row_len):
            for col in xrange(col_len):
                if self.board[row][col] != 0:
                    captured, group = self._check_for_captured_group_at_location(
                        row, col, checked_groups)
                    if group:
                        checked_groups.append(group)
                    if captured:
                        return captured, group
        return False, None

    def _check_for_captured_group_at_location(self, row, col, already_checked):
        # skip if index is in an already checked group
        if any(Piece(row=row, col=col) in c for c in already_checked):
            return False, None
        group = self._detect_group_at_location(row, col)
        if self._is_surrounded_group(group):
            return True, group
        else:
            return False, group

    def _surrounding_indices(self, point):
        point = (point.row, point.col)
        for shift in surrounding:
            val = tuple(map(operator.add, point, shift))
            yield Piece(row=val[0], col=val[1])

    def _detect_group_at_location(self, row, col):
        color = self.board[row][col]
        group = Group(Piece(row=row, col=col), color)

        # Loop through all known pieces of a group (will begin with just one piece).
        # Check surrounding pieces and add to the group if they are the same color. Also add these
        # pieces to be checked later in the loop (the Group class automatically adds them
        # to an unprocessed queue which this loop pulls from on subsequent checks.)
        current = group.get_next()
        while current:
            for p in self._surrounding_indices(current):
                try:
                    if self.board[p.row][p.col] == group.color and p not in group:
                        group.add(p)
                except IndexError:
                    pass
            current = group.get_next()
        return group

    def _is_surrounded_group(self, group):
        return all(self._piece_surrounded(piece, group.color) for piece in group.pieces)

    def _piece_surrounded(self, piece, color):
        def is_not_empty(p):
            if p.row < 0 or p.col < 0:
                return True
            try:
                return self.board[p.row][p.col] != 0
            except IndexError:
                return True
        return all(is_not_empty(p) for p in self._surrounding_indices(piece))

print 'Example 1: '
b = Board()
b.move(BLACK, 4, 4)
b.move(BLACK, 4, 5)
b.move(WHITE, 3, 4)
b.move(WHITE, 3, 5)
b.move(WHITE, 4, 3)
b.move(WHITE, 4, 6)
b.move(WHITE, 5, 4)
b.move(WHITE, 5, 5)
print b

print 'Example 2: '
b = Board()
b.move(BLACK, 4, 4)
b.move(BLACK, 4, 5)
b.move(BLACK, 4, 6)
b.move(BLACK, 5, 6)
b.move(WHITE, 3, 4)
b.move(WHITE, 3, 5)
b.move(WHITE, 3, 6)
b.move(WHITE, 4, 3)
b.move(WHITE, 4, 7)
b.move(WHITE, 5, 4)
b.move(WHITE, 5, 5)
b.move(WHITE, 5, 7)
b.move(WHITE, 6, 6)
print b
print

print 'Example 3: '
b = Board()

b.move(BLACK, 7, 0)
b.move(BLACK, 8, 0)
b.move(BLACK, 9, 0)
b.move(BLACK, 8, 1)
b.move(BLACK, 9, 1)
b.move(WHITE, 6, 0)
b.move(WHITE, 7, 1)
b.move(WHITE, 8, 2)
b.move(WHITE, 9, 2)
b.move(WHITE, 10, 0)
b.move(WHITE, 10, 1)
print b
