# Hidden Ranks

A screen-reader-friendly hidden-rank strategy game played on a 10 by 10 board against a computer opponent or a friend online. Capture the enemy Flag while their ranks stay hidden until battle.

Play it here: https://christopherabel3000-creator.github.io/Hidden-Ranks/

## How to play

- Arrow keys move around the board, and Enter selects or moves a piece. On a touch screen, tap a piece and then a square.
- You can also type commands such as `e4 e5`, `f7`, `row 4`, `moves`, `known`, `status` or `help`.
- The full rules are in the "How to play" section of the game.

## Files

- `index.html` — the whole game: the page, its styles and its code (plain HTML, CSS and JavaScript, no build step)
- `firebase-config.js` — the settings of the Firebase project used for online play
- `fonts/` — the game's two fonts (Atkinson Hyperlegible and Barlow Condensed, both under the SIL Open Font License), kept with the game so it looks right offline
- `vendor/firebase/` — the Firebase library (version 10.12.2), kept with the game
- `icons/` — the website's icons
- `privacy.html`, `support.html` — the privacy policy and the support page, linked from the bottom of the game and used as the App Store's Privacy Policy URL and Support URL
- `database.rules.json` — the Firebase Realtime Database rules for online play
- `package.json`, `capacitor.config.json`, `scripts/build-www.js`, `ios/`, `.github/workflows/ios.yml` — the iPhone app (see App Store below)
- `appstore/` — the App Store listing text and screenshots. Not part of the game or the app.
- `tools/icon.html`, `tools/icon.py` — draw the app icon and launch image. `tools/screenshots.py` — takes the App Store screenshots. Both are run with Python and Playwright; the notes at the top of each say how.

## Online play

Press **Host an online game** to get a four-letter code and invite link for a friend. Games are stored in the game's own Firebase project, `hidden-ranks` (Realtime Database, US), under `hiddenRanks/<CODE>`. The rules are in `database.rules.json` and are published in the Firebase console (Realtime Database, then Rules). Change the file and the console together.

Until November 2026 the game used the call-sheet-football project shared with the other games. Games in progress at the changeover weren't carried across.

The rules only accept well-formed records and require every change to be exactly one version newer than the last, so a game can't be rewound or wiped. A game nobody has touched in 7 days can be deleted, which the game does when its code comes up again. Nobody can list the games; a game can only be read with its code. A game holds each player's army layout, the moves, and a random code for each player's device. There are no names or messages.

A player on the website and a player in the App Store app can play each other. In the app, the invite link points at the website.

## App Store

The App Store version wraps the same files with [Capacitor](https://capacitorjs.com). Nothing about the game changes: `scripts/build-www.js` copies the page, the two extra pages, `firebase-config.js`, `fonts/`, `icons/` and `vendor/` into `www/`, and `npx cap sync ios` puts them in the Xcode project in `ios/`. In the app, saved setups are also kept as a file in the app's Documents folder (see "The iPhone app's own copy of saved setups" in index.html), which iOS never clears; if the web view's storage comes up empty at startup, the setups are restored from that file.

There's no Mac needed: `.github/workflows/ios.yml` builds the app on GitHub's Macs. Every push that touches the game checks that it still builds; running the workflow by hand (Actions, iPhone app, Run workflow) signs it and sends it to TestFlight. Signing needs four repo secrets, listed at the top of the workflow. The app is `com.playbyear.hiddenranks`.
