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


from eos.tests.cache_generator.generator_testcase import GeneratorTestCase
from eos.tests.environment import Logger


class TestDefaultEffects(GeneratorTestCase):
    """
    Check that filtering out superfluous default effects
    occurs after data filtering, and that it occurs at all.
    """

    def setUp(self):
        GeneratorTestCase.setUp(self)
        self.item = {'typeID': 1, 'groupID': 1, 'typeName': ''}
        self.dh.data['invtypes'].append(self.item)
        self.eff_link1 = {'typeID': 1, 'effectID': 1}
        self.eff_link2 = {'typeID': 1, 'effectID': 2}
        self.dh.data['dgmtypeeffects'].append(self.eff_link1)
        self.dh.data['dgmtypeeffects'].append(self.eff_link2)
        self.dh.data['dgmeffects'].append({'effectID': 1, 'falloffAttributeID': 10})
        self.dh.data['dgmeffects'].append({'effectID': 2, 'falloffAttributeID': 20})

    def test_normal(self):
        self.eff_link1['isDefault'] = False
        self.eff_link2['isDefault'] = True
        data = self.run_generator()
        self.assertEqual(len(self.log), 2)
        literal_stats = self.log[0]
        self.assertEqual(literal_stats.name, 'eos_test.cache_generator')
        self.assertEqual(literal_stats.levelno, Logger.INFO)
        clean_stats = self.log[1]
        self.assertEqual(clean_stats.name, 'eos_test.cache_generator')
        self.assertEqual(clean_stats.levelno, Logger.INFO)
        self.assertIn(1, data['types'])
        self.assertEqual(len(data['effects']), 2)
        self.assertIn(2, data['effects'])
        self.assertEqual(data['effects'][2]['falloff_attribute'], 20)

    def test_duplicate(self):
        self.eff_link1['isDefault'] = True
        self.eff_link2['isDefault'] = True
        data = self.run_generator()
        self.assertEqual(len(self.log), 3)
        literal_stats = self.log[0]
        self.assertEqual(literal_stats.name, 'eos_test.cache_generator')
        self.assertEqual(literal_stats.levelno, Logger.INFO)
        clean_stats = self.log[1]
        self.assertEqual(clean_stats.name, 'eos_test.cache_generator')
        self.assertEqual(clean_stats.levelno, Logger.INFO)
        log_record = self.log[2]
        self.assertEqual(log_record.name, 'eos_test.cache_generator')
        self.assertEqual(log_record.levelno, Logger.WARNING)
        self.assertEqual(
            log_record.msg,
            'data contains 1 excessive default effects, marking them as non-default'
        )
        self.assertEqual(len(data['types']), 1)
        self.assertIn(1, data['types'])
        # Make sure effects are not removed
        self.assertEqual(len(data['effects']), 2)
        self.assertIn(1, data['effects'])
        self.assertIn(2, data['effects'])
        self.assertEqual(data['effects'][1]['falloff_attribute'], 10)

    def test_cleanup(self):
        del self.item['groupID']
        self.eff_link1['isDefault'] = True
        self.eff_link2['isDefault'] = True
        data = self.run_generator()
        self.assertEqual(len(self.log), 2)
        literal_stats = self.log[0]
        self.assertEqual(literal_stats.name, 'eos_test.cache_generator')
        self.assertEqual(literal_stats.levelno, Logger.INFO)
        clean_stats = self.log[1]
        self.assertEqual(clean_stats.name, 'eos_test.cache_generator')
        self.assertEqual(clean_stats.levelno, Logger.INFO)
        self.assertEqual(len(data['types']), 0)
        self.assertEqual(len(data['effects']), 0)
