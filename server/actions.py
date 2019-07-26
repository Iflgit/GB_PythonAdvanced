from functools import reduce
from server.settings import INSTALLED_APPS


def get_server_actions():
    print('get_server_actions call')
    modules = reduce(
        lambda value, item: value + [__import__(f'{item}.actions')],
        INSTALLED_APPS, []
    )

    actions = reduce(
        lambda value, item: value + [getattr(item, 'actions', [])],
        modules, []
    )

    return reduce(
        lambda value, item: value + getattr(item, 'actionnames', []),
        actions, []
    )

def resolve(action_name, actions=None):
    print('resolve call')
    action_list = actions or get_server_actions()
    action_mapping = {
        actions.get('action'): actions.get('controller')
        for actions in action_list
    }
    return action_mapping.get(action_name)

