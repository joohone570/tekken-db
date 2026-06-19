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

    con.execute("DROP TABLE IF EXISTS move_frame")
    con.execute("DROP TABLE IF EXISTS move")
    con.execute("DROP TABLE IF EXISTS fighter")

    con.execute("""
        CREATE TABLE IF NOT EXISTS fighter (
            id BIGINT PRIMARY KEY,
            name VARCHAR,
            nationality VARCHAR,
            fighting_style VARCHAR,
            image_path VARCHAR
        )
    """)

    con.execute("""
        INSERT OR IGNORE INTO fighter
        SELECT * FROM read_csv_auto('data/fighter.csv')
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS move (
            id BIGINT PRIMARY KEY,
            fighter_id BIGINT,
            move_name VARCHAR,
            command VARCHAR,
            FOREIGN KEY(fighter_id)
            REFERENCES fighter(id)
        )
    """)

    con.execute("""
        INSERT OR IGNORE INTO move
        SELECT *
        FROM read_csv_auto('data/move.csv')
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS move_frame (
            id BIGINT PRIMARY KEY,
            move_id BIGINT,
            startup INT,
            Hit INT,
            Block INT,
            Counter INT,
            FOREIGN KEY(move_id)
            REFERENCES move(id)
        )
    """)

    con.execute("""
        INSERT OR IGNORE INTO move_frame
        SELECT *
        FROM read_csv_auto('data/move_frame.csv')
    """)

    # -------------------------------
    # 조회 함수
    # -------------------------------

    def get_character(fighter_id):
        return con.execute("""
        SELECT *
        FROM fighter
        WHERE id=?
    """, [fighter_id]).fetchone()

    def get_skills(fighter_id):
        return con.execute("""
        SELECT *
        FROM move
        WHERE fighter_id=?
    """, [fighter_id]).fetchall()

    def get_frame(move_id):
        return con.execute("""
        SELECT *
        FROM move_frame
        WHERE move_id=?
    """, [move_id]).fetchone()

    current_fighter_id = [1]
    current_fighter_name = ["카즈야"]

    info_area = ft.Column()
    move_area = ft.Column()
    move_frame_area = ft.Column()
    fighter_image = ft.Image(
        src="",
        width=200,
        height=200
    )

    def show_info(e):
        fighter = get_character(current_fighter_id[0])
        info_area.controls.clear()
        info_area.controls.extend([
            ft.Text(f"국적 : {fighter[2]}"),
            ft.Text(f"격투 스타일 : {fighter[3]}")
        ])
        page.update()

    def show_frame(skill_id):
        move_frame = get_frame(skill_id)
        move_frame_area.controls.clear()
        move_frame_area.controls.extend([
            ft.Text(f"Startup : {move_frame[2]}"),
            ft.Text(f"Hit : {move_frame[3]}"),
            ft.Text(f"Block : {move_frame[4]}"),
            ft.Text(f"Counter : {move_frame[5]}")
        ])
        page.update()

    def show_skills(e):
        moves = get_skills(current_fighter_id[0])

        move_area.controls.clear()

        for skill in moves:
            move_area.controls.append(
                ft.Column([
                    ft.Text(f"기술명 : {skill[2]}"),
                    ft.Text(f"커맨드 : {skill[3]}"),
                    ft.Button(
                        "프레임 보기",
                        on_click=lambda e, sid=skill[0]:
                        show_frame(sid)
                    ),
                    ft.Text("----------------")
                ])
            )

    page.update()

    def select_character(fighter_id):
        current_fighter_id[0] = fighter_id
        fighter = get_character(fighter_id)
        current_fighter_name[0] = fighter[1]
        fighter_image.src = fighter[4]
        info_area.controls.clear()
        move_area.controls.clear()
        move_frame_area.controls.clear()
        page.update()

    character_panel = ft.Container(
        content=ft.Column([
            ft.Text("파이"),
            ft.Button("카즈야", on_click=lambda e: select_character(1)),
            ft.Button("진", on_click=lambda e: select_character(2)),
            ft.Button("빅터",on_click=lambda e: select_character(3))
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

    move_panel = ft.Row([
        ft.Container(
            content=ft.Column([
                ft.Text("기술"),
                ft.Button("조회", on_click=show_skills)
            ])
        ),
        ft.Container(
            width=350,
            height=200,
            content=ft.ListView(controls=[move_area])
        )
    ])

    move_frame_panel = ft.Row([
        ft.Container(width=350, content=move_frame_area)
    ])

    page.add(
        ft.Text("4.1 캐릭터 선택 조회"),
        character_panel,
        ft.Text("캐릭터 이미지"),
        fighter_image,
        ft.Text("4.2 캐릭터 정보 조회"),
        character_info_panel,
        ft.Text("4.3 기술 정보 조회"),
        move_panel,
        ft.Text("4.4 기술 프레임 정보 조회"),
        move_frame_panel
    )

    select_character(1)


ft.run(main)
