# Takes the App Store screenshots: six for iPhone 6.3" (1206 x 2622) and six for iPad 13" (2064 x 2752).
# Build and serve the app's files first: node scripts/build-www.js, then python3 -m http.server 8770 --directory www
# Then: python3 tools/screenshots.py appstore/screenshots
import asyncio, sys
from playwright.async_api import async_playwright
OUT = sys.argv[1]
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel="chrome", args=["--no-sandbox"])
        for dev, w, h, scale in (("iphone", 402, 874, 3), ("ipad", 1032, 1376, 2)):
            ctx = await b.new_context(viewport={"width": w, "height": h}, device_scale_factor=scale, color_scheme="dark", has_touch=True, is_mobile=True)
            pg = await ctx.new_page(); errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            await pg.goto("http://localhost:8770/index.html"); await pg.wait_for_timeout(1000)
            async def shot(name, sel=None, pad=12):
                if sel: await pg.evaluate("([s,p]) => { const e = document.querySelector(s); window.scrollTo(0, e.getBoundingClientRect().top + window.scrollY - p); }", [sel, pad])
                else: await pg.evaluate("window.scrollTo(0,0)")
                await pg.wait_for_timeout(300)
                await pg.screenshot(path=f"{OUT}/{dev}-{name}.png")
            async def cmd(t, wait=1100):
                await pg.fill("#cmd", t); await pg.press("#cmd", "Enter"); await pg.wait_for_timeout(wait)
            await shot("05-online")
            await shot("02-setup", "#setupBar")
            await pg.click("#manualBtn"); await pg.wait_for_timeout(300)
            for t in ("place 1 e4", "place flag a1", "place bomb a2", "place bomb b1", "place 9 f4", "place 5 d4"): await cmd(t, 150)
            await pg.evaluate("document.activeElement && document.activeElement.blur()")
            await shot("06-place", "#reserveBox" if dev == "iphone" else "#setupBar")
            await cmd("fill", 300)
            await pg.click("#startBtn"); await pg.wait_for_timeout(600)
            # march a few pieces forward until there have been some fights
            for step in range(4):
                for col in "aebfij":
                    for (a, c) in ((4, 5), (5, 6), (6, 7), (7, 8)):
                        if await pg.evaluate("document.getElementById('turnLine').dataset.who") not in ("you",): await pg.wait_for_timeout(900)
                        await cmd(f"{col}{a} {col}{c}", 1000)
                fights = await pg.evaluate("[...document.querySelectorAll('#log li')].filter(l => /defeat|captur|destroy|both|defus/i.test(l.textContent)).length")
                if fights >= 6: break
            await pg.evaluate("document.activeElement && document.activeElement.blur()")
            print(dev, "turn:", await pg.inner_text("#turnLine"), "| fights:", fights, "| last:", (await pg.evaluate("document.querySelector('#log li')?.textContent || ''"))[:110])
            await cmd("known", 300)
            await pg.evaluate("document.activeElement && document.activeElement.blur()")
            await shot("01-battle", "#playBar" if dev == "iphone" else "#turnLine", 14 if dev == "iphone" else 40)
            await shot("03-log", "#logHead")
            await pg.evaluate("document.querySelector('#helpHead + details').open = true")
            await shot("04-rules", "#helpHead")
            print(dev, "errors:", errs)
            await ctx.close()
        await b.close()
asyncio.run(main())
