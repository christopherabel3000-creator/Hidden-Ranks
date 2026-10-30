# Hidden Ranks

A screen-reader-friendly hidden-rank strategy game played on a 10 by 10 board against a computer opponent. Capture the enemy Flag while their ranks stay hidden until battle.

Play it here: https://christopherabel3000-creator.github.io/Hidden-Ranks/

## Online play

Press **Host an online game** to get a four-letter code and invite link for a friend. Games are stored in the Firebase Realtime Database project shared with Gridiron Duel, Shardkin: Eight Realms and Friday to Sunday, under `hiddenRanks/`. The rules for all four games are in `database.rules.json`, and the Gridiron Duel, Shardkin and Friday to Sunday repos have identical copies. Always paste the whole file into the Realtime Database Rules tab of the Firebase console, and keep the four copies the same, or the other games will stop working online.

## How to play

- Arrow keys move around the board, and Enter selects or moves a piece.
- You can also type commands such as `e4 e5`, `f7`, `row 4`, `moves`, `known`, `status` or `help`.
- The full rules are in the "How to play" section of the game.
