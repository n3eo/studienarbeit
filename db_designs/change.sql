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