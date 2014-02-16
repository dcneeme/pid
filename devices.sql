-- devices attached to the modbusRTU or modbusTCP network
BEGIN TRANSACTION; 
-- count0..count3 are channel counts for do, do, ai an 1wire.

CREATE TABLE 'devices'(num integer,rtuaddr integer,tcpaddr,status integer,name,location,descr,count0 integer,count1 integer,count2 integer,count3 integer); -- ebables using mixed rtu and tcp inputs

INSERT INTO 'devices' VALUES(1,9,'',0,'DC6888','vent room','droid4control kontroller',8,8,8,8); -- # num 1 on alati master!!! webilehel esimene. starmanis 9!
-- INSERT INTO 'devices' VALUES(2,1,'',0,'vent1','vent room','modbus-juhtimisega ventilaator',8,8,8,8); -- 
-- INSERT INTO 'devices' VALUES(3,2,'',0,'vent1','vent room','modbus-juhtimisega ventilaator',8,8,8,8); -- 
INSERT INTO 'devices' VALUES(4,3,'',0,'pump1','vent room','modbus-juhtimisega pump',8,8,8,8); -- 
INSERT INTO 'devices' VALUES(5,4,'',0,'pump2','cellar','modbus-juhtimisega pump',8,8,8,8); -- 


-- di can be counter. ai can be di or do. subtype? only do (type=0) has subtype 0...
-- possible type.subtype combinations are 
-- 0.0,  1.1, 1.4,  2.0, 2.1, 2.2,  3.3
 
CREATE UNIQUE INDEX num_devices on 'devices'(num); -- device ordering numbers must be unique
CREATE UNIQUE INDEX addr_devices on 'devices'(rtuaddr,tcpaddr); -- device addresses must be unique

COMMIT;
    