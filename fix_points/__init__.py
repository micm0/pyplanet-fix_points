from pyplanet.apps.config import AppConfig
from pyplanet.contrib.command import Command

class PointsManager(AppConfig):
    name = 'fix_points'
    app_dependencies = ['core.maniaplanet']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_start(self):
        await self.instance.permission_manager.register('admin', 'Set team or player points', app=self, min_level=2)
        await self.instance.command_manager.register(
            Command(command='setplayerpoints', target=self.set_points_to_player, perms='fix_points:admin', admin=True, description='Set the points of the player. It overrides its current points($i//setplayerpoints loginornickname points).')
            .add_param(name='player', required=True).add_param(name='points', required=True),
        )
        await self.instance.command_manager.register(
            Command(command='setteampoints', target=self.set_points_to_team, perms='fix_points:admin', admin=True, description='Set the points of a team. It overrides their current points($i//setteampoints team points. $z$s0 for Blue and 1 for Red).')
            .add_param(name='team', required=True).add_param(name='points', required=True),
        )

    async def set_points_to_player(self, player, data = None, **kwargs):
        current_script = await self.instance.mode_manager.get_current_script()
        if not self.is_rounds_or_cup_mode(current_script):
            await self.instance.chat(f'$f00Command available only for rounds or cup mode !', player.login)
        else:
            player_found = await self.find_player_by_login_or_nickname(data.player)
            if not len(player_found) == 1:
                await self.instance.chat(f'{data.player} $f00is not found!', player.login)
            else:
                await self.instance.gbx.script('Trackmania.SetPlayerPoints', player_found[0].login, "", "", data.points, encode_json=False, response_id=False)
                await self.instance.chat(f'$0C0{player.nickname} sets points of {player_found[0].nickname} to {data.points}!')

    async def set_points_to_team(self, player, data = None, **kwargs):
        current_script = await self.instance.mode_manager.get_current_script()
        if not self.is_team_mode(current_script):
            await self.instance.chat(f'$f00Command available only for team mode !', player.login)
        else:
            if data.team == '0' or data.team.lower() == 'blue':
                team = '0'
                teamstring = '$00FBlue$z$s$0C0'
            elif data.team == '1' or data.team.lower() == 'red':
                team = '1'
                teamstring = '$F00Red$z$s$0C0'
            else:
                team = False
                await self.instance.chat(f'$f00Team {data.team} unknown. Please use $iblue $z$s$f00or $ired $z$s$f00or $i0 $z$s$f00(blue) or $i1 $z$s$f00(red)!', player.login)
            if team:
                await self.instance.gbx.script('Trackmania.SetTeamPoints', team, "", data.points, encode_json=False, response_id=False)
                await self.instance.chat(f'$0C0{player.nickname} sets points of {teamstring} Team to {data.points}!')

    async def find_player_by_login_or_nickname(self, player_login_or_nickname):
        player_found = [p for p in self.instance.player_manager.online if p.nickname.lower() == player_login_or_nickname.lower() or p.login == player_login_or_nickname]
        return player_found

    def is_rounds_or_cup_mode(self, mode):
        mode = mode.lower()
        return mode.startswith('rounds') or mode.startswith('cup') or \
               mode.startswith('trackmania/tm_rounds_online') or mode.startswith('trackmania/tm_cup_online')

    def is_team_mode(self, mode):
        mode = mode.lower()
        return mode.startswith('team') or mode.startswith('trackmania/tm_teams_online')