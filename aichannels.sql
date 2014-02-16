-- starmani jaoks

-- analogue values and temperatures channel definitions for android-based automation controller 
-- x1 ja x2 for input range, y1 y2 for output range. conversion based on 2 points x1,y1 and y1,y2. x=raw, y=value.
-- avg defines averaging strength, has effect starting from 2

-- # CONFIGURATION BITS
-- # siin ei ole tegemist ind ja grp teenuste eristamisega, ind teenused konfitakse samadel alustel eraldi!
-- # konfime poolbaidi vaartustega, siis hex kujul hea vaadata. vanem hi, noorem lo!
-- # x0 - alla outlo ikka ok, 0x - yle outhi ikka ok 
-- # x1 - alla outlo warning, 1x - yle outhi warning
-- # x2 - alla outlo critical, 2x - yle outhi critical
-- # x3 - alla outlo ei saada, 3x - yle outhi ei saada, status 3?
-- hex 21 = dec 33, hex 12 = dec 18 - aga ei muuda statust???
-- # lisaks bit 2 lisamine asendab vaartuse nulliga / kas on vaja?
-- # lisaks bit 4 teeb veel midagi / reserv

-- x1 x2 y1 y2 values needed also for virtual setup values, where no linear conversions is needed. use 0 100 0 100 not to convert

PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
-- drop table aichannels; -- remove the old one

CREATE TABLE aichannels(mba,regadd,val_reg,member,cfg,x1,x2,y1,y2,outlo,outhi,avg,block,raw,value,status,ts,desc,comment,type integer); 
-- type is for category flagging, 0=do, 1 = di, 2=ai, 3=ti. use only 2 and 3 in this table (4=humidity, 5=co2?)

INSERT INTO "aichannels" VALUES('9','8','Q1W','1','18','4','4095','0','100','10','70','1','','','110','0','','humidity ai7','0..10V 0..100%',3); -- vt niiskus 0..100, lo hi 10 70%
INSERT INTO "aichannels" VALUES('9','2','Q1W','2','18','4','4095','0','100','0','10','1','','','110','0','','co2 ai1','0..10V 0..100%',3); -- vt saastatus 0..100%, lo hi 0-  10%

-- INSERT INTO "aichannels" VALUES('9','605','T5W','1','18','0','80','0','50','100','300','3','','','110','0','','kalorif tagastuv','28AC849C04000086',3); -- VT tegelik, 1w / 0..10 andurilt
INSERT INTO "aichannels" VALUES('9','9','T5W','1','18','0','2413','0','239','100','300','3','','','110','0','','kalorif tagastuv','28AC849C04000086',3); -- VT tegelik, 1w / 0..10 andurilt
INSERT INTO "aichannels" VALUES('','','T5W','2','0','0','100','0','100','0','','1','','','110','0','','temp channel 2','ai7 voltage',3); -- VT setpoint
INSERT INTO "aichannels" VALUES('','','T5W','3','0','0','100','0','100','0','','1','','0','150','0','','temp channel 1','lo limit',3); -- VT lo alarm
INSERT INTO "aichannels" VALUES('','','T5W','4','0','0','100','0','100','0','','1','','0','300','0','','temp channel 1','hi limit',3); -- VT hi alarm

INSERT INTO "aichannels" VALUES('9','602','T6W','1','33','0','80','0','50','150','300','3','','','110','0','','temp SP','28FAAE98040000D9',3); -- SP tegelik, 1 wire d9
INSERT INTO "aichannels" VALUES('','','T6W','2','0','0','100','0','100','0','','1','','0','110','0','','temp channel 2','ai7 voltage',3); -- SP setpoint
INSERT INTO "aichannels" VALUES('','','T6W','3','0','0','100','0','100','0','','1','','0','180','0','','temp channel 1','lo limit',3); -- VT lo limit, arvesta get_ai()[] kaudu
INSERT INTO "aichannels" VALUES('','','T6W','4','0','0','100','0','100','0','','1','','0','300','0','','temp channel 1','hi limit',3); -- VT hi limit

INSERT INTO "aichannels" VALUES('9','600','T7W','1','33','0','80','0','50','150','600','3','','','110','0','','temp vesi','28E0F59B040000A8',3); -- kalorif sisse, 1 wire 
INSERT INTO "aichannels" VALUES('','','T7W','2','0','0','100','0','100','0','','1','','','110','0','','temp channel 2','ai7 voltage',3); -- kalorif setpoint
INSERT INTO "aichannels" VALUES('','','T7W','3','0','0','100','0','100','0','','1','','0','150','0','','temp channel 1','lo limit',3); -- kalorif lo alarm
INSERT INTO "aichannels" VALUES('','','T7W','4','0','0','100','0','100','0','','1','','0','600','0','','temp channel 1','hi limit',3); -- kalorif hi alarm
-- 

