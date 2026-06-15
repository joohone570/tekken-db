import pandas as pd
import flet as ft
import duckdb

con = duckdb.connect("data/tk.db")


def main(page: ft.Page):
    page.title = "Tekken Character Viewer"
    page.window.width = 900
    page.window.height = 700
    page.scroll = ft.ScrollMode.AUTO

    # -------------------------------
    # DB 생성
    # -------------------------------

    con.execute("DROP TABLE IF EXISTS frame")
    con.execute("DROP TABLE IF EXISTS primary_skill")
    con.execute("DROP TABLE IF EXISTS character")

    con.execute("""
        CREATE TABLE IF NOT EXISTS character (
            id BIGINT PRIMARY KEY,
            name VARCHAR,
            nationality VARCHAR,
            fighting_style VARCHAR,
            image_path VARCHAR
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
            skill_name VARCHAR,
            command VARCHAR,
            FOREIGN KEY(character_id)
            REFERENCES character(id)
        )
    """)

    con.execute("""
        INSERT OR IGNORE INTO primary_skill
        SELECT *
        FROM read_csv_auto('data/primary_skill.csv')
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
        SELECT *
        FROM read_csv_auto('data/frame.csv')
    """)

    # -------------------------------
    # 조회 함수
    # -------------------------------

    def get_character(character_id):
        return con.execute("""
        SELECT *
        FROM character
        WHERE id=?
    """, [character_id]).fetchone()

    def get_skills(character_id):
        return con.execute("""
        SELECT *
        FROM primary_skill
        WHERE character_id=?
    """, [character_id]).fetchall()

    def get_frame(skill_id):
        return con.execute("""
        SELECT *
        FROM frame
        WHERE skill_id=?
    """, [skill_id]).fetchone()

    current_character_id = [1]
    current_character_name = ["카즈야"]

    info_area = ft.Column()
    skill_area = ft.Column()
    frame_area = ft.Column()
    character_image = ft.Image(
        src="",
        width=200,
        height=200
)

    def show_info(e):
        character = get_character(current_character_id[0])
        info_area.controls.clear()
        info_area.controls.extend([
            ft.Text(f"국적 : {character[2]}"),
            ft.Text(f"격투 스타일 : {character[3]}")
        ])
        page.update()

    def show_frame(skill_id):
        frame = get_frame(skill_id)
        frame_area.controls.clear()
        frame_area.controls.extend([
            ft.Text(f"Startup Frame : {frame[2]}"),
            ft.Text(f"On Hit : {frame[3]}"),
            ft.Text(f"On Block : {frame[4]}")
        ])
        page.update()

    def show_skills(e):
        skills = get_skills(current_character_id[0])

        skill_area.controls.clear()

        for skill in skills:
            skill_area.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Text(
                            f"기술명 : {skill[2]}"
                        ),
                        ft.Text(
                            f"커맨드 : {skill[3]}"
                        ),
                        ft.ElevatedButton(
                            "프레임 보기",
                            on_click=lambda e, sid=skill[0]:
                            show_frame(sid)
                        )
                    ])
                )
            )

    page.update()

    def select_character(character_id):
        current_character_id[0] = character_id
        character = get_character(character_id)
        current_character_name[0] = character[1]
        character_image.src = character[4]
        info_area.controls.clear()
        skill_area.controls.clear()
        frame_area.controls.clear()
        page.update()

    character_panel = ft.Container(
        content=ft.Column([
            ft.Text("캐릭터"),
            ft.Button("카즈야", on_click=lambda e: select_character(1)),
            ft.Button("진", on_click=lambda e: select_character(2))
        ])
    )

    character_info_panel = ft.Row([
        ft.Container(
            content=ft.Column([
                ft.Text("정보"),
                ft.Button("조회", on_click=show_info)
            ])
        ),
        ft.Container(content=info_area)
    ])

    skill_panel = ft.Row([
        ft.Container(
            content=ft.Column([
                ft.Text("주력기"),
                ft.Button("조회", on_click=show_skills)
            ])
        ),
        ft.Container(
            width=350,
            height=200,
            content=ft.ListView(controls=[skill_area])
        )
    ])

    frame_panel = ft.Row([
        ft.Container(width=350, content=frame_area)
    ])


    page.add(
        ft.Text("4.1 캐릭터 선택 조회"),
        character_panel,
        ft.Text("캐릭터 이미지"),
        character_image,
        ft.Text("4.2 캐릭터 정보 조회"),
        character_info_panel,
        ft.Text("4.3 주력기 정보 조회"),
        skill_panel,
        ft.Text("4.4 주력기 프레임 정보 조회"),
        frame_panel
    )

    select_character(1)


ft.run(main)