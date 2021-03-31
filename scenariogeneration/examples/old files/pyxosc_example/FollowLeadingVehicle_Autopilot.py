import pyoscx   

### create catalogs
catalog = pyoscx.Catalog()
catalog.add_catalog("ManeuverCatalog", "catalogs")

### create road
road = pyoscx.RoadNetwork(roadfile='Town04',scenegraph=" ")


### create parameters
paramdec = pyoscx.ParameterDeclarations()

paramdec.add_parameter(pyoscx.Parameter('leadingSpeed',pyoscx.ParameterType.double,'4.0'))
###create properties

prop= pyoscx.Properties()
#prop.add_property


### create vehicles

bb = pyoscx.BoundingBox(2,5,1.8,2.0,0,0.9)
fa = pyoscx.Axle(0.523598775598,0.8,1.68,2.98,0.4)
ba = pyoscx.Axle(0.523598775598,0.8,1.68,0,0.4)
ego_veh = pyoscx.Vehicle('vehicle.tesla.model3',pyoscx.VehicleCategory.car,bb,fa,ba,69,10,10)
ego_veh.add_property(name='type',value='ego_vehicle')
ego_veh.add_property(name='color',value='255,69,0')
bb = pyoscx.BoundingBox(1.8,4.5,1.5,1.3,0,0.8)
fa = pyoscx.Axle(0.523598775598,0.8,1.68,2.98,0.4)
ba = pyoscx.Axle(0.523598775598,0.8,1.68,0,0.4)
other_veh = pyoscx.Vehicle('vehicle.tesla.model3',pyoscx.VehicleCategory.car,bb,fa,ba,69,10,10)
other_veh.add_property(name='type',value='simulation')

## create entities

egoname = 'hero'
targetname = 'adversary'

entities = pyoscx.Entities()

entities.add_scenario_object(egoname,ego_veh)

entities.add_scenario_object(targetname,other_veh)


timeofday=pyoscx.TimeOfDay(True,2020,12,11,21,52,10)
roadcond=pyoscx.RoadCondition(1.0)
weather=pyoscx.Weather(pyoscx.CloudState.free,1,0,1,pyoscx.PrecipitationType.dry,0,100000)
env=pyoscx.Environment("Environment1", timeofday,weather,roadcond)


### create init
init = pyoscx.Init()

#environment
timeofday=pyoscx.TimeOfDay(True,2020,12,11,11,52,10)
roadcond=pyoscx.RoadCondition(1.0)
weather=pyoscx.Weather(pyoscx.CloudState.free,1,0,1,pyoscx.PrecipitationType.dry,0,100000)
env=pyoscx.Environment("Environment1",timeofday,weather,roadcond)
envAct= pyoscx.EnvironmentAction("Environment1", env)

#controller
#prop= pyoscx.Properties()
#prop.add_property(name='module',value='external_control')
#contr = pyoscx.Controller('HeroAgent',prop)
#controllerAct = pyoscx.AssignControllerAction(contr)

#step_time = pyoscx.TransitionDynamics(pyoscx.DynamicsShapes.step,pyoscx.DynamicsDimension.time,1)

#targetspeed = pyoscx.AbsoluteSpeedAction(15,step_time)
targetstart = pyoscx.TeleportAction(pyoscx.WorldPosition(-8.6,30,0.5,4.7))
#targetstart = pyoscx.TeleportAction(pyoscx.WorldPosition(190,133,0.5,0))

#egostart = pyoscx.TeleportAction(pyoscx.WorldPosition(-9.4,-152.8,0.5,1.57079632679))
egostart = pyoscx.TeleportAction(pyoscx.WorldPosition(-8.6,60,0.5,4.7))
#egospeed = pyoscx.AbsoluteSpeedAction(15,pyoscx.TransitionDynamics(pyoscx.DynamicsShapes.step,pyoscx.DynamicsDimension.distance,10))


init.add_global_action(envAct)
#init.add_init_action(egoname,egospeed)
init.add_init_action(egoname,egostart)
#init.add_init_action(egoname,controllerAct)
#init.add_init_action(targetname,targetspeed)
init.add_init_action(targetname,targetstart)


### create an event

#autopilot
ap_starttrigger = pyoscx.ValueTrigger('StartCondition',1,pyoscx.ConditionEdge.rising,pyoscx.SimulationTimeCondition(0,pyoscx.Rule.greaterThan))
ap_eventstart = pyoscx.Event('StartAutopilot',pyoscx.Priority.overwrite)
ap_eventstart.add_trigger(ap_starttrigger)
ap_actionstart = pyoscx.ActivateControllerAction(True,True)
ap_eventstart.add_action('StartAutopilot',ap_actionstart)


stoptrigcond = pyoscx.TraveledDistanceCondition(200.0)
ap2_stoptrigger = pyoscx.EntityTrigger('EndCondition',1,pyoscx.ConditionEdge.rising,stoptrigcond,egoname)

ap_stoptrigger = pyoscx.ValueTrigger('StopCondition',1,pyoscx.ConditionEdge.rising,pyoscx.SimulationTimeCondition(30,pyoscx.Rule.greaterThan))
ap_eventstop = pyoscx.Event('StopAutopilot',pyoscx.Priority.overwrite)
ap_eventstop.add_trigger(ap_stoptrigger)
ap_actionstop = pyoscx.ActivateControllerAction(False,False)
ap_eventstop.add_action('StopAutopilot',ap_actionstop)


## create the maneuvers
#maneuver for hero 
h_man = pyoscx.Maneuver('AutopilotSequenceHero')
h_man.add_event(ap_eventstart)
h_man.add_event(ap_eventstop)

h_mangr = pyoscx.ManeuverGroup('AutopilotSequenceHero')
h_mangr.add_actor('hero')
h_mangr.add_maneuver(h_man)

#maneuver for adversary
a_man = pyoscx.Maneuver('AutopilotSequenceAdversary')
a_man.add_event(ap_eventstart)
a_man.add_event(ap_eventstop)

a_mangr = pyoscx.ManeuverGroup('AutopilotSequenceAdversary')
a_mangr.add_actor('adversary')
a_mangr.add_maneuver(a_man)


act_starttrigger = pyoscx.ValueTrigger('starttrigger',0,pyoscx.ConditionEdge.rising,pyoscx.SimulationTimeCondition(0,pyoscx.Rule.greaterThan))
stoptrigcond = pyoscx.TraveledDistanceCondition(200.0)
act_stoptrigger = pyoscx.EntityTrigger('EndCondition',0,pyoscx.ConditionEdge.rising,stoptrigcond,egoname, triggeringpoint='stop')
act = pyoscx.Act('my_act',act_starttrigger,act_stoptrigger)
act.add_maneuver_group(h_mangr)
act.add_maneuver_group(a_mangr)

# create the story
story = pyoscx.Story('mystory')
story.add_act(act)

## create the storyboard
sb = pyoscx.StoryBoard(init)
sb.add_story(story)

## create the scenario
sce = pyoscx.Scenario('follow_leading_vehicle','Bonora_Motta',paramdec,entities=entities,storyboard = sb,roadnetwork=road,catalog=catalog)

# display the scenario
pyoscx.prettyprint(sce.get_element())

# if you want to save it
sce.write_xml('FollowLeadingVehicle.xosc',True)




