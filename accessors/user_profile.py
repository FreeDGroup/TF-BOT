from botbuilder.core import TurnContext, UserState
from botbuilder.schema import ChannelAccount


class UserProfile:
    def __init__(self, name=None, is_logged_in=False):
        self.name = name
        self.is_logged_in = is_logged_in


class UserProfileAccessor:
    def __init__(self, user_state: UserState):
        self.user_state = user_state
        self.user_profile_accessor = self.user_state.create_property("UserProfile")

    async def get_user_profile(self, turn_context: TurnContext, channel_account: ChannelAccount) -> UserProfile:
        user_profile = await self.user_profile_accessor.get(turn_context, lambda: UserProfile())
        return user_profile

    async def set_user_logged_in(self, turn_context: TurnContext, channel_account: ChannelAccount):
        user_profile = await self.get_user_profile(turn_context, channel_account)
        user_profile.is_logged_in = True
        user_profile.name = channel_account.name
        await self.user_profile_accessor.set(turn_context, user_profile)
        await self.user_state.save_changes(turn_context)
