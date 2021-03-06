from sc2 import UnitTypeId, Race

from sharpy.knowledges import KnowledgeBot
from sharpy.plans import BuildOrder, Step, StepBuildGas
from sharpy.plans.acts import *
from sharpy.plans.acts.terran import *
from sharpy.plans.require import *
from sharpy.plans.tactics import *
from sharpy.plans.tactics.terran import *


class OneBaseTurtle(KnowledgeBot):
    def __init__(self):

        super().__init__("One Base Turtle Defence")

    async def create_plan(self) -> BuildOrder:

        build_steps_buildings = [
            TerranUnit(UnitTypeId.SCV, 13),
            Step(RequiredSupply(13), GridBuilding(UnitTypeId.SUPPLYDEPOT, 1)),
            TerranUnit(UnitTypeId.SCV, 15),
            Step(RequiredUnitReady(UnitTypeId.SUPPLYDEPOT, 0.95), GridBuilding(UnitTypeId.BARRACKS, 1)),
            TerranUnit(UnitTypeId.SCV, 16),
            StepBuildGas(1),
            Step(RequiredSupply(16), GridBuilding(UnitTypeId.SUPPLYDEPOT, 2)),
            TerranUnit(UnitTypeId.SCV, 18),
            Step(None, MorphOrbitals(), skip_until=RequiredUnitReady(UnitTypeId.BARRACKS, 1)),
            Step(None, GridBuilding(UnitTypeId.FACTORY, 1), skip_until=RequiredUnitReady(UnitTypeId.BARRACKS, 1)),
            TerranUnit(UnitTypeId.SCV, 20),
            Step(RequiredSupply(20), GridBuilding(UnitTypeId.SUPPLYDEPOT, 3)),
            Step(None, GridBuilding(UnitTypeId.BUNKER, 1), skip_until=RequiredUnitReady(UnitTypeId.BARRACKS, 1)),
            StepBuildGas(2),
            Step(None, GridBuilding(UnitTypeId.FACTORY, 2)),
            TerranUnit(UnitTypeId.SCV, 22),
            Step(
                None,
                ActBuildAddon(UnitTypeId.FACTORYTECHLAB, UnitTypeId.FACTORY, 2),
                skip_until=RequiredUnitReady(UnitTypeId.FACTORY, 1),
            ),
            Step(RequiredSupply(28), GridBuilding(UnitTypeId.SUPPLYDEPOT, 4)),
            Step(None, GridBuilding(UnitTypeId.BARRACKS, 3)),
            Step(RequiredSupply(38), GridBuilding(UnitTypeId.SUPPLYDEPOT, 5)),
            AutoDepot(),
        ]

        build_step_tanks = [
            Step(RequiredUnitReady(UnitTypeId.FACTORYTECHLAB, 1), ActUnit(UnitTypeId.SIEGETANK, UnitTypeId.FACTORY, 20))
        ]

        build_steps_marines = [
            Step(RequiredUnitReady(UnitTypeId.BARRACKS, 1), ActUnit(UnitTypeId.MARINE, UnitTypeId.BARRACKS, 100)),
        ]

        build_order = BuildOrder([build_steps_buildings, build_step_tanks, build_steps_marines])

        attack = PlanZoneAttack(4)
        tactics = [
            PlanCancelBuilding(),
            ManTheBunkers(),
            LowerDepots(),
            PlanZoneDefense(),
            CallMule(),
            PlanDistributeWorkers(),
            Repair(),
            ContinueBuilding(),
            PlanZoneGatherTerran(),
            # once enough marines to guard the tanks, attack
            Step(RequiredUnitExists(UnitTypeId.MARINE, 18, include_killed=True), attack),
            PlanFinishEnemy(),
        ]
        return BuildOrder(build_order, tactics)


class LadderBot(OneBaseTurtle):
    @property
    def my_race(self):
        return Race.Terran
