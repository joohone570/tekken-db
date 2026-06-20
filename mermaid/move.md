```mermaid
sequenceDiagram
    participant Page as Flet Page (main.py)
    participant DB as DuckDB (tk.db)
    participant CSV as move.csv

     Page->>DB: DROP TABLE IF EXISTS move
    Page->>DB: CREATE TABLE IF NOT EXISTS move
    Page->>CSV: read_csv_auto('data/move.csv')
    CSV-->>Page: move data
    Page->>DB: INSERT OR IGNORE INTO move 
    DB->>DB: FK 확인: fighter_id → fighter.id
    DB-->>Page: Data Stored
```