-- jargmine on abiteenus sp jarelkytte pid/juhtimise jalgimiseks
INSERT INTO "aichannels" VALUES('9','9','T8W','1','18','4','2413','0','239','150','300','3','','','110','0','','temp VT 1..50 deg 0..10V','ai7 voltage',3); -- VT tegelik, kalibr 1p
INSERT INTO "aichannels" VALUES('','','T8W','2','0','0','100','0','100','0','','1','','','110','0','','temp channel 2','ai7 voltage',3); -- VT setpoint
INSERT INTO "aichannels" VALUES('','','T8W','3','0','0','100','0','100','0','','1','','0','110','0','','temp channel 2','ai7 voltage',3); -- SP setpoint
INSERT INTO "aichannels" VALUES('','','T8W','4','0','0','100','0','100','0','','1','','','110','0','','temp channel 2','ai7 voltage',3); -- kalorif setpoint 1
INSERT INTO "aichannels" VALUES('','','T8W','5','0','0','100','0','100','0','','1','','','110','0','','temp channel 2','ai7 voltage',3); -- kalorif setpoint 2

INSERT INTO "aichannels" VALUES('9','7','TAW','1','17','2344','2654','326','483','50','700','1','','','110','0','','kalorif 1 k andur','',3); -- 1k termoandur kalorifeeris
INSERT INTO "aichannels" VALUES('9','601','TAW','2','17','0','80','0','50','0','500','1','','','110','0','','kalorif tagasi 1w andur','28AC849C04000086',3); -- 1w termoandur kalorifeer tagasi
INSERT INTO "aichannels" VALUES('','','TAW','3','0','0','100','0','100','0','0','3','','','50','0','','kalorif 1 k andur','lolim',3); -- kylmumise alarm


-- talv/suvi ajami liikumise aeg molemas suunas 142 s

-- soojusvaheti -- 
INSERT INTO "aichannels" VALUES('9','604','T9W','1','17','0','80','0','50','50','300','3','','','110','0','','temp sissepuhe enne kalorif','2805920400002A',3); -- 
INSERT INTO "aichannels" VALUES('9','606','T9W','2','17','0','80','0','50','50','350','1','','','110','0','','temp valjapuhe','28AB559B04000016',3); -- ds18b20 sensor
INSERT INTO "aichannels" VALUES('9','603','T9W','3','17','0','80','0','50','-400','400','1','','','110','0','','temp sissetommme','286E199C0400002C',3); -- ds18b20 sensor
INSERT INTO "aichannels" VALUES('9','605','T9W','4','17','0','80','0','50','150','300','3','','','110','0','','temp valjatomme','28d5a59B0400003B',3); -- tc1047 sensor

INSERT INTO "aichannels" VALUES('3','1','P1W','1','17','0','200','0','100','0','100','1','','','110','0','','pump1','ao',2); -- pump speed 0..100, controlled via aochannels
INSERT INTO "aichannels" VALUES('4','1','P1W','2','17','0','200','0','100','0','100','1','','','110','0','','pump 2','ao',2); -- pump speed, controlled via aochannels
INSERT INTO "aichannels" VALUES('','','P1W','3','0','0','100','0','100','0','10','1','','','10','0','','lo warning','ao',2); -- 10%
INSERT INTO "aichannels" VALUES('','','P1W','4','0','0','100','0','100','0','95','1','','','95','0','','hi warning','ao',2); -- 95%

INSERT INTO "aichannels" VALUES('','','V1W','1','17','0','120','0','100','-90','90','1','','','110','0','','pump1','ao',2); -- valve pos cumul runtime (tegelik 120 max)
INSERT INTO "aichannels" VALUES('','','V1W','2','0','0','100','0','100','0','100','1','','','-100','0','','pump 2','ao',2); -- min
INSERT INTO "aichannels" VALUES('','','V1W','3','0','0','100','0','100','0','10','1','','','100','0','','lo warning','ao',2); -- max joon

INSERT INTO "aichannels" VALUES('1','','V2W','1','17','0','100','0','100','-90','90','1','','','100','0','','vent1 speed','ao',2); -- vent 1 0..100
INSERT INTO "aichannels" VALUES('2','','V2W','2','17','0','100','0','100','0','100','1','','','100','0','','vent2 speed','ao',2); -- vent2 0..100
INSERT INTO "aichannels" VALUES('','','V2W','3','0','0','100','0','100','0','10','1','','','20','0','','lo warning','ao',2); -- min joon, hoiatuseks?

-- lisa siia torustiku rohk reg 2 ja pumpade voolud reg 4 ning 5

CREATE UNIQUE INDEX ai_regmember on 'aichannels'(val_reg,member); -- every service member only once
COMMIT;
