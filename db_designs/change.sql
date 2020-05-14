ALTER TABLE NichtTextMedien MODIFY Typ ENUM('Video','Bild','Text');

INSERT INTO NichtTextMedien(Titel, Untertitel, Erscheinungsjahr, Kurzbeschreibung, SorteId, Typ) SELECT Titel, Untertitel, Erscheinungsjahr, Kurzbeschreibung, SorteId, "Text" FROM Buch;

ALTER TABLE Buch ADD COLUMN BuchId Integer(13) NOT NULL DEFAULT 0 FIRST;
UPDATE Buch LEFT JOIN NichtTextMedien ON NichtTextMedien.Titel = Buch.Titel AND NichtTextMedien.Untertitel = Buch.Untertitel AND NichtTextMedien.Kurzbeschreibung = Buch.Kurzbeschreibung AND NichtTextMedien.SorteId = Buch.SorteId AND NichtTextMedien.Erscheinungsjahr = Buch.Erscheinungsjahr SET Buch.BuchId=NichtTextMedien.NichtTextMedienId;
ALTER TABLE Buch ADD CONSTRAINT Buch_infk_1 FOREIGN KEY (BuchId) REFERENCES NichtTextMedien(NichtTextMedienId);
ALTER TABLE Buch DROP Titel;
ALTER TABLE Buch DROP Untertitel;
ALTER TABLE Buch DROP Erscheinungsjahr;
ALTER TABLE Buch DROP Kurzbeschreibung;
ALTER TABLE Buch DROP FOREIGN KEY Buch_ibfk_2;
ALTER TABLE Buch DROP SorteId;

ALTER TABLE Ebooks ADD COLUMN BuchId Integer(13) NOT NULL DEFAULT 0 AFTER ISBN;
UPDATE Ebooks LEFT JOIN Buch ON Buch.ISBN = Ebooks.BuchISBN SET Ebooks.BuchId=Buch.BuchId;
ALTER TABLE Ebooks ADD CONSTRAINT Ebooks_infk_1 FOREIGN KEY (BuchId) REFERENCES Buch(BuchId);
ALTER TABLE Ebooks DROP FOREIGN KEY Ebooks_ibfk_1;
ALTER TABLE Ebooks DROP BuchISBN;

ALTER TABLE Hoerbuch ADD COLUMN BuchId Integer(13) NOT NULL DEFAULT 0 AFTER ISBN;
UPDATE Hoerbuch LEFT JOIN Buch ON Buch.ISBN = Hoerbuch.BuchISBN SET Hoerbuch.BuchId=Buch.BuchId;
ALTER TABLE Hoerbuch ADD CONSTRAINT Hoerbuch_infk_1 FOREIGN KEY (BuchId) REFERENCES Buch(BuchId);
ALTER TABLE Hoerbuch DROP FOREIGN KEY Hoerbuch_ibfk_1;
ALTER TABLE Hoerbuch DROP BuchISBN;

ALTER TABLE AutorBuchZuord ADD COLUMN BuchId Integer(13) NOT NULL DEFAULT 0 AFTER ISBN;
UPDATE AutorBuchZuord LEFT JOIN Buch ON Buch.ISBN = AutorBuchZuord.ISBN SET AutorBuchZuord.BuchId=Buch.BuchId;
ALTER TABLE AutorBuchZuord DROP FOREIGN KEY AutorBuchZuord_ibfk_2;
ALTER TABLE AutorBuchZuord ADD CONSTRAINT AutorBuchZuord_ibfk_3 FOREIGN KEY (BuchId) REFERENCES Buch(BuchId);
ALTER TABLE AutorBuchZuord DROP ISBN;

ALTER TABLE Ausleihe CHANGE MediumId MediumIdOld VARCHAR(17) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL; 
ALTER TABLE Ausleihe ADD COLUMN MediumId Integer(13) NOT NULL DEFAULT 0 AFTER MediumIdOld;
UPDATE Ausleihe LEFT JOIN Buch ON Buch.ISBN = Ausleihe.MediumIdOld SET Ausleihe.MediumId=Buch.BuchId;
ALTER TABLE Ausleihe DROP FOREIGN KEY Ausleihe_ibfk_2;
ALTER TABLE Ausleihe DROP MediumIdOld;
ALTER TABLE Ausleihe ADD CONSTRAINT Ausleihe_ibfk_3 FOREIGN KEY (MediumId) REFERENCES NichtTextMedien(NichtTextMedienId);

ALTER TABLE MediumWortZuord CHANGE MediumId MediumIdOld VARCHAR(17) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL; 
ALTER TABLE MediumWortZuord ADD COLUMN MediumId Integer(13) NOT NULL DEFAULT 0 AFTER MediumIdOld;
UPDATE MediumWortZuord LEFT JOIN Buch ON Buch.ISBN = MediumWortZuord.MediumIdOld SET MediumWortZuord.MediumId=Buch.BuchId;
ALTER TABLE MediumWortZuord DROP FOREIGN KEY MediumWortZuord_ibfk_1;
ALTER TABLE MediumWortZuord DROP MediumIdOld;
ALTER TABLE MediumWortZuord ADD CONSTRAINT MediumWortZuord_ibfk_2 FOREIGN KEY (MediumId) REFERENCES NichtTextMedien(NichtTextMedienId);

ALTER TABLE NichtTextMedien CHANGE NichtTextMedienId MediumId INT(13) NOT NULL AUTO_INCREMENT; 
RENAME TABLE NichtTextMedien TO Medien;