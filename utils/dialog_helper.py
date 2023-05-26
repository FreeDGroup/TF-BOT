# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import StatePropertyAccessor, TurnContext
from botbuilder.dialogs import DialogSet, DialogTurnStatus


class DialogHelper:
    @staticmethod
    async def run_dialog(
        dialog_id: str, dialog_set: DialogSet, turn_context: TurnContext, accessor: StatePropertyAccessor
    ):
        dialog_context = await dialog_set.create_context(turn_context, accessor)

        results = await dialog_context.continue_dialog()
        if results.status == DialogTurnStatus.Empty:
            await dialog_context.begin_dialog(dialog_id)
