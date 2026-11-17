# Saves the app icon (1024 x 1024) and the launch image (2732 x 2732) from tools/icon.html.
# Serve the repo first: python3 -m http.server 8771, then: python3 tools/icon.py <output folder>
import asyncio, sys
from playwright.async_api import async_playwright
OUT = sys.argv[1]
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel="chrome", args=["--no-sandbox"])
        for name, q, n in (("AppIcon-1024.png", "", 1024), ("splash-2732.png", "?splash", 2732)):
            pg = await b.new_page(viewport={"width": n, "height": n})
            await pg.goto("http://localhost:8771/tools/icon.html" + q)
            await pg.evaluate("document.fonts.load('700 360px \"Barlow Condensed\"')"); await pg.wait_for_timeout(400)
            await pg.screenshot(path=f"{OUT}/{name}", clip={"x": 0, "y": 0, "width": n, "height": n})
            await pg.close()
        await b.close()
asyncio.run(main())
