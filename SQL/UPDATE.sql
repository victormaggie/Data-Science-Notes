-- INSERT DELETE, UPDATE data

INSERT INTO ATTENDEE (FIRST_NAME, LAST_NAME)
VALUES ('Thomas', 'Nleld');


-- Multiple inserts

INSERT INTO ATTENDEE (FIRST_NAME, LAST_NAME, PHONE, EMAIL, VIP)
VALUES
('Jon', 'Skeeter', 4802185842, 'John.skeeter@rex.net', 1),
('Sam','Scala',2156783401,'sam.scala@gmail.com', 0), 
('Brittany','Fisher',5932857296,'brittany.fisher@outlook.com', 0)

-- DELETE the format

DELETE FROM ATTENDEE
WHERE PHONE IS NULL
AND EMAIL IS NULL;


-- TRUCATE THE TABLE
TRUCATE TABLE ATTENDEE


-- UPDATE FUNCTION
UPDATE ATTENDEE SET EMAIL=UPPER(EMAIL)


UPDATE ATTENDEE SET FIRST_NAME = UPPER(FIRST_NAME),
LAST_NAME = UPPER(LAST_NAME);

SELECT * FROM ATTENDEE

-- DROP TABLE
DROP TABLE JERRY

