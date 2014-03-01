-- LINUX version, longer watchdog delay. NEW PIC! starmani io 3.31, sisse progetud 3.28
PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE setup(register,value,ts,desc,comment,type integer); -- type vt chantypes. maarab kas loetav holding voi input registrist, bitikaaluga 8
-- desc jaab UI kaudu naha,  comment on enda jaoks. ts on muutmise aeg s, MIKS mitte mba, reg value? setup muutuja reg:value...
-- count oleks vaja lisada et korraga sygavuti saaks lugeda!

-- R... values will only be reported during channelconfiguration()
INSERT INTO 'setup' VALUES('R9.256','','','dev type','',0); -- read only
INSERT INTO 'setup' VALUES('R9.257','','','fw version','',0); -- start with this, W1.270,271,275 depend on this !
INSERT INTO 'setup' VALUES('R9.258','','','ser nr partii','',0); -- start with this, W1.270,271,275 depend on this !
INSERT INTO 'setup' VALUES('R9.259','','','ser nr plaat','',0); -- start with this, W1.270,271,275 depend on this !

-- INSERT INTO 'setup' VALUES('R2.53666','','','fw version','',0); -- vent1 serial MSB
-- INSERT INTO 'setup' VALUES('R3.53666','','','fw version','',0); -- vent2 serial MSB

INSERT INTO 'setup' VALUES('S400','http://www.itvilla.ee','','supporthost','for pull, push cmd',0);
INSERT INTO 'setup' VALUES('S401','upload.php','','requests.post','for push cmd',0);
INSERT INTO 'setup' VALUES('S402','Basic cHlhcHA6QkVMYXVwb2E=','','authorization header','for push cmd',0);
INSERT INTO 'setup' VALUES('S403','support/pyapp/$mac','','upload/dnload directory','for pull and push cmd',0); --  $mac will be replaced by wlan mac

INSERT INTO 'setup' VALUES('S51','0','','outer air loop kP','',0); -- P  VT OHK 
INSERT INTO 'setup' VALUES('S52','0','','outer air loop kI','',0); -- I
INSERT INTO 'setup' VALUES('S53','0','','outer air loop kD','',0); -- D
INSERT INTO 'setup' VALUES('S54','200','','outer air loop output lolim','',0); -- valjundi madalm piir (etteanne sp ohu jaoks)
INSERT INTO 'setup' VALUES('S55','350','','outer air loop output hilim','',0); -- valjundi korgem piir (etteanne sp ohu jaoks)

INSERT INTO 'setup' VALUES('S61','1','','inner air loop kP','',0); -- P  SP OHK  enne oli 0
INSERT INTO 'setup' VALUES('S62','0.01','','inner air loop kI','',0); -- I  enne oli 0.01ja 0,.005 / hirmus aeglane jargironimine...
INSERT INTO 'setup' VALUES('S63','100','','inner air loop kD','',0); -- D
INSERT INTO 'setup' VALUES('S64','170','','lolim','',0); -- valjundi madalm piir (etteanne kalorif vee jaoks)
INSERT INTO 'setup' VALUES('S65','700','','hilim','',0); -- valjundi korgem piir (etteanne kalorif vee jaoks)

INSERT INTO 'setup' VALUES('S81','0.1','','pump control loop kP','',0); -- P  pumbakiirus
INSERT INTO 'setup' VALUES('S82','0.025','','pump control loop kI','',0); -- I
INSERT INTO 'setup' VALUES('S83','10','','pump control loop kD','',0); -- D  oli 10
INSERT INTO 'setup' VALUES('S84','50','','lolim','',0); -- valjundi madalam piir (pumba min kiirus 25%)
INSERT INTO 'setup' VALUES('S85','200','','hilim','',0); -- valjundi korgem piir (pumba max kiirus 100%)


