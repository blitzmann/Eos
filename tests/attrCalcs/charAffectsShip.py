#===============================================================================
# Copyright (C) 2011 Diego Duclos
# Copyright (C) 2011-2012 Anton Vorobyov
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


from unittest import TestCase

from eos.eve.attribute import Attribute
from eos.eve.invType import InvType
from eos.eve.effect import Effect
from eos.calc.info.info import Info, InfoRunTime, InfoLocation, InfoOperator, InfoSourceType
from eos.fit.fit import Fit
from eos.fit.ship import Ship
from eos.fit.character import Character


class TestCharAffectsShip(TestCase):

    def testAttrCalc(self):

        def attrMetaGetter(attrId):
            attrs = {1: Attribute(1, highIsGood=1, stackable=1),
                     2: Attribute(2, highIsGood=1, stackable=1)}
            return attrs[attrId]

        attrShip = attrMetaGetter(1)
        attrChar = attrMetaGetter(2)

        fit = Fit(attrMetaGetter)

        ship1 = Ship(InvType(1, attributes={attrShip.id: 100}))
        ship2 = Ship(InvType(2, attributes={attrShip.id: 20}))

        info = Info()
        info.runTime = InfoRunTime.duration
        info.location = InfoLocation.ship
        info.operator = InfoOperator.postPercent
        info.targetAttribute = attrShip.id
        info.sourceType = InfoSourceType.attribute
        info.sourceValue = attrChar.id
        modEffect = Effect(1)
        modEffect._Effect__infos = {info}
        char = Character(InvType(3, effects={modEffect}, attributes={attrChar.id: 40}))
        fit.character = char

        fit.ship = ship1
        expVal = 140
        self.assertAlmostEqual(ship1.attributes[attrShip.id], expVal)

        # Then, check if after removal of modifier it's disabled properly,
        # to become enabled once again for other charge
        fit.ship = ship2
        expVal = 28
        self.assertAlmostEqual(ship2.attributes[attrShip.id], expVal)