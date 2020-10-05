ALTER TABLE NichtTextMedium MODIFY Typ ENUM('Video','Bild','Text');

INSERT INTO NichtTextMedium(Titel, Untertitel, Erscheinungsjahr, Kurzbeschreibung, SorteId, Typ) SELECT Titel, Untertitel, Erscheinungsjahr, Kurzbeschreibung, SorteId, "Text" FROM Buch;

ALTER TABLE Buch ADD COLUMN BuchId Integer(13) NOT NULL DEFAULT 0 FIRST;

UPDATE Buch LEFT JOIN NichtTextMedium ON NichtTextMedium.Titel = Buch.Titel 
	AND (NichtTextMedium.Untertitel = Buch.Untertitel OR NichtTextMedium.Untertitel IS NULL OR Buch.Untertitel IS NULL)
    AND (NichtTextMedium.Kurzbeschreibung = Buch.Kurzbeschreibung OR NichtTextMedium.Kurzbeschreibung IS NULL OR Buch.Kurzbeschreibung IS NULL)
    AND (NichtTextMedium.SorteId = Buch.SorteId OR NichtTextMedium.SorteId IS NULL OR Buch.SorteId IS NULL)
    AND (NichtTextMedium.Erscheinungsjahr = Buch.Erscheinungsjahr OR NichtTextMedium.Erscheinungsjahr IS NULL OR Buch.Erscheinungsjahr IS NULL)
    SET Buch.BuchId=NichtTextMedium.NichtTextMediumId;

ALTER TABLE Buch ADD CONSTRAINT Buch_infk_1 FOREIGN KEY (BuchId) REFERENCES NichtTextMedium(NichtTextMediumId);
ALTER TABLE Buch DROP Titel;
ALTER TABLE Buch DROP Untertitel;
ALTER TABLE Buch DROP Erscheinungsjahr;
ALTER TABLE Buch DROP Kurzbeschreibung;
ALTER TABLE Buch DROP FOREIGN KEY Buch_ibfk_2;
ALTER TABLE Buch DROP SorteId;

ALTER TABLE Ebook ADD COLUMN BuchId Integer(13) NOT NULL DEFAULT 0 AFTER ISBN;
UPDATE Ebook LEFT JOIN Buch ON Buch.ISBN = Ebook.BuchISBN SET Ebook.BuchId=Buch.BuchId;
ALTER TABLE Ebook ADD CONSTRAINT Ebook_infk_2 FOREIGN KEY (BuchId) REFERENCES Buch(BuchId);
ALTER TABLE Ebook DROP FOREIGN KEY Ebook_ibfk_1;
ALTER TABLE Ebook DROP BuchISBN;

ALTER TABLE Hoerbuch ADD COLUMN BuchId Integer(13) NOT NULL DEFAULT 0 AFTER ISBN;
UPDATE Hoerbuch LEFT JOIN Buch ON Buch.ISBN = Hoerbuch.BuchISBN SET Hoerbuch.BuchId=Buch.BuchId;
ALTER TABLE Hoerbuch ADD CONSTRAINT Hoerbuch_infk_2 FOREIGN KEY (BuchId) REFERENCES Buch(BuchId);
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
ALTER TABLE Ausleihe ADD CONSTRAINT Ausleihe_ibfk_3 FOREIGN KEY (MediumId) REFERENCES NichtTextMedium(NichtTextMediumId);

ALTER TABLE MediumWortZuord CHANGE MediumId MediumIdOld VARCHAR(17) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL; 
ALTER TABLE MediumWortZuord ADD COLUMN MediumId Integer(13) NOT NULL DEFAULT 0 AFTER MediumIdOld;
UPDATE MediumWortZuord LEFT JOIN Buch ON Buch.ISBN = MediumWortZuord.MediumIdOld SET MediumWortZuord.MediumId=Buch.BuchId;
ALTER TABLE MediumWortZuord DROP FOREIGN KEY MediumWortZuord_ibfk_1;
ALTER TABLE MediumWortZuord DROP MediumIdOld;
ALTER TABLE MediumWortZuord ADD CONSTRAINT MediumWortZuord_ibfk_3 FOREIGN KEY (MediumId) REFERENCES NichtTextMedium(NichtTextMediumId);

ALTER TABLE NichtTextMedium CHANGE NichtTextMediumId MediumId INT(13) NOT NULL AUTO_INCREMENT; 
RENAME TABLE NichtTextMedium TO Medium;
