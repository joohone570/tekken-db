```mermaid
sequenceDiagram
    participant Page as Flet Page (main.py)
    participant DB as DuckDB (tk.db)
    participant CSV as move_frame.csv

     Page->>DB: DROP TABLE IF EXISTS move_frame
    Page->>DB: CREATE TABLE IF NOT EXISTS move_frame
    Page->>CSV: read_csv_auto('data/move_frame.csv')
    CSV-->>Page: move_frame data
    Page->>DB: INSERT OR IGNORE INTO move_frame 
    DB->>DB: FK 확인: move_id → move.id
    DB-->>Page: Data Stored
```