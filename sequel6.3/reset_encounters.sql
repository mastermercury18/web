DROP TABLE IF EXISTS encounters;

CREATE TABLE encounters (
    id1 INTEGER,
    id2 INTEGER,
    encounter_type TEXT CHECK(encounter_type IN ('friendly', 'neutral', 'unfriendly')),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id1) REFERENCES heros(id),
    FOREIGN KEY (id2) REFERENCES heros(id)
);