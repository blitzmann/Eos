#===============================================================================
# Copyright (C) 2011 Diego Duclos
# Copyright (C) 2011-2015 Anton Vorobyov
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


from eos.const.eos import State, Domain, Scope, Operator
from eos.const.eve import EffectCategory
from eos.data.cache_object.modifier import Modifier
from eos.tests.attribute_calculator.attrcalc_testcase import AttrCalcTestCase
from eos.tests.attribute_calculator.environment import IndependentItem
from eos.tests.environment import Logger


class TestFilterUnknown(AttrCalcTestCase):
    """Test domain filter"""

    def setUp(self):
        AttrCalcTestCase.setUp(self)
        self.tgt_attr = tgt_attr = self.ch.attribute(attribute_id=1)
        self.src_attr = src_attr = self.ch.attribute(attribute_id=2)
        self.invalid_modifier = invalid_modifier = Modifier()
        invalid_modifier.state = State.offline
        invalid_modifier.scope = Scope.local
        invalid_modifier.src_attr = src_attr.id
        invalid_modifier.operator = Operator.post_percent
        invalid_modifier.tgt_attr = tgt_attr.id
        invalid_modifier.domain = Domain.self_
        invalid_modifier.filter_type = 26500
        invalid_modifier.filter_value = None
        self.effect = self.ch.effect(effect_id=1, category=EffectCategory.passive)

    def test_log(self):
        self.effect.modifiers = (self.invalid_modifier,)
        holder = IndependentItem(self.ch.type_(type_id=31, effects=(self.effect,),
                                               attributes={self.src_attr.id: 20, self.tgt_attr: 100}))
        self.fit.items.add(holder)
        self.assertEqual(len(self.log), 1)
        log_record = self.log[0]
        self.assertEqual(log_record.name, 'eos_test.attribute_calculator')
        self.assertEqual(log_record.levelno, Logger.WARNING)
        self.assertEqual(log_record.msg, 'malformed modifier on item 31: invalid filter type 26500')
        self.fit.items.remove(holder)
        self.assert_link_buffers_empty(self.fit)

    def test_combination(self):
        valid_modifier = Modifier()
        valid_modifier.state = State.offline
        valid_modifier.scope = Scope.local
        valid_modifier.src_attr = self.src_attr.id
        valid_modifier.operator = Operator.post_percent
        valid_modifier.tgt_attr = self.tgt_attr.id
        valid_modifier.domain = Domain.self_
        valid_modifier.filter_type = None
        valid_modifier.filter_value = None
        self.effect.modifiers = (self.invalid_modifier, valid_modifier)
        holder = IndependentItem(self.ch.type_(type_id=1, effects=(self.effect,),
                                               attributes={self.src_attr.id: 20, self.tgt_attr.id: 100}))
        self.fit.items.add(holder)
        # Invalid filter type in modifier should prevent proper processing of other modifiers
        self.assertNotAlmostEqual(holder.attributes[self.tgt_attr.id], 100)
        self.fit.items.remove(holder)
        self.assertEqual(len(self.log), 1)
        self.assert_link_buffers_empty(self.fit)
