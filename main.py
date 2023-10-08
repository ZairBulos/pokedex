import flet as ft
import aiohttp
import asyncio

current_pokemon = 0

async def main(page: ft.Page):
    page.window_width = 600
    page.window_height = 800
    page.window_resizable = False
    page.padding = 0
    page.margin = 0
    page.fonts = {"zpix": "https://github.com/SolidZORO/zpix-pixel-font/releases/download/v3.1.8/zpix.ttf"}
    page.theme = ft.Theme(font_family="zpix")

    async def fetch_pokemon_data(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json()

    async def get_pokemon(e: ft.ContainerTapEvent):
        global current_pokemon

        if e.control == arrow_sup:
            current_pokemon += 1
        else:
            current_pokemon -= 1

        number = (current_pokemon % 150) + 1
        result = await fetch_pokemon_data(f"https://pokeapi.co/api/v2/pokemon/{number}")

        info = f"Name: {result['name']}\n\nAbilities:"
        abilities = [e['ability']['name'] for e in result['abilities']]
        info += "\n" + "\n".join(abilities)

        text.value = info
        sprite_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{number}.png"
        image_pokemon.src = sprite_url

        await page.update_async()

    async def blink():
        while True:
            await asyncio.sleep(1)
            light_blue.bgcolor = ft.colors.BLUE_100
            await page.update_async()
            await asyncio.sleep(0.1)
            light_blue.bgcolor = ft.colors.BLUE
            await page.update_async()

    # Container Top
    light_blue = ft.Container(width=50, height=50, bgcolor=ft.colors.BLUE, border_radius=50, left=5, top=5)
    btn_blue = ft.Stack([
        ft.Container(width=60, height=60, bgcolor=ft.colors.WHITE, border_radius=50),
        light_blue
    ])
    items_container_top = [
        ft.Container(btn_blue, width=60, height=60),
        ft.Container(width=30, height=30, bgcolor=ft.colors.RED_200, border_radius=50),
        ft.Container(width=30, height=30, bgcolor=ft.colors.YELLOW, border_radius=50),
        ft.Container(width=30, height=30, bgcolor=ft.colors.GREEN, border_radius=50),
    ]
    container_top = ft.Container(
        content=ft.Row(items_container_top),
        width=400,
        height=60,
        margin=ft.margin.only(top=40)
    )

    # Container Middle
    sprite_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/0.png"
    image_pokemon = ft.Image(
        src=sprite_url,
        scale=6,
        width=30,
        height=30,
        top=250/2,
        right=350/2
    )
    stack_middle = ft.Stack([
        ft.Container(width=400, height=300, bgcolor=ft.colors.WHITE),
        ft.Container(width=350, height=250, bgcolor=ft.colors.BLACK, top=25, left=25),
        image_pokemon
    ])
    container_middle = ft.Container(
        content=stack_middle,
        width=400,
        height=300,
        margin=ft.margin.only(top=20),
        alignment=ft.alignment.center
    )

    # Container Bottom
    triangle = ft.canvas.Canvas([
        ft.canvas.Path([
            ft.canvas.Path.MoveTo(30, 0),
            ft.canvas.Path.LineTo(0, 50),
            ft.canvas.Path.LineTo(60, 50),
        ],
        paint=ft.Paint(
            style=ft.PaintingStyle.FILL
        ))
    ],
    width=60,
    height=50
    )
    text = ft.Text(value="...", color=ft.colors.BLACK, size=18)
    arrow_sup = ft.Container(triangle, width=60, height=50, on_click=get_pokemon)
    arrow_inf = ft.Container(triangle, width=60, height=50, on_click=get_pokemon, rotate=ft.Rotate(angle=3.14159))
    arrows = ft.Column([arrow_sup, arrow_inf])
    items_bottom = [
        ft.Container(width=30),
        ft.Container(text, padding=10, width=300, height=200, bgcolor=ft.colors.GREEN),
        ft.Container(arrows, width=60, height=100, alignment=ft.alignment.center),
        ft.Container(width=30),
    ]
    container_bottom = ft.Container(
        content=ft.Row(items_bottom),
        width=400,
        height=250,
        margin=ft.margin.only(top=40)
    )

    # Container Principal
    col = ft.Column(spacing=0, controls=[
        container_top,
        container_middle,
        container_bottom
    ])
    container = ft.Container(
        col,
        width=600,
        height=800,
        bgcolor=ft.colors.RED,
        alignment=ft.alignment.top_center
    )

    await page.add_async(container)
    await blink()

ft.app(target=main)