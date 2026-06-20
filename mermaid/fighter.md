```mermaid
sequenceDiagram
    participant Page as Flet Page (main.py)
    participant DB as DuckDB (tk.db)
    participant CSV as fighter.csv

    Page->>DB: CREATE TABLE IF NOT EXISTS fighter
    Page->>CSV: read_csv_auto('data/fighter.csv')
    CSV-->>Page: id, name, nationality, fighting_style
    Page->>DB: INSERT INTO character ON CONFLICT (id) DO NOTHING
    DB-->>Page: 저장 완료
```