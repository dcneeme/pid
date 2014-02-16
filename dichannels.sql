-- starman_vent

-- modbus di and do channels for android based automation controller with possible extension modules
-- if output channels should ne reported to monitoring, they must be defined here in addition to dochannels
-- member 1..n defines multivalue service content. mixed input and output channels in one service are also possible!
-- status and dsc are last known results, see timestamp ts as well when using
-- also power counting may be involved, see cfg 

-- CONF BITS
-- # 1 - value 1 = warningu (values can be 0 or 1 only)
-- # 2 - value 1 = critical, 
-- # 4 - value inversion 
-- # 8 - value to status inversion
-- # 16 - immediate notification on value change (whole multivcalue service will be (re)reported)
-- # 32 - this channel is actually a writable coil output, not a bit from the register (takes value 0000 or FF00 as value to be written, function code 05 instead of 06!)
--     when reading coil, the output will be in the lowest bit, so 0 is correct as bit value

-- # block sending. 1 = read, but no notifications to server. 2=do not even read, temporarely register down or something...

PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;

CREATE TABLE dichannels(mba,regadd,bit,val_reg,member,cfg,block,value,status,ts_chg,chg,desc,comment,ts_msg,type integer); -- ts_chg is update toime (happens on change only), ts_msg =notif
-- value is bit value 0 or 1, to become a member value with or without inversion
-- status values can be 0..3, depending on cfg. member values to service value via OR (bigger value wins)
-- type is for category flagging, 0=do, 1 = di, 2=ai, 3=ti. use only 0 and 1 in this table

-- input channels
-- INSERT INTO "dichannels" VALUES('9','1','14','D1W','1','0','0','0','1','0','','','DI7','',1); -- en mootja, vt counters

INSERT INTO "dichannels" VALUES('9','1','8','FAS','1','2','0','0','1','1','','','DI1','',1); -- tulesignaal
INSERT INTO "dichannels" VALUES('9','1','9','D1W','1','18','0','0','1','1','','','DI2','',1); -- niisuti kaitse
INSERT INTO "dichannels" VALUES('9','1','10','D1W','2','17','0','0','1','1','','','DI3','',1); -- niisuti too
-- INSERT INTO "dichannels" VALUES('9','1','11','D3W','8','0','0','0','1','1','','','DI4','',1); -- RESERV voi vent kontaktor?
INSERT INTO "dichannels" VALUES('9','1','12','D2W','1','18','0','0','1','1','','','DI5','',1); -- jahuti kaitse
INSERT INTO "dichannels" VALUES('9','1','13','D2W','2','17','0','0','1','1','','','DI6','',1); -- jahuti kompressori too
-- INSERT INTO "dichannels" VALUES('9','1','14','D4W','1','0','0','0','1','1','','','DI7','',1); -- energiamootur 3f, vt counters
INSERT INTO "dichannels" VALUES('9','1','15','PWS','1','0','0','0','1','1','','','DI8','',1); -- faasiviga

-- controlled outputs, following dochannels bit values
INSERT INTO "dichannels" VALUES('9','0','8','K1W','1','17','0','0','1','0','','','D01','',0); -- niisutus
INSERT INTO "dichannels" VALUES('9','0','9','K1W','2','17','0','0','1','0','','','D02','',0); -- jahutus

INSERT INTO "dichannels" VALUES('9','0','10','K2W','1','17','0','0','1','0','','','D03','',0); -- 3tee ventiili ajam up
INSERT INTO "dichannels" VALUES('9','0','11','K2W','2','17','0','0','1','1','','','DO4','',0); -- 3tee ventiili ajam dn

INSERT INTO "dichannels" VALUES('9','0','12','K3W','1','17','0','0','1','0','','','D05','',0); -- moodaviigu 3step ajam up
INSERT INTO "dichannels" VALUES('9','0','13','K3W','2','17','0','0','1','1','','','DO6','',0); -- moodaviigu 3step ajam dn

INSERT INTO "dichannels" VALUES('9','0','14','K4W','1','0','0','0','1','0','','','D07','',0); -- roheline lamp
INSERT INTO "dichannels" VALUES('9','0','15','K4W','2','0','0','0','1','1','','','DO8','',0); -- punane lamp

CREATE UNIQUE INDEX di_regmember on 'dichannels'(val_reg,member);
-- NB bits and registers are not necessarily unique!

COMMIT;
