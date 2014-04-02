-- gcal events into setup values. value - is default value, ends previos calendar-set event
PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE calendar(title,timestamp,value); --  all integers
-- insert all values from calendar if got anything. erase older ones somehow. 
CREATE INDEX ts_calendar on 'calendar'(timestamp);
COMMIT;
