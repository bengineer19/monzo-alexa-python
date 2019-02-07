"""Alexa handler."""
import os
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_model.ui import SimpleCard

from monzo_getter import MonzoGetter
from price_getter import price_lookup_pounds

sb = SkillBuilder()

# Get token from https://developers.monzo.com/
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
# TODO: make this settable/configurable from the skill
MONTHLY_BUDGET = 1000

@sb.request_handler(can_handle_func=lambda handler_input:
                    is_intent_name("AMAZON.CancelIntent")(handler_input) or
                    is_intent_name("AMAZON.StopIntent")(handler_input) or
                    is_intent_name("AMAZON.FallbackIntent")(handler_input))
def fallback_handler(handler_input):
    speech_text = "See you later! Enjoy the hackathon."

    handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Hello World", speech_text)).set_should_end_session(
        True)
    return handler_input.response_builder.response

@sb.request_handler(can_handle_func=is_intent_name("GetBalance"))
def balance_intent_handler(handler_input):
    # type: (HandlerInput) -> Response

    monzo = MonzoGetter(ACCESS_TOKEN)
    balance = monzo.get_balance_pounds()
    speech_text = f"Your balance is {balance} pounds"

    handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Hello World", speech_text)).set_should_end_session(
        False)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("GetMonthlySpend"))
def monthly_spend_intent_handler(handler_input):
    # type: (HandlerInput) -> Response

    monzo = MonzoGetter(ACCESS_TOKEN)
    monthly_spend = monzo.get_monthly_spend_pounds()
    speech_text = f"So far this month you've spent {monthly_spend} pounds"

    handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Hello World", speech_text)).set_should_end_session(
        False)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("GetPurchaseApproval"))
def can_i_afford_intent_handler(handler_input):
    # type: (HandlerInput) -> Response

    slots = handler_input.request_envelope.request.intent.slots
    print(f"Slots: {slots}")
    purchase = slots['purchase'].value.lower()
    print(f"purchase: {purchase}")

    monzo = MonzoGetter(ACCESS_TOKEN)
    monthly_spend = monzo.get_monthly_spend_pounds()

    try:
        price = price_lookup_pounds[purchase]
        if price > (MONTHLY_BUDGET - monthly_spend):
            speech_text = f"Sorry, you can't afford this. A {purchase} " \
                          f"costs about {price} pounds. You've already spent " \
                          f"{monthly_spend} pounds this month."
        else:
            remaining = MONTHLY_BUDGET - monthly_spend - price
            speech_text = f"You can afford that. A {purchase} costs about " \
                          f"{price} pounds. If you buy it your remaining " \
                          f"monthly budget will be {remaining}"
    except KeyError:
        # Just in case....
        speech_text = "Sorry, we couldn't find a price for that product." \
                      f"You have {MONTHLY_BUDGET - monthly_spend} pounds" \
                      " left to spend this month"

    handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Hello World", speech_text)).set_should_end_session(
        False)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input):
    # type: (HandlerInput) -> Response
    speech_text = f"Yo yo yo what's popping. Come checkout what is up with your Monzo"

    handler_input.response_builder.speak(speech_text).set_card(
         SimpleCard("Hello World", speech_text)).set_should_end_session(
         False)
    return handler_input.response_builder.response


lambda_handler = sb.lambda_handler()

if __name__ == '__main__':
    monzo = MonzoGetter(ACCESS_TOKEN)
    monthly_spend = monzo.get_monthly_spend_pounds()
    print(monthly_spend)
