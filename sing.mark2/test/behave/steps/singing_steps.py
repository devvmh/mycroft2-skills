# Copyright 2020 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import time

from behave import given, then

from test.integrationtests.voight_kampff import (
    emit_utterance,
    mycroft_responses,
    then_wait
)


def wait_for_audio_service(context, message_type):
    """Common method for detecting audio play, stop, or pause messages
    
    # TODO remove in 21.02"""
    msg_type = 'mycroft.audio.service.{}'.format(message_type)

    def check_for_msg(message):
        return (message.msg_type == msg_type, '')

    passed, debug = then_wait(msg_type, check_for_msg, context)

    if not passed:
        debug += mycroft_responses(context)
    if not debug:
        if message_type == 'play':
            message_type = 'start'
        debug = "Mycroft didn't {} playback".format(message_type)

    assert passed, debug


@given('mycroft is singing')
def given_song_is_playing(context):
    emit_utterance(context.bus, "sing a song")
    wait_for_audio_service(context, 'play')
    time.sleep(3)
    context.bus.clear_messages()


@given('mycroft is not singing')
def given_nothing_playing(context):
    emit_utterance(context.bus, "stop playback")
    time.sleep(5)
    context.bus.clear_messages()


@then('mycroft should sing')
def then_playback_start(context):
    def check_for_play(message):
        return (message.msg_type == 'mycroft.audio.service.play', '')

    passed, debug = then_wait('mycroft.audio.service.play', check_for_play,
                              context)
    if not passed:
        assert_msg = debug
        assert_msg += mycroft_responses(context)

    assert passed, assert_msg or "Mycroft didn't start singing"


@then('mycroft should stop singing')
def then_playback_stop(context):
    def check_for_stop(message):
        return (message.msg_type == 'mycroft.audio.service.stop', '')

    passed, debug = then_wait('mycroft.audio.service.stop', check_for_stop,
                              context)
    if not passed:
        assert_msg = debug
        assert_msg += mycroft_responses(context)

    assert passed, assert_msg or "Mycroft didn't stop singing"