-- 3step params motortime = 130, maxpulse = 10, maxerror = 100, minpulse =1 , minerror = 1, runperiod = 20
INSERT INTO 'setup' VALUES('S71','2','','minpulse s','',0); -- alla 2 s pole motet
INSERT INTO 'setup' VALUES('S72','5','','maxpulse s','',0); -- yle 10 ka ehk ei tasu
INSERT INTO 'setup' VALUES('S73','240','','runperiod s','',0); -- kordus millise perioodiga - enne oli 60, aga liiga kiirelt reageeris. 120 ka liiga kiire. pulse 5s.
INSERT INTO 'setup' VALUES('S74','120','','motortime s','',0); -- aeg yhest servast teise kerimiseks
INSERT INTO 'setup' VALUES('S75','0.5','','minerror','',0); -- maarab tundetuse tsooni. symm molemas suunas.
INSERT INTO 'setup' VALUES('S76','2','','maxerror','',0); -- maarab tundlikkuse. sisendiks on aga pump_onlimie, max -1..+1!



INSERT INTO 'setup' VALUES('S200','225','','setpoint air in temp','ddeg',0); -- temp setpoint sissepuhkele, valjatommet ei suuda mojurtada vent. ddeg
INSERT INTO 'setup' VALUES('S220','100','','setpoint vent speed','prots',0); -- VENT KIIRUSe setpoint molemale 0..100%

INSERT INTO 'setup' VALUES('S512','starman','','location','',0);
INSERT INTO 'setup' VALUES('S514','0.0.0.0','','syslog server ip address','local broadcast in use if empty or 0.0.0.0 or 255.255.255.255',0); -- port is fixed to udp 514.

INSERT INTO 'setup' VALUES('W3.1','9','','8=stop, 9=run','wilo stratos',0); -- start pump1 in starman
INSERT INTO 'setup' VALUES('W4.1','9','','8=stop, 9=run','wilo',0); -- start pump2

INSERT INTO 'setup' VALUES('W9.270','48','','Vref','ai1..ai6, adi7..adi8',0); -- ref voltage 0000=5v, 4.096V jaoks 0030=48, 2.048V puhul 0020 (ONLY NEW PIC!)

-- INSERT INTO 'setup' VALUES('W1.271','192','','ANA mode ','ai1..ai6, adi7..adi8'); -- old pic (16f877), 2 oldest bits are di, the rest ai
INSERT INTO 'setup' VALUES('W9.271','0','','DI XOR 0000','inversioon',0); -- NEW PIC. DI inversion bitmap. 0=hi active, 1=low active

-- INSERT INTO 'setup' VALUES('W1.272','49152','','powerup mode','do on startup 0xC000'); -- do7 ja do8 up (commLED ja pwr_gsm)
INSERT INTO 'setup' VALUES('W9.272','0','','powerup mode','do on startup 0x0000',0); -- starmani jaoks koik releed off startimisel / EI MOIKA??

INSERT INTO 'setup' VALUES('W9.275','6162','','ANA bitmap','2 tk di',0); --  uus pic, 2 tk di  00011000 MBS

-- INSERT INTO 'setup' VALUES('W1.276','10','','usbreset powerup protection','10 s lisaaega',0); -- usbreset powerup protection
-- INSERT INTO 'setup' VALUES('W1.277','1380','','usbreset pulse','5 ja 100 s, 0x0564',0); -- usbreset 5 s pulse 100 s delay (ft31x+usb5v) / et sobiks ka linuxile 
-- INSERT INTO 'setup' VALUES('W1.278','10','','button powerup protection','10 s lisaaega',0); -- buttonpulse powerprotection
-- INSERT INTO 'setup' VALUES('W1.279','1380','','button pulse','100 ja 5 s',0); -- buttonpulse 100 s delay 5 s pulse , useless for linux

-- INSERT INTO 'setup' VALUES('W3.42','1','','pump fixed speed','ventkambris',0); -- wilo
-- INSERT INTO 'setup' VALUES('W4.42','1','','pump fixed speed','keldris',0); -- wilo


-- input registers 
INSERT INTO 'setup' VALUES('R1.53664','1','','vent1 ref voltage','20 mV unit',8); -- 
INSERT INTO 'setup' VALUES('R2.53664','1','','vent2 ref voltage','20 mV unit',8); -- 
INSERT INTO 'setup' VALUES('R1.53665','1','','vent1 ref current','2mA unit',8); -- 
INSERT INTO 'setup' VALUES('R2.53665','1','','vent2 ref current','2mA unit',8); -- 


CREATE UNIQUE INDEX reg_setup on 'setup'(register);
COMMIT;
