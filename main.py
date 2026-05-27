import flet as ft
import pandas as pd
import duckdb

con = duckdb.connect("data/tk.db")

def main(page: ft.Page):
    page.title = "tk"
    page.padding = 16
    page.window.width = 400
    page.window.height = 400

    con.execute("""
            CREATE TABLE IF NOT EXISTS character (
                id BIGINT PRIMARY KEY,
                name VARCHAR,
                nationality VARCHAR,
                fighting_skill VARCHAR
            )
        """)

    con.execute("""
            INSERT OR IGNORE INTO character 
            SELECT * FROM read_csv_auto('data/character.csv')
        """)

    con.execute("""
            CREATE TABLE IF NOT EXISTS primary_skill (
                id BIGINT PRIMARY KEY,
                character_id BIGINT,
                command_name VARCHAR,
                command VARCHAR,
                Hit_Level VARCHAR,
                FOREIGN KEY(character_id)
                REFERENCES character(id)
            )
        """)

    con.execute("""
        INSERT OR IGNORE INTO primary_skill
        SELECT * FROM read_csv_auto('data/primary_skill.csv')
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS frame (
            id BIGINT PRIMARY KEY,
            skill_id BIGINT,
            startup_frame INT,
            On_Hit INT,
            On_Block INT,
            FOREIGN KEY(skill_id)
            REFERENCES primary_skill(id)
        )
    """)

    con.execute("""
        INSERT OR IGNORE INTO frame
        SELECT * FROM read_csv_auto('data/frame.csv')
    """)

    print("데이터베이스 저장 완료")
    
    snack_bar = ft.SnackBar(
        content=ft.Text("데이터베이스 저장 완료")
    )
    page.overlay.append(snack_bar)
    snack_bar.open = True

if __name__ == "__main__":
    ft.run(main)