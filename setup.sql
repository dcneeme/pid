-- LINUX version, longer watchdog delay. NEW PIC!
PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE setup(register,value,ts,desc,comment); -- desc jaab UI kaudu naha,  comment on enda jaoks. ts on muutmise aeg s, MIKS mitte mba, reg value? setup muutuja reg:value...
-- count oleks vaja lisada et korraga sygavuti saaks lugeda!

-- R... values will only be reported during channelconfiguration()
INSERT INTO 'setup' VALUES('R9.256','','','dev type',''); -- read only
INSERT INTO 'setup' VALUES('R9.257','','','fw version',''); -- start with this, W1.270,271,275 depend on this !

INSERT INTO 'setup' VALUES('R2.5366','','','fw version',''); -- vent1 serial
INSERT INTO 'setup' VALUES('R3.5366','','','fw version',''); -- vent1 serial

INSERT INTO 'setup' VALUES('S400','http://www.itvilla.ee','','supporthost','for pull, push cmd');
INSERT INTO 'setup' VALUES('S401','upload.php','','requests.post','for push cmd');
INSERT INTO 'setup' VALUES('S402','Basic cHlhcHA6QkVMYXVwb2E=','','authorization header','for push cmd');
INSERT INTO 'setup' VALUES('S403','support/pyapp/$mac','','upload/dnload directory','for pull and push cmd'); --  $mac will be replaced by wlan mac

INSERT INTO 'setup' VALUES('S51','0','','outer air loop kP',''); -- P  VT OHK 
INSERT INTO 'setup' VALUES('S52','0.03','','outer air loop kI',''); -- I
INSERT INTO 'setup' VALUES('S53','0','','outer air loop kD',''); -- D
INSERT INTO 'setup' VALUES('S54','200','','outer air loop output lolim',''); -- valjundi madalm piir (etteanne sp ohu jaoks)
INSERT INTO 'setup' VALUES('S55','350','','outer air loop output hilim',''); -- valjundi korgem piir (etteanne sp ohu jaoks)

INSERT INTO 'setup' VALUES('S61','0','','inner air loop kP',''); -- P  SP OHK 
INSERT INTO 'setup' VALUES('S62','0.01','','innner air loop kI',''); -- I
INSERT INTO 'setup' VALUES('S63','100','','inner air loop kD',''); -- D
INSERT INTO 'setup' VALUES('S64','180','','lolim',''); -- valjundi madalm piir (etteanne kalorif vee jaoks)
INSERT INTO 'setup' VALUES('S65','700','','hilim',''); -- valjundi korgem piir (etteanne kalorif vee jaoks)

-- 3step params motortime = 130, maxpulse = 10, maxerror = 100, minpulse =1 , minerror = 1, runperiod = 20
INSERT INTO 'setup' VALUES('S71','2','','minpulse s',''); -- alla 2 s pole motet
INSERT INTO 'setup' VALUES('S72','10','','maxpulse s',''); -- yle 10 ka ehk ei tasu
INSERT INTO 'setup' VALUES('S73','60','','runperiod s',''); -- kordus millise perioodiga 
INSERT INTO 'setup' VALUES('S74','120','','motortime s',''); -- aeg yhest servast teise kerimiseks
INSERT INTO 'setup' VALUES('S75','30','','minerror',''); -- maarab tundetuse tsooni. symm molemas suunas.
INSERT INTO 'setup' VALUES('S76','200','','maxerror',''); -- maarab tundlikkuse



INSERT INTO 'setup' VALUES('S200','245','','setpoint air out temp','ddeg'); -- temp setpoint valjatombele. ddeg

INSERT INTO 'setup' VALUES('S512','starman','','location','');
INSERT INTO 'setup' VALUES('S514','0.0.0.0','','syslog server ip address','local broadcast in use if empty or 0.0.0.0 or 255.255.255.255'); -- port is fixed to udp 514.

INSERT INTO 'setup' VALUES('W3.1','9','','8=stop, 9=run','wilo stratos'); -- start pump1 in starman
INSERT INTO 'setup' VALUES('W4.1','9','','8=stop, 9=run','wilo'); -- start pump2

INSERT INTO 'setup' VALUES('W9.270','48','','Vref','ai1..ai6, adi7..adi8'); -- ref voltage 0000=5v, 4.096V jaoks 0030=48, 2.048V puhul 0020 (ONLY NEW PIC!)

-- INSERT INTO 'setup' VALUES('W1.271','192','','ANA mode ','ai1..ai6, adi7..adi8'); -- old pic (16f877), 2 oldest bits are di, the rest ai
INSERT INTO 'setup' VALUES('W9.271','0','','DI XOR 0000','inversioon'); -- NEW PIC. DI inversion bitmap. 0=hi active, 1=low active

-- INSERT INTO 'setup' VALUES('W1.272','49152','','powerup mode','do on startup 0xC000'); -- do7 ja do8 up (commLED ja pwr_gsm)
INSERT INTO 'setup' VALUES('W9.272','0','','powerup mode','do on startup 0x0000'); -- starmani jaoks koik releed off startimisel / EI MOIKA??

INSERT INTO 'setup' VALUES('W9.275','0','','ANA direction','kogu ANA on sis'); --  old pic, all inputs
-- INSERT INTO 'setup' VALUES('W1.275','49152','','ANA mode + direction c000','kogu ANA on sis'); --  NEW pic, ANA port+mode bitmap, LSB: 1=output, 0=input. MSB: AI/DI, 0=AI

-- INSERT INTO 'setup' VALUES('W1.276','10','','usbreset powerup protection','10 s lisaaega'); -- usbreset powerup protection
-- INSERT INTO 'setup' VALUES('W1.277','1380','','usbreset pulse','5 ja 100 s, 0x0564'); -- usbreset 5 s pulse 100 s delay (ft31x+usb5v) / et sobiks ka linuxile 
-- INSERT INTO 'setup' VALUES('W1.278','10','','button powerup protection','10 s lisaaega'); -- buttonpulse powerprotection
-- INSERT INTO 'setup' VALUES('W1.279','1380','','button pulse','100 ja 5 s'); -- buttonpulse 100 s delay 5 s pulse , useless for linux

-- INSERT INTO 'setup' VALUES('W3.42','1','','pump fixed speed','ventkambris'); -- wilo
-- INSERT INTO 'setup' VALUES('W4.42','1','','pump fixed speed','keldris'); -- wilo


-- INSERT INTO 'setup' VALUES('W1.402','255','','ao test','ao test'); -- ao test setp kaudu, saada uus vaartus ja kehtestub

-- lisada supportserver ja mon server aadressid

CREATE UNIQUE INDEX reg_setup on 'setup'(register);
COMMIT;
