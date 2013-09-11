#===============================================================================
# Copyright (C) 2011 Diego Duclos
# Copyright (C) 2011-2013 Anton Vorobyov
#
# This file is part of Eos.
#
# Eos is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Eos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Eos. If not, see <http://www.gnu.org/licenses/>.
#===============================================================================


from unittest.mock import Mock, call

from eos.fit.holder.container import HolderList
from eos.tests.fit.holderContainer.containerTestCase import ContainerTestCase


class TestContainerOrderedRemove(ContainerTestCase):

    def setUp(self):
        ContainerTestCase.setUp(self)
        self.fitMock = self._setupContainerCheck()
        self.container = HolderList(self.fitMock)

    def testHolder(self):
        container = self.container
        fitMock = self.fitMock
        holder1 = Mock(spec_set=())
        holder2 = Mock(spec_set=())
        container.append(holder1)
        container.append(holder2)
        self.assertEqual(len(container), 2)
        fitCallsBefore = len(fitMock.mock_calls)
        container.remove(holder1)
        fitCallsAfter = len(fitMock.mock_calls)
        self.assertEqual(fitCallsAfter - fitCallsBefore, 1)
        self.assertEqual(fitMock.method_calls[-1], call._removeHolder(holder1))
        self.assertEqual(len(container), 1)
        self.assertIs(container[0], holder2)
        fitCallsBefore = len(fitMock.mock_calls)
        container.remove(holder2)
        fitCallsAfter = len(fitMock.mock_calls)
        self.assertEqual(fitCallsAfter - fitCallsBefore, 1)
        self.assertEqual(fitMock.method_calls[-1], call._removeHolder(holder2))
        self.assertEqual(len(container), 0)
        self.assertObjectBuffersEmpty(container)

    def testHolderAfterNones(self):
        container = self.container
        fitMock = self.fitMock
        holder1 = Mock(spec_set=())
        holder2 = Mock(spec_set=())
        holder3 = Mock(spec_set=())
        container.append(holder1)
        container.place(3, holder2)
        container.place(6, holder3)
        self.assertEqual(len(container), 7)
        self.assertIs(container[0], holder1)
        self.assertIsNone(container[1])
        self.assertIsNone(container[2])
        self.assertIs(container[3], holder2)
        self.assertIsNone(container[4])
        self.assertIsNone(container[5])
        self.assertIs(container[6], holder3)
        fitCallsBefore = len(fitMock.mock_calls)
        container.remove(holder2)
        fitCallsAfter = len(fitMock.mock_calls)
        self.assertEqual(fitCallsAfter - fitCallsBefore, 1)
        self.assertEqual(fitMock.method_calls[-1], call._removeHolder(holder2))
        self.assertEqual(len(container), 6)
        self.assertIs(container[0], holder1)
        self.assertIsNone(container[1])
        self.assertIsNone(container[2])
        self.assertIsNone(container[3])
        self.assertIsNone(container[4])
        self.assertIs(container[5], holder3)
        fitCallsBefore = len(fitMock.mock_calls)
        container.remove(holder3)
        fitCallsAfter = len(fitMock.mock_calls)
        self.assertEqual(fitCallsAfter - fitCallsBefore, 1)
        self.assertEqual(fitMock.method_calls[-1], call._removeHolder(holder3))
        self.assertEqual(len(container), 1)
        self.assertIs(container[0], holder1)
        container.remove(holder1)
        self.assertObjectBuffersEmpty(container)

    def testHolderFailure(self):
        container = self.container
        fitMock = self.fitMock
        holder1 = Mock(spec_set=())
        holder2 = Mock(spec_set=())
        container.append(holder1)
        fitCallsBefore = len(fitMock.mock_calls)
        self.assertRaises(ValueError, container.remove, holder2)
        fitCallsAfter = len(fitMock.mock_calls)
        self.assertEqual(fitCallsAfter - fitCallsBefore, 0)
        container.remove(holder1)
        self.assertEqual(len(fitMock.mock_calls), 2)
        self.assertRaises(ValueError, container.remove, holder1)
        self.assertObjectBuffersEmpty(container)

    def testNone(self):
        # Check that first found None is removed
        container = self.container
        fitMock = self.fitMock
        holder1 = Mock(spec_set=())
        holder2 = Mock(spec_set=())
        container.place(1, holder1)
        container.place(3, holder2)
        self.assertEqual(len(container), 4)
        self.assertIsNone(container[0])
        self.assertIs(container[1], holder1)
        self.assertIsNone(container[2])
        self.assertIs(container[3], holder2)
        fitCallsBefore = len(fitMock.mock_calls)
        container.remove(None)
        fitCallsAfter = len(fitMock.mock_calls)
        self.assertEqual(fitCallsAfter - fitCallsBefore, 0)
        self.assertEqual(len(container), 3)
        self.assertIs(container[0], holder1)
        self.assertIsNone(container[1])
        self.assertIs(container[2], holder2)
        container.remove(holder1)
        container.remove(holder2)
        self.assertObjectBuffersEmpty(container)

    def testNoneFailure(self):
        # Check that first found None is removed
        container = self.container
        fitMock = self.fitMock
        holder = Mock(spec_set=())
        container.append(holder)
        self.assertEqual(len(container), 1)
        self.assertIs(container[0], holder)
        fitCallsBefore = len(fitMock.mock_calls)
        self.assertRaises(ValueError, container.remove, None)
        fitCallsAfter = len(fitMock.mock_calls)
        self.assertEqual(fitCallsAfter - fitCallsBefore, 0)
        self.assertEqual(len(container), 1)
        self.assertIs(container[0], holder)
        container.remove(holder)
        self.assertObjectBuffersEmpty(container)

    def testIndexHolder(self):
        container = self.container
        fitMock = self.fitMock
        holder1 = Mock(spec_set=())
        holder2 = Mock(spec_set=())
        container.append(holder1)
        container.append(holder2)
        self.assertEqual(len(container), 2)
        self.assertIs(container[0], holder1)
        self.assertIs(container[1], holder2)
        fitCallsBefore = len(fitMock.mock_calls)
        container.remove(0)
        fitCallsAfter = len(fitMock.mock_calls)
        self.assertEqual(fitCallsAfter - fitCallsBefore, 1)
        self.assertEqual(fitMock.method_calls[-1], call._removeHolder(holder1))
        self.assertEqual(len(container), 1)
        self.assertIs(container[0], holder2)
        fitCallsBefore = len(fitMock.mock_calls)
        container.remove(0)
        fitCallsAfter = len(fitMock.mock_calls)
        self.assertEqual(fitCallsAfter - fitCallsBefore, 1)
        self.assertEqual(fitMock.method_calls[-1], call._removeHolder(holder2))
        self.assertEqual(len(container), 0)
        self.assertObjectBuffersEmpty(container)

    def testIndexNone(self):
        container = self.container
        fitMock = self.fitMock
        holder = Mock(spec_set=())
        container.place(1, holder)
        self.assertEqual(len(container), 2)
        self.assertIsNone(container[0])
        self.assertIs(container[1], holder)
        fitCallsBefore = len(fitMock.mock_calls)
        container.remove(0)
        fitCallsAfter = len(fitMock.mock_calls)
        self.assertEqual(fitCallsAfter - fitCallsBefore, 0)
        self.assertEqual(len(container), 1)
        self.assertIs(container[0], holder)
        container.remove(holder)
        self.assertObjectBuffersEmpty(container)

    def testIndexAfterNones(self):
        container = self.container
        fitMock = self.fitMock
        holder1 = Mock(spec_set=())
        holder2 = Mock(spec_set=())
        holder3 = Mock(spec_set=())
        container.append(holder1)
        container.place(3, holder2)
        container.place(6, holder3)
        self.assertEqual(len(container), 7)
        self.assertIs(container[0], holder1)
        self.assertIsNone(container[1])
        self.assertIsNone(container[2])
        self.assertIs(container[3], holder2)
        self.assertIsNone(container[4])
        self.assertIsNone(container[5])
        self.assertIs(container[6], holder3)
        fitCallsBefore = len(fitMock.mock_calls)
        container.remove(3)
        fitCallsAfter = len(fitMock.mock_calls)
        self.assertEqual(fitCallsAfter - fitCallsBefore, 1)
        self.assertEqual(fitMock.method_calls[-1], call._removeHolder(holder2))
        self.assertEqual(len(container), 6)
        self.assertIs(container[0], holder1)
        self.assertIsNone(container[1])
        self.assertIsNone(container[2])
        self.assertIsNone(container[3])
        self.assertIsNone(container[4])
        self.assertIs(container[5], holder3)
        fitCallsBefore = len(fitMock.mock_calls)
        container.remove(5)
        fitCallsAfter = len(fitMock.mock_calls)
        self.assertEqual(fitCallsAfter - fitCallsBefore, 1)
        self.assertEqual(fitMock.method_calls[-1], call._removeHolder(holder3))
        self.assertEqual(len(container), 1)
        self.assertIs(container[0], holder1)
        container.remove(holder1)
        self.assertObjectBuffersEmpty(container)

    def testIndexOutside(self):
        container = self.container
        fitMock = self.fitMock
        holder = Mock(spec_set=())
        container.append(holder)
        self.assertEqual(len(container), 1)
        self.assertIs(container[0], holder)
        fitCallsBefore = len(fitMock.mock_calls)
        self.assertRaises(IndexError, container.remove, 5)
        fitCallsAfter = len(fitMock.mock_calls)
        self.assertEqual(fitCallsAfter - fitCallsBefore, 0)
        self.assertEqual(len(container), 1)
        self.assertIs(container[0], holder)
        container.remove(holder)
        self.assertObjectBuffersEmpty(container)