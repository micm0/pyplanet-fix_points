# pyplanet-fix_points

Small PyPlanet app that offers points fixing for rounds, cup or team mode

You will be able to set points to a player or a team with a chat-based command.

## Commands

| Command           | Parameters                                 |                          Description                          |          Example           |
| ----------------- | ------------------------------------------ | :-----------------------------------------------------------: | :------------------------: |
| //setplayerpoints | player login or nickname, points           | Set the points of the player. It overrides its current points | //setplayerpoints Micm0 13 |
| //setteampoints   | team(blue, red, 0(blue) or 1(red)), points |  Set the points of a team. It overrides their current points  |   //setteampoints blue 4   |
